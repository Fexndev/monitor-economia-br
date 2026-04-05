"""
Coleta cotações de moedas via API PTAX do Banco Central.
USD, EUR e GBP → salva em data/moedas.json
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT = DATA_DIR / "moedas.json"

# USD usa endpoint específico, EUR/GBP usam o genérico
PTAX_USD = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@di,dataFinalCotacao=@df)"
    "?@di='{di}'&@df='{df}'&$format=json&$orderby=dataHoraCotacao asc"
)

PTAX_MOEDA = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@di,dataFinalCotacao=@df)"
    "?@moeda='{moeda}'&@di='{di}'&@df='{df}'&$format=json&$orderby=dataHoraCotacao asc"
)

MOEDAS = {
    "usd": {"nome": "Dólar (USD)", "codigo": None},  # endpoint próprio
    "eur": {"nome": "Euro (EUR)", "codigo": "EUR"},
    "gbp": {"nome": "Libra (GBP)", "codigo": "GBP"},
    "chf": {"nome": "Franco Suíço (CHF)", "codigo": "CHF"},
    "cad": {"nome": "Dólar Can. (CAD)", "codigo": "CAD"},
}


def fetch_usd(di, df):
    url = PTAX_USD.format(di=di, df=df)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()["value"]


def fetch_moeda(codigo, di, df):
    url = PTAX_MOEDA.format(moeda=codigo, di=di, df=df)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()["value"]


def one_per_day(records):
    by_day = {}
    for r in records:
        dt = r["dataHoraCotacao"][:10]
        by_day[dt] = r
    return [by_day[k] for k in sorted(by_day)]


def process_currency(raw_records):
    """Processa registros brutos em histórico diário e mensal."""
    daily = one_per_day(raw_records)

    history = []
    for r in daily:
        history.append({
            "data": r["dataHoraCotacao"][:10],
            "venda": round(r["cotacaoVenda"], 4),
        })

    # Agregar mensal (fechamento do mês)
    by_month = {}
    for h in history:
        mes = h["data"][:7]
        by_month[mes] = h["venda"]

    monthly = [{"data": m, "valor": v} for m, v in sorted(by_month.items())]

    current = history[-1] if history else None

    # Variações
    variations = {}
    if len(history) >= 2:
        cur = history[-1]["venda"]
        prev = history[-2]["venda"]
        variations["day"] = round((cur - prev) / prev * 100, 2)

    return {
        "current": {"cotacao_venda": current["venda"], "data": current["data"]} if current else None,
        "variations": variations,
        "monthly": monthly,
    }


def main():
    today = datetime.now()
    di = "01-01-2020"
    df = today.strftime("%m-%d-%Y")

    result = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "BCB/PTAX",
    }

    for key, cfg in MOEDAS.items():
        print(f"Buscando {cfg['nome']}...")
        try:
            if cfg["codigo"] is None:
                raw = fetch_usd(di, df)
            else:
                raw = fetch_moeda(cfg["codigo"], di, df)
            print(f"  {len(raw)} registros brutos")
            result[key] = process_currency(raw)
            result[key]["nome"] = cfg["nome"]
            print(f"  {len(result[key]['monthly'])} meses")
        except Exception as e:
            print(f"  ERRO: {e}")
            result[key] = {"nome": cfg["nome"], "current": None, "variations": {}, "monthly": []}

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Salvo em {OUTPUT}")


if __name__ == "__main__":
    main()
