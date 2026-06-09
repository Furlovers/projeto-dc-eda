# Projeto I EDA — Entrega

Este repositório contém os arquivos para as duas partes do Projeto I de EDA.

## Sumário das entregas

### Notebook completo

- Notebook único com as duas partes: [`notebooks/Projeto_I_EDA_Completo.ipynb`](notebooks/Projeto_I_EDA_Completo.ipynb)

### Parte A — Pesquisas de opinião

- Notebook: [`notebooks/Projeto_I_EDA_Parte_A_Opiniao_CESOP.ipynb`](notebooks/Projeto_I_EDA_Parte_A_Opiniao_CESOP.ipynb)
- Microdados tratados: [`data/processed/cesop_04829_microdados.csv`](data/processed/cesop_04829_microdados.csv)
- Dicionário de variáveis: [`data/processed/cesop_04829_codebook.csv`](data/processed/cesop_04829_codebook.csv)
- Rótulos de valores: [`data/processed/cesop_04829_value_labels.json`](data/processed/cesop_04829_value_labels.json)
- Dados brutos fornecidos: [`data/raw/04829.SAV`](data/raw/04829.SAV), [`data/raw/quest_04829.pdf`](data/raw/quest_04829.pdf), [`data/raw/TF_04829.pdf`](data/raw/TF_04829.pdf)
- Base pública correlacionada: [`data/external/ibge_censo2022_raca_uf.csv`](data/external/ibge_censo2022_raca_uf.csv)

### Parte B — Séries temporais

- Notebook: [`notebooks/Projeto_I_EDA_Parte_B_Series_Inadimplencia.ipynb`](notebooks/Projeto_I_EDA_Parte_B_Series_Inadimplencia.ipynb)
- Série principal e indicadores já alinhados: [`data/external/bcb_inadimplencia_indicadores_wide.csv`](data/external/bcb_inadimplencia_indicadores_wide.csv)
- Fontes SGS usadas: [`data/external/bcb_sgs_sources.csv`](data/external/bcb_sgs_sources.csv)
- Dados brutos BCB: [`data/raw/bcb_21084.csv`](data/raw/bcb_21084.csv), [`data/raw/bcb_4390.csv`](data/raw/bcb_4390.csv), [`data/raw/bcb_433.csv`](data/raw/bcb_433.csv)

### Texto do trabalho

- Texto em Markdown: [`TEXTO_TRABALHO.md`](TEXTO_TRABALHO.md)
- O mesmo conteúdo interpretativo também está incorporado nos notebooks, nas seções de Introdução, Métodos, Discussão e Conclusão.

## Como executar no Google Colab

Os notebooks trazem uma célula inicial que detecta o ambiente: no Colab, ela baixa o projeto do GitHub; localmente, usa a própria pasta do projeto. Em ambos os casos, a pasta `data/` é localizada automaticamente.

1. Publique este projeto em um repositório no GitHub.
2. Abra um dos notebooks de `notebooks/` no Colab (Arquivo → Abrir notebook → aba GitHub, ou faça upload do `.ipynb`).
3. Na primeira célula, ajuste `REPO_URL` para o endereço do seu repositório:

```python
REPO_URL = "https://github.com/USUARIO-OU-ORG/projeto_i_eda.git"
```

4. Execute todas as células (Ambiente de execução → Executar tudo). No Colab, a célula roda `git clone` em `/content/projeto_i_eda` e carrega os dados de lá; localmente, o download é ignorado.

## Principais fontes de dados

- CESOP/IPEC 04829 — Pesquisa “Percepção dos brasileiros sobre o racismo no Brasil”.
- IBGE, Censo Demográfico 2022 — população por raça/cor, Brasil, regiões e UFs.
- Banco Central do Brasil, SGS:
  - 21084 — inadimplência da carteira de crédito, pessoas físicas, total;
  - 4390 — Selic acumulada no mês;
  - 433 — IPCA mensal.

## Observações metodológicas

- A Parte A usa os microdados sem ponderação, pois a base recebida não traz uma variável de peso amostral.
- Os testes estatísticos são exploratórios; associação não implica causalidade.
- A Parte B correlaciona séries mensais em níveis, variações e defasagens. Essas correlações devem ser interpretadas como hipóteses descritivas, não como efeito causal.
