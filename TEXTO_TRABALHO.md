# Texto do trabalho — Projeto I EDA

## Parte A — Pesquisa de opinião CESOP/IPEC 04829

### Introdução

Nesta parte analisamos a pesquisa CESOP/IPEC 04829, sobre a percepção dos brasileiros a respeito do racismo. O levantamento foi feito entre 14 e 18 de abril de 2023, com 2.000 entrevistas e universo de eleitores de 16 anos ou mais. O questionário cobre raça/cor/etnia, experiências de racismo, racismo ambiental, escola, segurança pública, representatividade, cotas e ações afirmativas, acessibilidade, religião, renda e perfil sociodemográfico.

Organizamos a análise em torno de cinco perguntas: qual dimensão é mais apontada como geradora de desigualdades; se a percepção de que o Brasil é racista vem acompanhada de relatos pessoais ou indiretos; se o relato de ter sofrido racismo varia por raça/cor; como o apoio a cotas se distribui por raça/cor e por posicionamento político; e se a composição racial da amostra se aproxima da do Censo. Para atender à exigência de correlação com uma base pública, comparamos a composição racial da amostra com a distribuição da população por raça/cor no Censo Demográfico 2022 do IBGE. A comparação serve para situar a amostra diante de uma referência nacional, e não para corrigir seus pesos.

### Métodos

A análise é exploratória e descritiva. Trabalhamos com tabelas de frequência, gráficos de barras e cruzamentos entre variáveis categóricas. Para medir a associação entre pares de variáveis nominais, aplicamos o teste qui-quadrado de independência e o V de Cramér, que resume a força dessa associação.

Os microdados vieram em formato SPSS (.SAV) e foram convertidos para CSV por um leitor próprio, em `src/spss_sav_minimal_reader.py`, preservando os rótulos de variáveis e de valores. Nas frequências gerais mantivemos as respostas "não sabe" e "não respondeu"; já nos cruzamentos por grupo e nos testes trabalhamos apenas com as respostas substantivas, para não diluir os percentuais. A base não traz variável de peso amostral, então os resultados são calculados sem ponderação. As conclusões são associativas, não causais.

### Resultados

**Perfil da amostra.** A composição racial da amostra é próxima da do Censo 2022: brancos somam 44,6% (43,5% no Censo) e pardos 43,8% (45,3%), com pretos em 10,5% (10,2%). Amarelos e indígenas somam cerca de 1% da amostra, o que recomenda cautela em qualquer cruzamento que dependa dessas categorias. Por isso a comparação com o Censo entra como contexto demográfico, não como reponderação.

**Percepção do racismo.** Raça/cor/etnia foi o fator mais citado como gerador de desigualdades (44,1%), à frente de classe social (29,0%). A concordância de que o Brasil é racista chega a 80,9%, e as afirmações sobre atuação policial têm adesão alta: 84,0% concordam que brancos e negros são tratados de forma diferente pelas polícias, 87,9% que pessoas negras são mais criminalizadas e 79,0% que a abordagem policial se baseia em cor, cabelo e vestimenta.

**Experiência por raça/cor.** O relato de já ter sofrido racismo é de 23,3% no conjunto da amostra, mas varia muito por raça/cor entre as respostas substantivas: 16,3% entre brancos, 24,8% entre pardos e 50,0% entre pretos. O teste qui-quadrado indica diferença estatisticamente relevante (p < 0,001) e o V de Cramér é de 0,240, a associação mais forte desta parte.

**Cotas raciais.** O apoio a cotas em universidades é majoritário (76,2% entre respostas válidas) e se divide sobretudo por política: 89,0% à esquerda, 80,2% no centro e 66,1% à direita. Por raça/cor, o apoio é semelhante entre os grupos (de 74% a 78%), com V de Cramér de 0,046 (não significativo).

**Racismo ambiental.** A expressão "racismo ambiental" ainda é pouco reconhecida, com a maioria dizendo não conhecê-la, enquanto a demanda por ação pública contra desigualdades aparece de forma ampla.

### Discussão e conclusão

