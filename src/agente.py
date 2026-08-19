import json

from pathlib import Path
from openai import OpenAI
import pandas as pd

from config import MODEL_NAME, OPENROUTER_BASE_URL, TEMPERATURE

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SYSTEM_PROMPT = """
Você é Norman, um agente financeiro inteligente especializado em soluções financeiras educativas.
Seja formal, atencioso, respeitoso, analítico e inclusivo.

Responda somente com base nos dados de contexto fornecidos pela aplicação.
Não invente valores, saldos, taxas, previsões, produtos ou informações ausentes.
Não prometa rentabilidade ou resultados financeiros futuros.
Quando não houver dados suficientes, diga que não é possível responder com segurança
e informe qual dado está faltando. Você não executa investimentos nem movimentações financeiras.
""".strip()

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

    gastos_por_categoria = (
        transacoes[transacoes["tipo"] == "saida"]
        .groupby("categoria")["valor"]
        .sum()
        .to_dict()
    )

    gasto_alimentacao = gastos_por_categoria.get("alimentacao", 0)

    meta_reserva = next(
        meta
        for meta in perfil["metas"]
        if meta["meta"] == "Completar reserva de emergência"
    )

    falta_para_reserva = (
        meta_reserva["valor_necessario"] - perfil["reserva_emergencia_atual"]
    )

    return {
        "receitas": total_receitas,
        "despesas": total_despesas,
        "saldo_periodo": saldo_periodo,
        "gastos_por_categoria": gastos_por_categoria,
        "gasto_alimentacao": gasto_alimentacao,
        "reserva_atual": perfil["reserva_emergencia_atual"],
        "meta_reserva": meta_reserva["valor_necessario"],
        "falta_para_reserva": falta_para_reserva,
    }


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def montar_contexto(perfil, produtos, resumo, pergunta):
    produtos_formatados = "\n".join(
        f"- {produto['nome']}: risco {produto['risco']}; "
        f"aporte mínimo de {formatar_moeda(produto['aporte_minimo'])}; "
        f"indicado para {produto['indicado_para']}."
        for produto in produtos
    )

    categorias_formatadas = "\n".join(
        f"- {categoria}: {formatar_moeda(valor)}"
        for categoria, valor in resumo["gastos_por_categoria"].items()
    )

    return f"""
CONTEXTO DO CLIENTE:
- Nome: {perfil['nome']}
- Perfil de investidor: {perfil['perfil_investidor']}
- Aceita risco: {'sim' if perfil['aceita_risco'] else 'não'}
- Renda mensal: {formatar_moeda(perfil['renda_mensal'])}
- Patrimônio total: {formatar_moeda(perfil['patrimonio_total'])}
- Objetivo principal: {perfil['objetivo_principal']}
- Reserva atual: {formatar_moeda(resumo['reserva_atual'])}
- Meta da reserva: {formatar_moeda(resumo['meta_reserva'])}
- Falta para a reserva: {formatar_moeda(resumo['falta_para_reserva'])}

RESUMO DAS TRANSAÇÕES:
- Receitas: {formatar_moeda(resumo['receitas'])}
- Despesas: {formatar_moeda(resumo['despesas'])}
- Saldo do período: {formatar_moeda(resumo['saldo_periodo'])}
- Alimentação: {formatar_moeda(resumo['gasto_alimentacao'])}

GASTOS POR CATEGORIA:
{categorias_formatadas}

PRODUTOS DISPONÍVEIS:
{produtos_formatados}

PERGUNTA DO USUÁRIO:
{pergunta}
""".strip()


def responder(pergunta, api_key, modelo=MODEL_NAME):
    if not api_key:
        return (
            "Informe uma chave da OpenRouter para consultar o Norman. "
            "A chave é usada somente durante esta sessão."
        )

    transacoes, _, perfil, produtos = carregar_dados()
    resumo = gerar_resumo_financeiro(transacoes, perfil)
    contexto = montar_contexto(perfil, produtos, resumo, pergunta)

    try:
        cliente = OpenAI(api_key=api_key, base_url=OPENROUTER_BASE_URL)
        resposta = cliente.chat.completions.create(
            model=modelo,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": contexto},
            ],
        )
        return resposta.choices[0].message.content
    except Exception:
        return (
            "Não foi possível consultar o modelo neste momento. "
            "Verifique sua conexão, a chave da OpenRouter e o nome do modelo configurado."
        )


if __name__ == "__main__":
    transacoes, historico, perfil, produtos = carregar_dados()
    resumo = gerar_resumo_financeiro(transacoes, perfil)

    print(resumo)
    print("\nResposta do Norman:")
    print("Execute o chat em Streamlit para informar sua chave da OpenRouter com segurança.")
