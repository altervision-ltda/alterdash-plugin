---
name: plano-de-acao-meta
description: Monta um plano de ação para bater a meta de uma loja ou da rede usando o MCP AlterVision — mede quanto falta, projeta o fechamento, decompõe o gap em fluxo, conversão e ticket, encontra as alavancas (vendedores, horários, motivos de não-conversão, benchmark de mercado) e calcula quanto cada ação vale. Use quando o usuário perguntar como bater a meta, o que fazer para chegar na meta, por que está abaixo da meta, quanto falta, ou pedir um plano de ação.
---

# Plano de ação para bater a meta

Responde três perguntas, nesta ordem: **quanto falta**, **de onde pode vir** e **o que fazer, quem
faz e quanto vale**.

Escrita e visual seguem `../relatorio-pdf/references/identidade-visual.md`. Toda comparação diz
contra o quê; nada de número, meta ou nome inventado.

## 1. Quanto falta

1. `get_stores` para resolver as lojas citadas (sem citação, todas).
2. `metas_infos` do início do período da meta até hoje, com `includeDetails` e `includeSellers`.
   Pegue: meta, realizado, projeção de fechamento, faixas (multi-tier) e dias restantes.
3. Calcule:
   - **Gap** = meta − projeção (se a projeção já passa a meta, diga e mire a próxima faixa).
   - **Necessário por dia** = (meta − realizado) ÷ dias restantes, contra a média diária até agora.

Se não houver meta ativa no período, diga isso e pergunte qual valor o usuário quer perseguir.
Não crie meta.

## 2. De onde pode vir

Faturamento = fluxo × taxa de conversão × ticket médio. Busque em paralelo:

| Pergunta | Ferramenta |
| --- | --- |
| Fluxo, TC, ticket e PA do período e do mesmo período do mês anterior | `conversion_rate_per_date` (duas chamadas) |
| Atendimentos, atratividade, tempo de atendimento | `get_metrics_from_stores` |
| Dispersão entre vendedores | `get_metrics_from_sellers` |
| TC e fluxo contra o mercado (último mês fechado) | `market_data` |
| Motivos de não-conversão e receita perdida (últimos 30 dias) | `non_conversion_reasons_stats` com `includeSubclassifications` e `sellerIds: []` |
| O que o cliente pediu e não tinha (motivo principal) | `get_non_conversion_reasons_classifications_available` + `search_non_conversion_transcriptions` |
| Horários de pico | `get_flow_per_hour` com `responseType: "best_hours"` em 2–3 dias recentes |
| Corrida em andamento que pode servir de incentivo | `corridas_infos` |

Motivos de não-conversão e corridas só existem para lojas com AlterVez; se vier vazio, diga e siga.

Decomponha o gap: quanto de faturamento faltaria cobrir se só a conversão subisse, se só o ticket
subisse, se só o fluxo subisse. Use o fluxo esperado dos dias restantes (média por dia da semana
das últimas semanas).

## 3. Alavancas e quanto valem

Para cada alavanca, estime o valor com a conta explícita sobre os dias restantes:

- **Conversão dos vendedores abaixo da mediana.** Trazer os N vendedores abaixo da mediana para a
  mediana da loja: Δ TC × atendimentos esperados × ticket médio.
- **Motivos de não-conversão evitáveis.** Ruptura de estoque, falta de tamanho, forma de pagamento:
  receita perdida por semana (vem do `non_conversion_reasons_stats`) × semanas restantes × parcela
  recuperável (diga a premissa, ex.: 30%). Cite os produtos ou pedidos que mais aparecem nas
  transcrições.
- **Picos sem cobertura.** Se a conversão cai nos horários de maior fluxo, ganho de levar a TC do
  pico para a média do dia. Sugira a skill `escala-do-time` para redistribuir o time.
- **Ticket e PA.** Se PA ou ticket estão abaixo do mês anterior ou da mediana dos vendedores:
  +0,1 de PA × vendas esperadas × preço médio.
- **Benchmark.** Se a TC está abaixo da mediana do segmento em `market_data`, diga a distância em
  p.p. e o que ela vale.
- **Corrida.** Se não houver corrida ativa e a meta for de vendedores, sugira uma no KPI mais
  defasado.

Fluxo é a alavanca que a loja menos controla; trate ações de fluxo (vitrine, ação de rua) como
complemento e não como base do plano.

Some o valor das ações e compare com o gap. Se não fecha, diga com clareza quanto fica faltando.

## 4. Entregar

No chat, nesta ordem:

1. **Conclusão em uma frase:** "A Loja Centro projeta 91% da meta; faltam R$ 42 mil em 9 dias, ou
   R$ 4,7 mil por dia acima da média atual."
2. **Ponte do gap:** o que somou e o que tirou contra o mês anterior (fluxo, TC, ticket).
3. **Plano de ação** em tabela: o que fazer · quem faz · até quando · quanto vale · como medir.
   No máximo 5 ações, ordenadas por valor.
4. **Acompanhamento diário:** a meta do dia e os indicadores a olhar (TC do dia, PA, vendas no pico).
5. **Qualidade dos dados:** uptime abaixo de 95% em algum dia, lojas sem integração de vendas,
   premissas usadas.

Ofereça o PDF pela skill `relatorio-pdf`: cartões (meta, projeção, gap, necessário por dia), resumo,
barras divergentes da ponte, tabela de vendedores com meta em rosa sob o valor, quadro de ação e
qualidade dos dados.