Três achados se destacam. Primeiro, o racismo é reconhecido como problema estrutural por boa parte dos entrevistados, com raça/cor/etnia liderando como fator de desigualdade e adesão acima de 80% às afirmações sobre tratamento policial desigual. Segundo, a experiência direta de racismo é socialmente desigual: ela salta de 16,3% entre brancos para 50,0% entre pretos, e o V de Cramér de 0,240 mostra que essa diferença não é ruído amostral. Terceiro, o apoio a cotas é majoritário, mas se organiza pela clivagem ideológica (de 66,1% à direita a 89,0% à esquerda) muito mais do que pela raça/cor de quem responde.

Em resumo, a opinião pública reconhece amplamente o racismo como problema do país, mas a vivência pessoal é desigual entre grupos raciais, mais frequente entre pretos e pardos. As cotas têm apoio majoritário, ainda que dividido por posicionamento político. Como próximos passos, valeria aplicar pesos amostrais (caso a base os disponibilize), estimar intervalos de confiança para os subgrupos menores e comparar estes resultados com pesquisas anteriores sobre racismo e ações afirmativas, para enxergar a tendência no tempo.

## Parte B — Séries temporais de inadimplência

### Introdução

Nesta parte acompanhamos a evolução mensal da inadimplência de pessoas físicas no Brasil. A série principal é a SGS 21084 do Banco Central, que mede o percentual da carteira de crédito com alguma parcela em atraso há mais de 90 dias. É um indicador sensível à saúde financeira das famílias e aos ciclos de crédito e de juros.

Para entender o que acompanha esse movimento, correlacionamos a inadimplência com dois indicadores públicos: a Selic acumulada no mês (SGS 4390), que aproxima o custo do dinheiro, e o IPCA mensal (SGS 433), que aproxima a pressão da inflação sobre o orçamento das famílias. O período coberto começa em março de 2011, primeiro mês em que as três séries estão disponíveis em conjunto.

### Métodos

Coletamos as três séries no Sistema Gerenciador de Séries Temporais (SGS) do Banco Central, padronizamos para frequência mensal e unimos pela data. Sobre essa base, fizemos: o gráfico da série com média móvel de 12 meses, para separar a tendência das oscilações de curto prazo; as médias anuais das três séries; a matriz de correlação em nível e em variação mensal; as correlações com defasagem de 0 a 12 meses, já que o efeito de juros e inflação sobre o atraso de crédito não é imediato; e uma regressão linear exploratória com os indicadores defasados.

Tratamos tudo como descritivo. Correlação não é causa: séries macroeconômicas têm tendência, sazonalidade e quebras de regime, e dependem de fatores que não entram aqui, como desemprego, renda, oferta de crédito e renegociações de dívidas.

### Resultados e discussão

A série vai de 4,62% em março de 2011 a 5,24% em fevereiro de 2026, com mínimo de 2,84% em dezembro de 2020 (auge da pandemia, com juros baixos e crédito reorganizado) e máximo de 5,51% em maio de 2012. A partir de 2022 ela se desloca para um patamar mais alto, acompanhando o ciclo de Selic elevada.

Nas correlações em nível, a inadimplência anda junto com a Selic (0,41) e tem relação fraca e negativa com o IPCA (-0,14). Em variação mensal as correlações encolhem, o que reforça a cautela. O resultado mais interessante aparece nas defasagens: a Selic de 7 meses atrás se correlaciona 0,55 com a inadimplência de hoje, mais do que a Selic do mês corrente. Isso é coerente com o funcionamento do crédito, em que o aperto de juros leva meses para virar atraso acima de 90 dias. Para o IPCA, mesmo a melhor defasagem (12 meses) fica baixa, em 0,12.

A regressão exploratória resume esse quadro: com a Selic defasada em 7 meses e o IPCA em 12, o modelo explica cerca de 31% da variância (R² = 0,308); a Selic defasada é fortemente significativa (p < 0,001) e o IPCA não (p = 0,72). Vale registrar uma limitação: o Durbin-Watson de 0,07 indica forte autocorrelação dos resíduos, esperada em séries em nível, o que reforça que o modelo é apenas descritivo.

### Conclusão

A inadimplência de pessoas físicas não se move sozinha nem reage a choques de um mês para o outro: ela tem ciclos longos e responde, com defasagem, às condições de juros. Entre os dois indicadores, a Selic é o que mostra associação mais clara; o IPCA, isolado, diz pouco. O passo seguinte natural seria incorporar desemprego, massa de rendimentos, comprometimento de renda das famílias, saldo da carteira de crédito e renegociações, para testar explicações mais completas do que a leitura apenas por juros e inflação.
