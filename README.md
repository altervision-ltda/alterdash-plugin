# alterdash-plugin

Claude plugin marketplace for AlterVision. It holds the `altervision` plugin, which connects Claude
to the AlterVision MCP (`https://api.painelalter.com/mcp`: flow, conversion, goals and camera uptime
per store) and adds four skills:

| Skill | What it does |
|---|---|
| `escala-do-time` | Builds the sellers' schedule from flow per hour and weekday and average service time |
| `relatorio-pdf` | Branded A4 PDF report (`scripts/gerar_pdf.py`) |
| `plano-de-acao-meta` | How far the goal is, where the gap can come from, and what each action is worth |
| `conectividade-uptime` | Camera uptime per store and day, hours with no data and share of estimated flow |

Details in [plugins/altervision/README.md](plugins/altervision/README.md).

## Install

```bash
claude plugin marketplace add altervision-ltda/alterdash-plugin
claude plugin install altervision@alterdash
```

On first use of an AlterVision tool, Claude opens the painel OAuth login.

`relatorio-pdf` needs Python 3 with `reportlab` (`pip install reportlab`).

## Publishing a new version

1. Change the plugin under `plugins/altervision/`.
2. Bump `version` in `plugins/altervision/.claude-plugin/plugin.json`; users only get an update
   when the version changes.
3. Open a PR. CI runs `claude plugin validate` on the marketplace and the plugin and renders the
   example PDF (downloadable from the run's artifacts).
4. Merge to `main`. Users update with `claude plugin marketplace update alterdash`.

Check locally before pushing:

```bash
npx -y @anthropic-ai/claude-code plugin validate .
```

## Brand guide

The visual identity is in `plugins/altervision/skills/relatorio-pdf/references/identidade-visual.md`,
with the logo in `.../relatorio-pdf/assets/`.
