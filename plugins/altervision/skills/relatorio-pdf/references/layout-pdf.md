# Layout do PDF

Medidas para montar o relatório com `reportlab` seguindo a diretriz (`identidade-visual.md`).
Monte primeiro o conteúdo como uma lista de blocos (veja `exemplo.json`) e depois desenhe cada bloco
como descrito aqui. Os números chegam ao desenho como texto já no padrão brasileiro
(R$ 1.234.567 · 23,5% · −2,3 p.p.); o desenho não calcula nem formata.

## Página

- A4 retrato. Paisagem só para escala de mural com muitas colunas.
- Margens laterais de 15 mm. A área de conteúdo começa 16 mm acima da borda inferior e termina
  8 mm abaixo da faixa do topo.
- Título do documento (metadado) = título do relatório; autor = "AlterVision".

## Fontes

Procure TTFs instaladas nesta ordem e registre a primeira família que tiver regular e negrito:

- Texto: Inter → Lato → Carlito → Helvetica (embutida).
- Números: Roboto Mono → DejaVu Sans Mono → Courier (embutida).

Pastas comuns: `/usr/share/fonts`, `~/.fonts`, `~/.local/share/fonts`, `/Library/Fonts`,
`~/Library/Fonts`, `C:/Windows/Fonts`. OTF com contornos CFF não carrega no reportlab; pule.

## Capa (página 1)

- Faixa de 56 mm de altura no topo, largura total, com o degradê #3A1446 → #14133B a 115°
  (do canto superior esquerdo para o inferior direito).
- Logo (`assets/Logo_AlterVision_branco_transparente.png`, proporção 480 × 232) com 40 mm de
  largura, topo a 7 mm da borda superior, na margem esquerda.
- Título em texto negrito 24 pt, branco, 14 mm acima da base da faixa.
- Período em texto 10 pt, branco, 6,5 mm acima da base da faixa.
- Escopo (número de lojas ou nome da loja) em mono 10 pt, branco, alinhado à direita na mesma
  linha do período.
- Logo do cliente, só se o usuário fornecer o arquivo: canto superior direito, até 30 mm de
  largura e 16 mm de altura, proporção original.

## Páginas internas

- Faixa azul-marinho #14133B de 14 mm no topo.
- Logo com 20 mm de largura, topo a 2,5 mm da borda, na margem esquerda.
- Nome da página em texto negrito 11 pt, branco, 25 mm à direita da margem, centrado na faixa.
- Escopo em mono 9 pt, branco, alinhado à direita.

## Rodapé (todas as páginas)

Texto 7,5 pt em #6E6C7E, 9 mm acima da borda inferior: à esquerda
"relatório · rede · período"; à direita "página / total". Para saber o total, desenhe cabeçalho
e rodapé só no fim (canvas que guarda as páginas e as desenha no `save`).

## Blocos

Depois de cada bloco, 5 mm de espaço (parágrafo: 3 mm; imagem: 4 mm).

| Bloco | Como desenhar |
| --- | --- |
| Cartões (3 a 5) | Lado a lado, 4 mm entre eles, fundo branco, borda #E6E2D8 de 0,8 pt, cantos de 2,5 mm, 3,5 mm de respiro interno. Rótulo texto 8 pt #5B5A74; valor mono negrito, o mesmo tamanho em toda a fileira (o maior entre 24 e 12 pt que caiba em uma linha); comparação texto 8 pt em #0E6B38 (positivo), #9E2A22 (negativo) ou #5B5A74 (neutro). |
| Resumo | Caixa creme #F8F5EF, cantos de 1,5 mm, filete rosa #96084E de 1,2 mm à esquerda, 4 mm de respiro. Texto 11 pt, entrelinha 15, números em negrito. |
| Seção | Se sobrarem menos de 40 mm na página, comece outra. Rótulo opcional em mono 8 pt, MAIÚSCULAS, rosa; título em texto negrito 14 pt, azul-marinho. |
| Parágrafo | Texto 10 pt, entrelinha 14, azul-marinho. |
| Tabela | Cabeçalho texto negrito 8 pt #5B5A74, repetido em cada página. Células texto 9 pt; números em mono 9 pt à direita (1ª coluna à esquerda, as demais à direita). Linha fina #E6E2D8 de 0,6 pt abaixo de cada linha, 4 pt de respiro vertical e 5 pt lateral. Meta embaixo do valor em mono 7 pt rosa. Linha de total com fundo creme e filete azul-marinho de 1 pt em cima. Nota da tabela em 7,5 pt #6E6C7E, 1,5 mm abaixo. |
| Status em célula | Círculo de 3,2 pt de raio: verde #1E9E57 (ok), amarelo #E0A800 (atenção), vermelho #D9463B (ruim), seguido do texto 9 pt. |
| Mapa de calor (escala) | Fundo da célula creme, rosa claro #F7D9E7, rosa #96084E (pico) ou azul-marinho; nos dois últimos, texto branco negrito. |
| Barras divergentes | Uma linha de 7 mm por item. Rótulo à esquerda em 30% da largura; eixo vertical #E6E2D8 no meio do resto. Barra verde #1E9E57 para a direita (somou) ou vermelha #D9463B para a esquerda (tirou), proporcional ao maior valor absoluto, deixando 18 mm para o texto do valor ao lado (mono 8,5 pt, #0E6B38 ou #9E2A22). A maior perda: rótulo em negrito rosa e valor em negrito. Não quebre o bloco entre páginas. |
| Quadro de ação | Caixa creme (ou rosa claro #F7D9E7) com filete rosa. Título em rótulo de seção ("PLANO DE AÇÃO"), depois uma tabela de três colunas: O que fazer (60%), Quem (20%), Quanto vale (20%, mono à direita; sem estimativa, "sem dado"). |
| Qualidade dos dados | Caixa #FBF0CC, sem filete. Título "QUALIDADE DOS DADOS" em mono 8 pt #8A6100; itens com "• " em texto 9 pt #8A6100. |
| Imagem | Gráfico que a tabela e as barras não resolvem (ex.: linha diária de fluxo), feito em matplotlib só com as cores da diretriz. Largura até a largura útil, proporção original. |
| Nova página | Quebra de página; a faixa interna passa a mostrar o novo título. |
| Siglas | No fim, 4 mm abaixo do último bloco, em 7,5 pt #6E6C7E. |
