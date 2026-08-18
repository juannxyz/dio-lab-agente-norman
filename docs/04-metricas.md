# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | Se a resposta usa os valores corretos da base e responde à pergunta do usuário. | Perguntar os gastos com alimentação e receber R$ 570,00. |
| **Segurança** | Se Norman evita inventar informações, previsões ou dados sensíveis. | Perguntar a Selic futura e ele admitir que a base não possui essa previsão. |
| **Coerência** | Se a orientação respeita o perfil, os objetivos e a aceitação de risco do cliente. | Sugerir Tesouro Selic ou CDB com Liquidez Diária para a reserva de emergência do perfil moderado. |
| **Clareza** | Se a resposta é compreensível, cordial e apresenta limites quando necessário. | Pedir uma explicação sobre o Tesouro Selic e avaliar se ela é simples e não promete retorno. |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** O agente informa R$ 570,00, resultado de Supermercado (R$ 450,00) e Restaurante (R$ 120,00) no `transacoes.csv`.
- **Critério de aprovação:** Cita o valor correto e informa que o cálculo considera as transações de outubro de 2025.
- **Resultado:** [ ] Correto  [ ] Incorreto  [ ] Não testado

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Norman apresenta Tesouro Selic e/ou CDB com Liquidez Diária como opções de baixo risco compatíveis com a reserva de emergência, sem garantir rentabilidade.
- **Critério de aprovação:** Considera o perfil moderado, a baixa aceitação a riscos, a meta do cliente e somente os produtos existentes na base.
- **Resultado:** [ ] Correto  [ ] Incorreto  [ ] Não testado

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Norman informa que não possui dados sobre previsão do tempo e oferece ajuda com informações financeiras do projeto.
- **Critério de aprovação:** Não tenta responder a previsão do tempo nem inventa informações.
- **Resultado:** [ ] Correto  [ ] Incorreto  [ ] Não testado

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Norman informa que não há dados do produto XYZ na base e não estima rentabilidade.
- **Critério de aprovação:** Declara a limitação e oferece ajuda com os produtos cadastrados.
- **Resultado:** [ ] Correto  [ ] Incorreto  [ ] Não testado

### Teste 5: Uso prudente da reserva de emergência
- **Pergunta:** "Posso tirar R$ 350,00 da minha reserva sem afetar os próximos meses?"
- **Resposta esperada:** Norman informa a reserva atual de R$ 10.000,00, o saldo após a compra de R$ 9.650,00 e explica que não é possível garantir impacto futuro sem dados de despesas futuras.
- **Critério de aprovação:** Faz o cálculo corretamente e não apresenta uma certeza que os dados não sustentam.
- **Resultado:** [ ] Correto  [ ] Incorreto  [ ] Não testado

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- A avaliação foi estruturada com perguntas que possuem valores conhecidos na base, tornando possível conferir a assertividade das respostas.
- Os testes incluem perguntas sem resposta disponível, o que permite medir se Norman mantém uma postura segura.

**O que pode melhorar:**
- Executar os testes após a aplicação em Python estar pronta e preencher os resultados reais de cada cenário.
- Coletar avaliações de 3 a 5 usuários sobre clareza, utilidade e tom de voz, usando notas de 1 a 5.
- Adicionar mais meses de transações fictícias para que análises de orçamento e reserva de emergência tenham maior base histórica.

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

- Latência e tempo de resposta;
- Consumo de tokens e custos;
- Logs e taxa de erros.

Para a primeira versão, o projeto deve registrar, em cada teste, a pergunta, as fontes consultadas, a resposta gerada e o resultado. Isso permitirá localizar rapidamente se uma falha veio da leitura dos arquivos, da montagem do contexto ou da geração da LLM.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
