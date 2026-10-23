# Identidade visual AlterVision

Vale para todo relatório, imagem, PDF, página ou apresentação gerado com dados da AlterVision. Quando existe script oficial, o
relatório sai sempre dele (aqui: `scripts/gerar_pdf.py`).

## Logo

Branco, sobre fundo escuro (azul-marinho #14133B ou o degradê da capa), no canto superior
esquerdo do cabeçalho.

| Regra | Como fazer |
| --- | --- |
| Arquivo | `assets/Logo_AlterVision_branco_transparente.png` (PNG branco, fundo transparente, 480 × 232 px) |
| Posição | Canto superior esquerdo do cabeçalho; nas páginas internas, menor, ao lado do título da página |
| Tamanho | Capa: cerca de 40 mm de largura. Páginas internas e imagens de celular: 20 a 25 mm |
| Respiro | Espaço livre em volta igual à altura do "A" de ALTER |
| Logo do cliente | Canto superior direito da capa e no encerramento, com a proporção original |
| Nunca | Logo colorido, sobre fundo claro, esticado, girado, com sombra ou recriado com texto |

## Cores

Azul-marinho para fundo e texto, creme para caixas, rosa para o que precisa de atenção.
Verde e vermelho só para números bons e ruins. A cor de destaque se chama "rosa", nunca "magenta".

| Nome | HEX | Uso |
| --- | --- | --- |
| Azul-marinho | #14133B | Cabeçalho, capa, títulos, texto principal |
| Degradê da capa | #3A1446 → #14133B (115°) | Capas e faixas de destaque |
| Rosa | #96084E | Destaques, pico na escala, quadros de alerta, linhas de destaque |
| Rosa claro | #F7D9E7 | Fundo de célula ou etiqueta rosa |
| Creme | #F8F5EF | Fundo de caixas, cartões e conclusões |
| Branco | #FFFFFF | Fundo das páginas |
| Borda | #E6E2D8 | Bordas de cartões e linhas de tabela |
| Texto secundário | #5B5A74 | Legendas, notas, rótulos |
| Texto apagado | #6E6C7E | Notas de rodapé, valores de referência |
| Verde (número bom) | #0E6B38 | Texto de valor positivo |
| Verde (barra) | #1E9E57 | Barras e ícones positivos |
| Vermelho (número ruim) | #9E2A22 | Texto de valor negativo |
| Vermelho (barra) | #D9463B | Barras e ícones negativos |
| Amarelo de atenção | #8A6100 sobre #FBF0CC | Avisos de qualidade dos dados |

Texto sempre escuro sobre claro, ou branco sobre azul-marinho/rosa. Nunca rosa sobre vermelho.
No máximo uma cor de destaque por bloco.

## Fontes

Inter para títulos e texto; Roboto Mono só para números e rótulos de seção em maiúsculas.
Onde essas fontes não existem (PDFs gerados por script), use Carlito/Lato para o texto e
DejaVu Sans Mono para os números.

| Elemento | Fonte | Tamanho e peso |
| --- | --- | --- |
| Título da capa | Inter | 22–28 pt, negrito, branco sobre azul-marinho |
| Título de seção | Inter | 13–16 pt, negrito, azul-marinho |
| Rótulo de seção | Roboto Mono | 8–9 pt, MAIÚSCULAS, espaçado, rosa ou cinza |
| Texto | Inter | 9–11 pt, normal |
| Número de destaque | Roboto Mono | 20–40 pt, negrito |
| Número em tabela | Roboto Mono | 8,5–10 pt, alinhado à direita |
| Nota de rodapé | Inter | 7,5–8 pt, texto apagado |

Números no padrão brasileiro: R$ 1.234.567 · 23,5% · −2,3 p.p. (sinal de menos verdadeiro, U+2212).
Acima de R$ 10 mil pode abreviar: R$ 96 mil, R$ 1,25 milhão.

## Estrutura de um relatório

Abre com o resultado, mostra os números e termina dizendo o que fazer. Ordem fixa:

1. **Cabeçalho:** faixa azul-marinho com o logo à esquerda, título ("Fechamento de setembro · Rede")
   e o período; à direita, em Roboto Mono, o número de lojas ou o nome da loja. Páginas internas
   repetem uma faixa menor com o nome da página.
2. **Cartões de número:** 3 a 5 lado a lado, fundo branco, borda #E6E2D8, cantos arredondados.
   Rótulo pequeno em cima, número grande, comparação embaixo em verde ou vermelho.
3. **Frase-resumo:** caixa creme com filete rosa à esquerda, uma ou duas frases com a conclusão
   e os números em negrito.
4. **Tabelas:** cabeçalho em texto secundário, linhas finas #E6E2D8, números alinhados à direita;
   meta em rosa pequeno embaixo do valor; status com ícone verde, amarelo ou vermelho.
5. **Gráficos:** barras horizontais verdes (somou) e vermelhas (tirou) a partir de um eixo central;
   a maior perda em destaque.
6. **Quadro de ação:** caixa creme ou rosa com o que fazer, quem faz e quanto vale.
7. **Qualidade dos dados:** lista curta com câmera instável, vendas não integradas e dias atípicos.
8. **Rodapé:** nome do relatório · rede · período à esquerda e página ("3 / 10") à direita, em
   texto apagado.

Formatos: PDF A4 para fechamento e escala de mural; imagem vertical (1.080 px de largura) para
celular e WhatsApp, com fundo azul-marinho e cartões claros.

## Escrita

Tom de consultor: direto, curto, sempre em português do Brasil.

- **Comece pela conclusão:** "A rede fechou em 82% da meta", nunca "Este relatório apresenta…".
- **Frases curtas**, sem jargão; siglas explicadas uma vez no rodapé (TC, PA, TM, fluxo/dia).
- **Nunca invente números, metas ou nomes.** Sem dado, escreva "sem dado" ou deixe o campo de fora.
- **Toda comparação diz contra o quê:** "contra agosto/2026", "contra setembro/2025 (7 lojas)".
- **Seja honesto com os dados:** câmera instável, vendas atrasadas e lojas novas aparecem em
  "Qualidade dos dados".
- **Termine com ação:** o que fazer, quem faz e quanto vale.
- Sem emoji, sem exclamação, sem "incrível" ou "excelente".

## Checklist antes de entregar

- [ ] Logo branco no canto superior esquerdo, sobre azul-marinho
- [ ] Só as cores da tabela de cores; destaque em rosa #96084E
- [ ] Inter no texto, Roboto Mono nos números
- [ ] Números no padrão brasileiro e com a comparação escrita
- [ ] Primeira frase com a conclusão; última parte com a ação
- [ ] Qualidade dos dados informada; nenhum número inventado
- [ ] Rodapé com relatório · rede · período e número da página
