# Norman — Assistente Financeiro

Norman é um assistente financeiro educativo feito com Python, Streamlit e uma LLM acessada pela OpenRouter. Ele usa dados fictícios para ajudar o usuário a entender gastos, acompanhar metas e conhecer produtos financeiros disponíveis.

> Os dados deste projeto são somente para demonstração. Norman não realiza investimentos, movimentações financeiras ou previsões de rendimento.

## O que o Norman faz

- Soma receitas, despesas e gastos por categoria.
- Mostra o andamento da reserva de emergência.
- Explica os produtos financeiros cadastrados que combinam com o perfil apresentado.
- Responde somente com as informações disponíveis nos arquivos do projeto.
- Informa quando não há dados suficientes para responder com segurança.

## Como funciona

1. O usuário envia uma pergunta pelo chat.
2. A aplicação lê os dados fictícios da pasta `data/`.
3. O Norman calcula o resumo financeiro e monta um contexto com perfil, metas, gastos e produtos.
4. Esse contexto, junto das regras de segurança, é enviado ao modelo escolhido na OpenRouter.
5. A resposta é exibida no chat.

## Dados utilizados

| Arquivo | Conteúdo |
| --- | --- |
| `data/transacoes.csv` | Entradas e saídas financeiras. |
| `data/perfil_investidor.json` | Perfil, renda, metas e reserva de emergência. |
| `data/produtos_financeiros.json` | Produtos que o Norman pode apresentar. |
| `data/historico_atendimento.csv` | Histórico fictício de atendimentos. |

## Como executar

É necessário ter Python 3 instalado e uma chave de API da [OpenRouter](https://openrouter.ai/).

```bash
# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv .venv
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie a aplicação
streamlit run src/app.py
```

Ao abrir a página no navegador, informe sua chave da OpenRouter na barra lateral. A chave é usada somente durante a sessão e não deve ser adicionada ao repositório.

## Perguntas para testar

- `Quanto gastei com alimentação?`
- `Quanto falta para a minha reserva de emergência?`
- `Quais produtos disponíveis combinam com o meu perfil?`
- `Qual será a Selic daqui a seis meses?`

Na última pergunta, o comportamento esperado é informar que a base não possui dados para previsão.

## Estrutura

```text
src/
  app.py       Interface do chat em Streamlit
  agente.py    Leitura dos dados, cálculos e chamada ao modelo
  config.py    Configurações do modelo e da OpenRouter
data/          Dados fictícios usados pelo agente
docs/          Documentação complementar do Norman
requirements.txt
```

## Limitações

- A base contém dados fictícios e limitados a um cenário de demonstração.
- As respostas dependem da disponibilidade da OpenRouter e do modelo selecionado.
- O Norman não substitui orientação profissional financeira.
