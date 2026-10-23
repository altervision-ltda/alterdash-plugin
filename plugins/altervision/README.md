# Plugin AlterVision para Claude

Conecta o Claude ao MCP da AlterVision (`https://api.painelalter.com/mcp`) e adiciona quatro skills:

| Skill | O que faz |
| --- | --- |
| `escala-do-time` | Escala de vendedores a partir do fluxo por hora e dia da semana e do tempo de atendimento |
| `relatorio-pdf` | Relatório PDF A4 na identidade visual AlterVision (`scripts/gerar_pdf.py`) |
| `plano-de-acao-meta` | Quanto falta para a meta, de onde pode vir e o que fazer, com o valor de cada ação |
| `conectividade-uptime` | Uptime das câmeras por loja e dia, horas sem dado e parcela do fluxo estimada |

A identidade visual está em `skills/relatorio-pdf/references/identidade-visual.md` e o logo em
`skills/relatorio-pdf/assets/`.

## Instalar no Claude Code

```bash
claude plugin marketplace add altervision-ltda/alterdash-plugin
claude plugin install altervision@alterdash
```

Na primeira chamada de ferramenta, o Claude abre o login OAuth do painel (`/mcp/oauth/authorize`).

O `relatorio-pdf` precisa de Python 3 com `reportlab` (`pip install reportlab`).
