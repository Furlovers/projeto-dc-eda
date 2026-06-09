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

Cada notebook tem uma célula inicial que, no Colab, baixa este repositório com `git clone` e localiza a pasta `data/` automaticamente. Em execução local, o download é ignorado e usa-se a própria pasta do projeto. O `REPO_URL` já vem configurado para este repositório.

Abra direto no Colab e use "Ambiente de execução → Executar tudo":

- Notebook completo: https://colab.research.google.com/github/Furlovers/projeto-dc-eda/blob/main/notebooks/Projeto_I_EDA_Completo.ipynb
- Parte A — Opinião CESOP: https://colab.research.google.com/github/Furlovers/projeto-dc-eda/blob/main/notebooks/Projeto_I_EDA_Parte_A_Opiniao_CESOP.ipynb
- Parte B — Séries de inadimplência: https://colab.research.google.com/github/Furlovers/projeto-dc-eda/blob/main/notebooks/Projeto_I_EDA_Parte_B_Series_Inadimplencia.ipynb

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

## Referências

- CESOP/IPEC. Pesquisa 04829 — "Percepção dos brasileiros sobre o racismo no Brasil". Centro de Estudos de Opinião Pública (Cesop), Universidade Estadual de Campinas (Unicamp). Microdados e documentação técnica em `data/raw/`. Acervo: https://www.cesop.unicamp.br/
- IBGE — Instituto Brasileiro de Geografia e Estatística. Censo Demográfico 2022: população por cor ou raça. Rio de Janeiro, 2023. https://censo2022.ibge.gov.br/
- Banco Central do Brasil. Sistema Gerenciador de Séries Temporais (SGS). Séries 21084 (inadimplência da carteira de crédito — pessoas físicas — total), 4390 (Selic acumulada no mês) e 433 (IPCA mensal). https://www3.bcb.gov.br/sgspub/
- Ferramentas e bibliotecas: Python, pandas, NumPy, Matplotlib, SciPy (teste qui-quadrado) e statsmodels (regressão OLS).

## Declaração de uso de IA

Utilizamos ferramentas de inteligência artificial como apoio no desenvolvimento deste trabalho:

- Assistente de IA (Claude / Claude Code, da Anthropic): revisão e organização do código, verificação da execução dos notebooks, conferência dos resultados estatísticos e revisão da redação dos textos.
- _[Acrescente aqui outras ferramentas que o grupo utilizou — por exemplo ChatGPT ou GitHub Copilot — e em quê.]_

As decisões de análise, a escolha das bases, a interpretação dos resultados e a redação final foram revisadas e validadas pelos integrantes do grupo. As ferramentas de IA não foram usadas para gerar nem alterar dados: todos os dados provêm das fontes públicas citadas nas Referências.
