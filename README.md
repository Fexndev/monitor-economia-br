# Monitor Economia BR

Dashboard interativo de indicadores econômicos brasileiros com atualização automática diária via GitHub Actions.

**[Acessar o Dashboard](https://fexndev.github.io/monitor-economia-br/)**

## Indicadores

| Grupo | Métricas disponíveis |
|---|---|
| **Câmbio** | USD/BRL, EUR/BRL, GBP/BRL, CHF/BRL, CAD/BRL |
| **Selic** | Meta (COPOM), Efetiva (realizada) |
| **CDI** | Taxa diária (a.a.), Acum. ano, Acum. 12 meses |
| **IPCA** | Variação mensal, Acum. ano, Acum. 12 meses |
| **IGP-M** | Variação mensal, Acum. ano, Acum. 12 meses |
| **INPC** | Variação mensal, Acum. ano, Acum. 12 meses |
| **Poupança** | Rendimento mensal, Acum. ano, Acum. 12 meses |

Todos os indicadores são exibidos em um gráfico unificado com seleção dinâmica. Dados mensais a partir de janeiro/2024.

## Funcionalidades

- **Gráfico interativo** com múltiplos indicadores simultâneos e dois eixos (R$ e %)
- **Seletor por grupo** — ative/desative métricas de cada indicador independentemente
- **Eixo hierárquico** — meses agrupados por ano, distribuídos uniformemente
- **Rótulos de dados** com fundo destacado e ajuste automático conforme quantidade de séries
- **Tema claro/escuro** com persistência em localStorage
- **KPIs** resumidos no topo (Dólar, Selic, IPCA, CDI)
- **Tooltip** multi-série ao passar o mouse
- **Atualização automática** de segunda a sexta às 18h BRT via GitHub Actions

## Fontes de dados

| Fonte | Indicadores |
|---|---|
| [BCB/PTAX](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos) | Cotações de moedas |
| [BCB/SGS](https://www3.bcb.gov.br/sgspub/) | Selic (séries 432, 11), CDI (12, 4391), IPCA (433, 13522), IGP-M (189), INPC (188, 11426), Poupança (25) |

## Tecnologias

- HTML, CSS, JavaScript (sem frameworks)
- Chart.js + chartjs-plugin-datalabels + plugin custom para eixo hierárquico
- Python (requests) para coleta de dados
- GitHub Actions (atualização automática)
- GitHub Pages (hospedagem)

## Como rodar localmente

```bash
# 1. Instalar dependências e coletar dados
pip install -r scripts/requirements.txt
cd scripts && python fetch_moedas.py && python fetch_selic.py && python fetch_cdi.py \
  && python fetch_ipca.py && python fetch_igpm.py && python fetch_inpc.py && python fetch_poupanca.py

# 2. Servir localmente
cd .. && python -m http.server 8000
# Abrir: http://localhost:8000
```

## Estrutura

```
├── .github/workflows/
│   └── update-data.yml          # Atualização diária automática
├── data/                        # JSONs gerados pelos scripts
│   ├── moedas.json              # USD, EUR, GBP, CHF, CAD
│   ├── selic.json               # Meta + Efetiva
│   ├── cdi.json                 # Taxa, acum. ano, acum. 12m
│   ├── ipca.json                # Mensal, acum. ano, acum. 12m
│   ├── igpm.json                # Mensal, acum. ano, acum. 12m
│   ├── inpc.json                # Mensal, acum. ano, acum. 12m
│   └── poupanca.json            # Mensal, acum. ano, acum. 12m
├── scripts/
│   ├── utils.py                 # Funções compartilhadas (fetch SGS, composição)
│   ├── fetch_moedas.py          # Cotações PTAX (5 moedas)
│   ├── fetch_selic.py           # Séries 432 + 11
│   ├── fetch_cdi.py             # Séries 12 + 4391
│   ├── fetch_ipca.py            # Séries 433 + 13522
│   ├── fetch_igpm.py            # Série 189
│   ├── fetch_inpc.py            # Séries 188 + 11426
│   ├── fetch_poupanca.py        # Série 25
│   └── requirements.txt
├── index.html
├── styles.css
├── app.js
└── manifest.json
```
