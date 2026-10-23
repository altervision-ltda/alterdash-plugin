# Formato da especificação de `gerar_pdf.py`

O script desenha; ele não calcula nem formata. Todo número chega como texto já no padrão
brasileiro (R$ 1.234.567 · 23,5% · −2,3 p.p.), exceto o `valor` numérico das barras, que só
define o comprimento.

```json
{
  "titulo": "Fechamento de setembro · Rede Exemplo",
  "periodo": "01/09/2026 a 30/09/2026",
  "escopo": "12 lojas",
  "relatorio": "Fechamento mensal",
  "rede": "Rede Exemplo",
  "orientacao": "retrato",
  "logo_cliente": "/caminho/opcional/logo_cliente.png",
  "siglas": "TC: taxa de conversão. PA: peças por atendimento. TM: ticket médio.",
  "blocos": [ ... ]
}
```

- `titulo`, `periodo`: capa (faixa com degradê). `escopo`: à direita, em mono (número de lojas ou nome da loja).
- `relatorio` · `rede` · `periodo`: rodapé, com "página / total" à direita.
- `orientacao`: `"retrato"` (padrão) ou `"paisagem"` (escala de mural com muitas colunas).
- `logo_cliente`: só se o usuário fornecer o arquivo. Nunca recrie um logo.

## Blocos, na ordem da diretriz

| `tipo` | Campos | Desenha |
| --- | --- | --- |
| `cartoes` | `itens`: 3 a 5 de `{rotulo, valor, comparacao, tendencia}`; `tendencia` = `positivo` \| `negativo` \| `neutro` | Cartões de número lado a lado |
| `resumo` | `texto` (aceita `<b>…</b>`) | Caixa creme com filete rosa |
| `secao` | `titulo`, `rotulo` opcional (vira MAIÚSCULAS espaçadas em rosa) | Título de seção |
| `paragrafo` | `texto` (aceita `<b>`, `<i>`, `<font color="#96084E">`) | Texto corrido |
| `tabela` | `colunas`, `linhas`, `alinhamento` (`"e"`/`"d"` por coluna; padrão: 1ª à esquerda, resto à direita), `larguras` (pesos relativos), `linha_total` (bool: última linha é total), `nota` | Tabela |
| `barras` | `itens`: `{rotulo, valor (número), texto}` | Barras divergentes; a maior perda sai em rosa |
| `acao` | `titulo`, `itens`: `{o_que, quem, quanto}`, `variante` = `creme` \| `rosa` | Quadro de ação |
| `qualidade` | `itens`: lista de textos | Caixa amarela "Qualidade dos dados" |
| `imagem` | `caminho`, `largura_mm` | Imagem (ex.: gráfico de linha feito em matplotlib com as cores da diretriz) |
| `pagina` | `titulo` | Nova página; a faixa interna passa a mostrar esse título |
| `quebra` | — | Nova página sem mudar o título da faixa |

### Células de tabela

Uma célula é um texto, ou um objeto:

- `{"valor": "R$ 96 mil", "meta": "meta R$ 110 mil", "tom": "negativo"}`: valor com meta em rosa pequeno embaixo; `tom` pinta o valor de verde/vermelho.
- `{"status": "ok" | "atencao" | "ruim", "texto": "No ritmo"}`: ícone verde, amarelo ou vermelho.
- `{"valor": "3", "fundo": "creme" | "rosa_claro" | "rosa" | "marinho"}`: célula com fundo (mapa de calor da escala; `rosa` = pico, texto branco).
