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

    gastor_por_categoria = (
        transacoes[transacoes["tipo"] == "saida"].groupby("categoria")["valor"].sum().to_dict()
    )

    gasto_alimentacao = gastor_por_categoria.get("alimentacao", 0)

    meta_reserva = next(
        meta
        for meta in perfil["metas"]
        if meta["meta"] == "Completar reserva de emergência"
    )

    falta_para_reserva = (
        meta_reserva["valor_necessario"] - perfil["reserva_emergencia_atual"]
    )

    return{
        "receitas": total_receitas,
        "despesas": total_despesas,
        "saldo_periodo": saldo_periodo,
        "gastos_por_categoria": gastor_por_categoria,
        "gasto_alimentacao": gasto_alimentacao,
        "reserva_atual": perfil["reserva_emergencia_atual"], 
        "meta_reserva": meta_reserva["valor_necessario"],
        "falta_para_reserva": falta_para_reserva
    }


if __name__ == "__main__":
    transacoes, historico, perfil, produtos = carregar_dados()
    resumo = gerar_resumo_financeiro(transacoes, perfil)

    print(resumo)