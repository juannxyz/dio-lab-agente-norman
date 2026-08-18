# Base de Conhecimento

## Dados Utilizados

O Norman utiliza os quatro arquivos mockados da pasta `data/`. Eles representam o contexto do cliente e evitam que o agente responda com informações inventadas.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualiza dúvidas e atendimentos anteriores, como perguntas sobre CDB, Tesouro Selic e metas financeiras. |
| `perfil_investidor.json` | JSON | Informa características do cliente, como renda, perfil moderado, tolerância a risco, patrimônio e metas. |
| `produtos_financeiros.json` | JSON | Disponibiliza os produtos que Norman pode explicar ou sugerir, com risco, rentabilidade informada e aporte mínimo. |
| `transacoes.csv` | CSV | Permite calcular receitas, despesas, categorias de gasto e a capacidade mensal de aporte do cliente. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Não. Nesta primeira versão, foram utilizados somente os dados mockados fornecidos pelo repositório. Essa decisão mantém o escopo do desafio, facilita os testes e evita o uso de informações financeiras reais ou sensíveis.

Em uma evolução futura, a base poderia receber mais meses de transações, metas adicionais e produtos financeiros atualizados, sempre com validação e consentimento do cliente.

---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos são carregados no início da sessão por uma pipeline em Python com Pandas e JSON. O código faz leituras separadas para CSV e JSON, calcula um resumo das transações e monta apenas o contexto necessário para a pergunta do usuário.

```python
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

transacoes = pd.read_csv(DATA_DIR / "transacoes.csv")
historico = pd.read_csv(DATA_DIR / "historico_atendimento.csv")

with open(DATA_DIR / "perfil_investidor.json", encoding="utf-8") as arquivo:
    perfil = json.load(arquivo)

with open(DATA_DIR / "produtos_financeiros.json", encoding="utf-8") as arquivo:
    produtos = json.load(arquivo)

receitas = transacoes.loc[transacoes["tipo"] == "entrada", "valor"].sum()
despesas = transacoes.loc[transacoes["tipo"] == "saida", "valor"].sum()
saldo_do_periodo = receitas - despesas
```

Os dados não precisam ser enviados integralmente à LLM em toda interação. Norman consulta e resume as partes relevantes: por exemplo, usa as transações para perguntas sobre gastos e o perfil com os produtos cadastrados para perguntas sobre objetivos ou investimentos.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

O system prompt contém apenas as regras fixas de comportamento e segurança do Norman. Os dados do cliente são consultados dinamicamente e enviados como um bloco de contexto junto da pergunta. Assim, o agente recebe informações atualizadas e reduz o risco de expor conteúdo desnecessário ou ultrapassar o limite de contexto.

```text
Você é Norman, um agente financeiro educativo. Responda apenas com base nos dados de contexto. Se a informação não estiver disponível, diga isso claramente. Não prometa rentabilidade e não substitua orientação profissional.

CONTEXTO DO CLIENTE:
- Nome: João Silva
- Perfil: moderado; aceita risco: não
- Renda mensal: R$ 5.000,00
- Objetivo principal: construir reserva de emergência
- Reserva atual: R$ 10.000,00 de R$ 15.000,00

RESUMO DAS TRANSAÇÕES DE OUTUBRO/2025:
- Receitas: R$ 5.000,00
- Despesas: R$ 2.488,90
- Saldo do período: R$ 2.511,10
- Maiores categorias de despesa: moradia (R$ 1.380,00) e alimentação (R$ 570,00)

PRODUTOS DISPONÍVEIS COMPATÍVEIS:
- Tesouro Selic: baixo risco; indicado para reserva de emergência.
- CDB com Liquidez Diária: baixo risco; indicado para segurança com rendimento diário.

PERGUNTA DO CLIENTE:
{pergunta_do_usuario}
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Renda mensal: R$ 5.000,00
- Objetivo: Completar a reserva de emergência
- Reserva atual: R$ 10.000,00 de R$ 15.000,00

Resumo de outubro/2025:
- Receitas: R$ 5.000,00
- Despesas: R$ 2.488,90
- Saldo do período: R$ 2.511,10
- Maiores gastos: Moradia (R$ 1.380,00) e Alimentação (R$ 570,00)

Produtos relevantes:
- Tesouro Selic: baixo risco e indicado para reserva de emergência.
- CDB com Liquidez Diária: baixo risco e rendimento diário.

Pergunta: "Quanto falta para minha reserva de emergência e quais opções disponíveis combinam com meu perfil?"
```
