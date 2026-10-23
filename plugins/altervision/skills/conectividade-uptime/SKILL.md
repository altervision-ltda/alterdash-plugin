---
name: conectividade-uptime
description: Analisa a conectividade e o uptime das câmeras de contagem AlterVision por loja e por dia usando o MCP AlterVision — ranking de lojas, dias e horários sem dado, quanto do fluxo foi estimado e quais números ficam pouco confiáveis. Use quando o usuário perguntar sobre uptime, câmera offline, loja sem dado, conectividade, contagem falhando, fluxo zerado ou estranho, ou se pode confiar nos números de uma loja ou período.
---

# Análise de conectividade e uptime

Mostra quais lojas e dias tiveram câmera fora do ar, quanto isso afetou o fluxo e a conversão e o
que fazer. Escrita e visual seguem `../relatorio-pdf/references/identidade-visual.md`.

## O que o MCP mostra e o que não mostra

- **Mostra:** uptime médio por loja e uptime por dia (`conversion_rate_per_date`), horas sem fluxo
  medido (`get_flow_per_hour`), e a diferença entre fluxo medido e ajustado
  (`get_metrics_from_stores`), que é a parte do fluxo estimada por falha de contagem.
- **Não mostra:** qual câmera caiu, o motivo (energia, rede, equipamento) nem o status ao vivo.
  Não chute a causa. Para isso, o caminho é o suporte AlterVision ou o painel administrativo.

## 1. Período e lojas

Sem período informado, use os últimos 30 dias até ontem. `get_stores` para resolver nomes; sem
lojas citadas, analise todas.

## 2. Buscar os dados

Em paralelo:

1. `conversion_rate_per_date` com `includeDetails`: `average_uptime_percent` por loja e
   `camera_uptime_percent` por dia.
2. `get_metrics_from_stores` no mesmo período: compare os pares `...Measured` × `...Adjusted` de
   fluxo. **Parcela estimada** = (ajustado − medido) ÷ ajustado.

Depois, para os piores dias (até 5 por loja, uptime mais baixo), chame `get_flow_per_hour` com
`includeDetails` e liste as horas do horário de funcionamento que vieram sem fluxo. Isso mostra se a
falha foi o dia todo, um trecho (ex.: abertura) ou horas soltas.

## 3. Classificar

Faixas padrão (diga ao usuário que são as usadas na análise):

| Uptime | Status | Leitura |
| --- | --- | --- |
| 98% ou mais | ok | Números confiáveis |
| 95% a 98% | atencao | Confiável no mês, conferir dias isolados |
| abaixo de 95% | ruim | Fluxo e conversão do período precisam de ressalva |

Procure padrões:

- **Dias seguidos** abaixo de 95%: provável problema contínuo que ainda não foi resolvido.
- **Mesmo dia da semana ou mesmo horário** recorrente: algo de rotina da loja (desligamento de
  energia, roteador, limpeza).
- **Loja inteira zerada** num dia com vendas: câmera ou rede fora, não falta de cliente.
- **Queda de uptime junto com salto de conversão:** a conversão está inflada porque o fluxo foi
  subcontado. Avise antes que alguém comemore.

## 4. Impacto nos números

Para cada loja em `atencao` ou `ruim`, diga o que fica comprometido: fluxo e TC dos dias afetados,
comparações com o mês anterior, ranking em corridas de conversão. Se o fluxo ajustado está ativo,
explique que os números exibidos já incluem estimativa e qual parcela é estimada.

## 5. Entregar

No chat:

1. **Conclusão em uma frase:** "11 de 12 lojas ficaram acima de 98% de uptime; a Loja Norte ficou
   em 86%, com câmera fora de 12/10 a 15/10 e 9% do fluxo do mês estimado."
2. **Ranking** do pior para o melhor: loja · uptime médio · dias abaixo de 95% · parcela estimada ·
   status.
3. **Detalhe das lojas críticas:** dias e horas sem dado, padrão encontrado.
4. **Ação:** o que fazer, quem faz e quanto vale. Ex.: "Abrir chamado no suporte AlterVision para a
   Loja Norte com os dias 12/10 a 15/10 · gerente da loja"; "Conferir se o roteador fica ligado
   depois do fechamento · gerente"; "Usar fluxo ajustado no fechamento de outubro da Loja Norte ·
   diretoria". Se não houver valor para estimar, escreva "sem dado".

Ofereça o PDF pela skill `relatorio-pdf`: cartões (uptime médio da rede, lojas em atenção, lojas
críticas, parcela estimada), resumo, tabela com status por loja, barras com a variação do uptime
contra o período anterior e a seção de qualidade dos dados.
