"""
Leitor mínimo de arquivos SPSS .SAV para este projeto.

Objetivo: permitir que o notebook rode no Colab sem depender de pacotes externos
como pyreadstat. O leitor foi escrito para o arquivo CESOP/IPEC 04829.SAV,
que contém apenas variáveis numéricas e compressão padrão do SPSS.

Uso:
    from src.spss_sav_minimal_reader import read_sav
    df, meta = read_sav("data/raw/04829.SAV")
"""
from __future__ import annotations

from pathlib import Path
import json
import struct
import numpy as np
import pandas as pd


def _fix_mojibake(text):
    if not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text


def parse_sav_dictionary(path):
    raw = Path(path).read_bytes()
    if raw[:4] not in (b"$FL2", b"$FL3"):
        raise ValueError("Arquivo não parece ser um SPSS system file .SAV.")

    endian = "<"
    pos = 0
    magic = raw[pos:pos+4]; pos += 4
    product = raw[pos:pos+60].decode("latin1", errors="replace").rstrip("\x00 ").strip(); pos += 60
    layout, nominal_case_size, compression, weight_index, ncases = struct.unpack_from(endian + "5i", raw, pos); pos += 20
    bias = struct.unpack_from(endian + "d", raw, pos)[0]; pos += 8
    creation_date = raw[pos:pos+9].decode("latin1", errors="replace").strip(); pos += 9
    creation_time = raw[pos:pos+8].decode("latin1", errors="replace").strip(); pos += 8
    file_label = raw[pos:pos+64].decode("latin1", errors="replace").rstrip("\x00 ").strip(); pos += 64
    pos += 3

    variables = []
    short_to_long = {}
    value_label_sets = []
    var_to_label_set = {}
    encoding = "latin1"
    var_record_index = 0

    while True:
        rec_type = struct.unpack_from(endian + "i", raw, pos)[0]
        pos += 4

        if rec_type == 2:
            type_code, has_var_label, missing_value_format, print_format, write_format = struct.unpack_from(endian + "5i", raw, pos)
            pos += 20
            name = raw[pos:pos+8].decode("latin1", errors="replace").rstrip("\x00 ").strip()
            pos += 8

            label = ""
            if has_var_label:
                lab_len = struct.unpack_from(endian + "i", raw, pos)[0]
                pos += 4
                label = raw[pos:pos+lab_len].decode(encoding, errors="replace")
                pos += lab_len
                pos += (4 - (lab_len % 4)) % 4

            if missing_value_format:
                pos += abs(missing_value_format) * 8

            var_record_index += 1
            if type_code == -1:
                continue

            variables.append({
                "index": len(variables) + 1,
                "spss_index": var_record_index,
                "name": name,
                "type": type_code,
                "label": label,
                "print_format": print_format,
                "write_format": write_format,
            })

        elif rec_type == 3:
            n_labels = struct.unpack_from(endian + "i", raw, pos)[0]
            pos += 4
            labmap = {}
            for _ in range(n_labels):
                val = struct.unpack_from(endian + "d", raw, pos)[0]
                pos += 8
                lab_len = raw[pos]
                pos += 1
                label = raw[pos:pos+lab_len].decode(encoding, errors="replace").strip()
                pos += lab_len
                pos += (8 - ((lab_len + 1) % 8)) % 8
                key = int(val) if abs(val - round(val)) < 1e-9 else val
                labmap[key] = label
            value_label_sets.append(labmap)

        elif rec_type == 4:
            n_vars = struct.unpack_from(endian + "i", raw, pos)[0]
            pos += 4
            var_idxs = list(struct.unpack_from(endian + f"{n_vars}i", raw, pos))
            pos += 4 * n_vars
            label_set_id = len(value_label_sets) - 1
            for vi in var_idxs:
                for v in variables:
                    if v["spss_index"] == vi:
                        var_to_label_set[v["name"]] = label_set_id
                        break

        elif rec_type == 6:
            n_lines = struct.unpack_from(endian + "i", raw, pos)[0]
            pos += 4 + 80 * n_lines

        elif rec_type == 7:
            subtype, size, count = struct.unpack_from(endian + "3i", raw, pos)
            pos += 12
            payload = raw[pos:pos + size * count]
            pos += size * count

            if subtype == 20:
                text = payload.decode("latin1", errors="ignore").strip("\x00 ").strip()
                if "UTF-8" in text.upper():
                    encoding = "utf-8"
                elif "1252" in text:
                    encoding = "cp1252"
            elif subtype == 13:
                txt = payload.decode(encoding, errors="replace").strip("\x00 ")
                for pair in txt.split("\t"):
                    if "=" in pair:
                        short, long = pair.split("=", 1)
                        short_to_long[short.strip()] = long.strip()

        elif rec_type == 999:
            pos += 4
            data_start = pos
            break

        else:
            raise ValueError(f"Record type não suportado: {rec_type}")

    # Corrige acentos caso o dicionário tenha sido lido antes do registro de encoding.
    for v in variables:
        v["label"] = _fix_mojibake(v.get("label", ""))
    short_to_long = {_fix_mojibake(k): _fix_mojibake(v) for k, v in short_to_long.items()}
    value_label_sets = [
        {k: _fix_mojibake(v) for k, v in labmap.items()}
        for labmap in value_label_sets
    ]

    return {
        "raw": raw,
        "endian": endian,
        "product": product,
        "layout": layout,
        "nominal_case_size": nominal_case_size,
        "compression": compression,
        "weight_index": weight_index,
        "ncases": ncases,
        "bias": bias,
        "creation_date": creation_date,
        "creation_time": creation_time,
        "file_label": file_label,
        "variables": variables,
        "short_to_long": short_to_long,
        "value_label_sets": value_label_sets,
        "var_to_label_set": var_to_label_set,
        "data_start": data_start,
        "encoding": encoding,
    }


