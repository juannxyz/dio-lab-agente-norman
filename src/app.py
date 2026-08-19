import streamlit as st

from agente import responder
from config import MODEL_NAME

st.set_page_config(page_title="Norman", page_icon="💼")

st.title("💼 Norman — Assistente Financeiro Inteligente")
st.caption(
    "Norman consulta os dados fictícios do projeto para responder sobre gastos, "
    "metas e produtos financeiros."
)

with st.sidebar:
    st.header("Configuração da sessão")
    api_key = st.text_input(
        "Chave da OpenRouter",
        type="password",
        help="A chave é usada somente nesta sessão e não é salva em arquivo pelo aplicativo.",
    )
    modelo = st.text_input("Modelo", value=MODEL_NAME)
    st.caption(
        "Para testar gratuitamente, use o modelo Llama sugerido. "
        "Modelos gratuitos podem ter limites ou ficar indisponíveis."
    )

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": (
                "Olá, eu sou Norman. Posso ajudar a analisar os dados financeiros "
                "fictícios deste projeto."
            ),
        }
    ]

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Ex.: Quanto gastei com alimentação?")

if pergunta:
    if not api_key:
        st.warning("Informe sua chave da OpenRouter na barra lateral antes de enviar uma pergunta.")
        st.stop()

    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Norman está analisando os dados..."):
            resposta = responder(pergunta, api_key, modelo)
        st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
