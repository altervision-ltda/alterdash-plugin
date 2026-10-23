---
name: relatorio-pdf
description: Gera um relatório em PDF (A4) na identidade visual AlterVision com os dados do MCP AlterVision — fechamento do mês, resultado da semana, desempenho por loja ou por vendedor, metas, fluxo e conversão. Use quando o usuário pedir um relatório, PDF, fechamento, resumo para imprimir ou para enviar ao gerente/diretor, ou quando outra skill do plugin (escala, plano de ação, uptime) precisar entregar o resultado em PDF.
---

# Gerar relatório PDF

Monta um PDF A4 com os dados das lojas, seguindo a identidade visual AlterVision
(`references/identidade-visual.md`). O layout sai sempre do script oficial desta skill; nunca desenhe o PDF
por outro caminho nem invente outro visual.

Antes de escrever o conteúdo, leia `references/identidade-visual.md` (cores, logo, fontes,
estrutura e regras de escrita) e `references/formato-json.md` (o que o script aceita). Os caminhos
são relativos ao diretório base desta skill.

## 1. Entender o pedido

Descubra, perguntando só o que faltar:

- **Período.** "Mês passado", "setembro", "última semana". Converta para datas YYYY-MM-DD a partir
  de hoje. Sem período, use o último mês fechado.
- **Lojas.** Chame `get_stores` e resolva nomes para ids. Sem lojas citadas, use todas.
- **Público.** Gerente de loja (uma loja, foco em vendedores e ação do dia a dia) ou diretor
  (rede, ranking de lojas, meta). Isso muda a profundidade, não o visual.

## 2. Buscar os dados no MCP AlterVision

Faça as chamadas em paralelo quando não dependem umas das outras:

| Dado | Ferramenta |
| --- | --- |
| Faturamento, vendas, TC, PA (UPT), ticket médio, uptime por loja | `conversion_rate_per_date` (com `includeDetails` se for mostrar dia a dia) |
| Mesmo período de comparação (mês anterior ou mesmo mês do ano anterior) | `conversion_rate_per_date` de novo, com as datas de comparação |
| Metas, realizado e projeção | `metas_infos` (`includeSellers` para relatório de loja) |
| Atendimentos, atratividade, fluxo medido × ajustado | `get_metrics_from_stores` |
| Ranking de vendedores | `get_metrics_from_sellers` |
| Benchmark de mercado do mês | `market_data` (mês fechado, YYYY-MM) |
| Por que não compraram | `non_conversion_reasons_stats` (só lojas com AlterVez) |
| Corridas em andamento | `corridas_infos` |

Se uma ferramenta devolver `account_delinquent`, pare e diga ao usuário que o acesso está
bloqueado por pagamento em atraso e deve ser regularizado no painel. Se devolver erro de
autenticação, peça para reconectar o conector AlterVision.

## 3. Escrever o conteúdo

Siga a ordem da diretriz e as regras de escrita:

1. **Cartões** (3 a 5): os números que respondem ao pedido, cada um com "contra o quê".
2. **Resumo:** a conclusão em uma ou duas frases, números em `<b>`. Comece pelo resultado
   ("A rede fechou em 82% da meta"), nunca por "Este relatório apresenta".
3. **Seções** com tabela ou barras. Use barras divergentes para explicar o que somou e o que tirou
   (ex.: efeito de fluxo, conversão e ticket sobre o faturamento).
4. **Quadro de ação:** o que fazer, quem faz, quanto vale. Se não der para estimar o valor,
   escreva "sem dado".
5. **Qualidade dos dados:** dias com uptime baixo (abaixo de 95%), lojas sem integração de vendas
   (PA e preço médio zerados), lojas novas sem base de comparação, dias atípicos (feriado).
6. **Siglas** explicadas uma vez no fim (TC, PA, TM, fluxo/dia).

Formato de número: R$ 1.234.567 · 23,5% · −2,3 p.p. (sinal de menos U+2212). Acima de R$ 10 mil
pode abreviar (R$ 96 mil, R$ 1,25 milhão). Nunca invente número, meta ou nome: sem dado, escreva
"sem dado" ou tire o campo. Sem emoji, sem exclamação, sem "incrível" ou "excelente".

Quando o fluxo ajustado estiver ativo (`adjustFlow`), use os valores Adjusted e diga isso na nota
da tabela.

## 4. Gerar o PDF

Grave a especificação em um arquivo JSON e rode o script (precisa de `reportlab`; se faltar,
instale com `pip install reportlab`):

```bash
python3 <diretório da skill>/scripts/gerar_pdf.py especificacao.json relatorio.pdf
```

Para um gráfico que o script não desenha (ex.: linha diária de fluxo), gere uma PNG com matplotlib
usando só as cores da diretriz e inclua com um bloco `imagem`.

Nomeie o arquivo de forma descritiva (`fechamento-setembro-2026-rede.pdf`) e salve na pasta de
trabalho do usuário.

## 5. Conferir antes de entregar

Converta a primeira página em imagem (`pdftoppm -r 60 -png -f 1 -l 1 relatorio.pdf pg`) e olhe.
Passe o checklist da diretriz:

- Logo branco no canto superior esquerdo, sobre azul-marinho
- Só as cores da tabela de cores; destaque em rosa #96084E
- Números no padrão brasileiro e com a comparação escrita
- Primeira frase com a conclusão; última parte com a ação
- Qualidade dos dados informada; nenhum número inventado
- Rodapé com relatório · rede · período e número da página

Na resposta, diga em uma linha a conclusão principal e onde o PDF foi salvo.
