---
name: escala-do-time
description: Monta a escala de trabalho dos vendedores de uma loja a partir do fluxo de visitantes por dia da semana e por hora, do tempo médio de atendimento e do desempenho de cada vendedor no MCP AlterVision. Use quando o usuário pedir para fazer, montar, revisar ou otimizar a escala, os turnos, as folgas ou o dimensionamento do time; perguntar quantos vendedores precisa em cada horário; ou dizer que falta ou sobra gente na loja em certos horários.
---

# Fazer escala do time

Cruza a demanda (visitantes por hora e por dia da semana) com a capacidade do time (atendimentos
por vendedor por hora) para dizer quantas pessoas a loja precisa em cada hora e propor uma escala
que cubra isso dentro das regras de jornada.

Escrita e visual seguem `../relatorio-pdf/references/identidade-visual.md`: conclusão primeiro,
números no padrão brasileiro, nada inventado.

## 1. Combinar as premissas

Pergunte de uma vez só o que o usuário ainda não disse:

- **Loja** (uma escala por loja). Resolva com `get_stores`.
- **Time:** nomes, carga semanal de cada um (ex.: 44 h, 36 h, 6 h/dia para meio período), quem
  tem restrição (estudo, folga fixa). Se o usuário não listar, ofereça os vendedores que aparecem em
  `get_metrics_from_sellers` e peça confirmação; nunca crie nomes.
- **Horário de funcionamento** por dia da semana.
- **Regras de jornada.** Proponha como ponto de partida e peça para confirmar: 6x1, até 8 h/dia e
  44 h/semana, intervalo de 1 h para jornada acima de 6 h, ao menos um domingo de folga a cada três
  semanas, mínimo de 2 pessoas na abertura e no fechamento. Deixe claro que a regra válida é a da
  convenção coletiva da loja; você não dá parecer jurídico.
- **Semana da escala** (as próximas datas) e se há feriado ou data comercial nela.

## 2. Medir a demanda

Use as 4 últimas semanas completas como base, salvo pedido diferente.

1. `get_flow_per_day` no período, com `includeDetails`: visitantes por dia. Agrupe por dia da
   semana e tire a média, descartando feriados e dias com fluxo muito fora do padrão (cite-os).
2. `get_flow_per_hour`, uma chamada por dia, com `includeDetails` e `responseType: "best_hours"`.
   Para não exagerar no número de chamadas, use as 2 ocorrências mais recentes de cada dia da semana
   (14 chamadas); se o usuário quiser mais precisão, use as 4. Faça as chamadas em paralelo.
   Horas sem fluxo medido vêm omitidas: trate como dado faltante, não como zero, e confira o uptime
   do dia em `conversion_rate_per_date` (`includeDetails`) antes de usar o dia.
3. Monte a matriz **hora × dia da semana** com a média de visitantes.

Use a preferência de fluxo do usuário (individual ou grupo); para dimensionar atendimento, fluxo de
grupos é a medida mais fiel, porque um grupo costuma ser atendido por um vendedor. Diga qual usou.

## 3. Medir a capacidade

`get_metrics_from_sellers` nas mesmas 4 semanas:

- **Duração média do atendimento** (minutos) da loja e de cada vendedor.
- **Atendimentos e conversão por vendedor**, para colocar quem converte mais nos picos.

Capacidade por vendedor por hora = 60 ÷ duração média do atendimento × ocupação-alvo.
Use ocupação-alvo de 70% (o vendedor não fica 100% do tempo atendendo) e diga a premissa.

Necessário na hora = arredondar para cima (visitantes na hora × taxa de abordagem ÷ capacidade),
com o mínimo de abertura e fechamento. Taxa de abordagem padrão: atendimentos ÷ fluxo da loja no
período (vem de `get_metrics_from_stores`). Mostre a conta para uma hora de pico, para o usuário
poder conferir.

## 4. Montar a escala

1. Gere a **matriz de necessidade** (hora × dia), destacando os picos.
2. Distribua turnos por pessoa respeitando carga, folgas e regras. Priorize:
   - cobrir os picos com os vendedores de maior conversão;
   - folgas nos dias de menor fluxo;
   - rodízio justo de domingos e fins de semana.
3. Compare **cobertura × necessidade** hora a hora e liste onde ficou faltando ou sobrando gente.
   Se o time não fecha a conta, diga quantas horas faltam e em quais faixas; não esconda o buraco.

## 5. Entregar

No chat:

- Uma frase com a conclusão ("O pico é sábado das 15h às 18h, com 4 vendedores necessários; o time
  atual cobre todos os horários menos sábado às 17h").
- Tabela da escala: pessoa × dia (entrada–saída, intervalo, folga) e total de horas na semana.
- Matriz de necessidade × cobertura (hora × dia).
- Premissas usadas e o que conferir na convenção coletiva.

Ofereça a versão para mural: um PDF A4 em paisagem gerado pela skill `relatorio-pdf`, com a
matriz como tabela de células com fundo (`creme` para normal, `rosa_claro` para movimento alto,
`rosa` para pico) e a escala por pessoa logo abaixo.