def read_sav(path):
    meta = parse_sav_dictionary(path)
    raw = meta["raw"]
    pos = meta["data_start"]
    nvars = meta["nominal_case_size"]
    ncases = meta["ncases"]
    bias = meta["bias"]
    endian = meta["endian"]

    values = []
    total = ncases * nvars
    while len(values) < total and pos < len(raw):
        ctrl = raw[pos:pos + 8]
        pos += 8
        for code in ctrl:
            if len(values) >= total:
                break
            if code == 0:
                continue
            if code == 253:
                values.append(struct.unpack_from(endian + "d", raw, pos)[0])
                pos += 8
            elif code in (254, 255):
                values.append(np.nan)
            elif 1 <= code <= 251:
                values.append(float(code - bias))

    arr = np.array(values, dtype=float).reshape((ncases, nvars))
    columns = [v["name"] for v in meta["variables"]]
    df = pd.DataFrame(arr, columns=columns)

    # Converte variáveis categóricas inteiras para Int64 quando possível.
    for col in df.columns:
        valid = df[col].dropna()
        if len(valid) and np.all(np.isclose(valid, np.round(valid), atol=1e-9)):
            try:
                df[col] = df[col].round().astype("Int64")
            except Exception:
                pass

    meta_public = dict(meta)
    meta_public.pop("raw", None)
    return df, meta_public


def write_codebook(meta, out_csv, out_json):
    value_labels_by_var = {}
    for v in meta["variables"]:
        name = v["name"]
        set_id = meta["var_to_label_set"].get(name)
        if set_id is not None:
            value_labels_by_var[name] = meta["value_label_sets"][set_id]

    rows = []
    for v in meta["variables"]:
        name = v["name"]
        set_id = meta["var_to_label_set"].get(name)
        rows.append({
            "name": name,
            "long_name": meta["short_to_long"].get(name, name),
            "label": v.get("label", ""),
            "type": "numeric" if v["type"] == 0 else f"string({v['type']})",
            "spss_index": v["spss_index"],
            "label_set_id": set_id if set_id is not None else "",
            "value_labels_json": json.dumps(value_labels_by_var.get(name, {}), ensure_ascii=False),
        })
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({k: {str(kk): vv for kk, vv in v.items()} for k, v in value_labels_by_var.items()}, f, ensure_ascii=False, indent=2)
