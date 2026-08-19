import pandas as pd
import json

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def carregar_dados():
    transacoes = pd.read_csv(DATA_DIR / "transacoes.csv")
    historico = pd.read_csv(DATA_DIR / "historico_atendimento.csv")

    with open(DATA_DIR / "perfil_investidor.json", encoding="utf-8") as arquivo:
        perfil = json.load(arquivo)

    with open(DATA_DIR / "produtos_financeiros.json", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    return transacoes, historico, perfil, produtos

def gerar_resumo_financeiro(transacoes, perfil):
    total_receitas = transacoes.loc[
        transacoes["tipo"] == "entrada", "valor"
    ].sum()

    total_despesas = transacoes.loc[
        transacoes["tipo"] == "saida", "valor"
    ].sum()

    saldo_periodo = total_receitas - total_despesas

if __name__ == "__main__":
    transacoes, historico, perfil, produtos = carregar_dados()

    print(transacoes.head())
    print(perfil["nome"])
    print(produtos[0]["nome"])