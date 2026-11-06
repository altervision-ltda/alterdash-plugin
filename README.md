# alterdash-plugin

Claude plugin marketplace for AlterVision. It holds the `altervision` plugin, which connects Claude
to the AlterVision MCP (`https://api.painelalter.com/mcp`: flow, conversion, goals and camera uptime
per store) and adds four skills:

| Skill | What it does |
|---|---|
| `escala-do-time` | Builds the sellers' schedule from flow per hour and weekday and average service time |
| `relatorio-pdf` | Branded A4 PDF report, drawn with reportlab from `references/layout-pdf.md` |
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
3. Open a PR. CI runs `claude plugin validate` on the marketplace and the plugin and checks that
   every file is an allowed type.
4. Merge to `main`. Users update with `claude plugin marketplace update alterdash`.

Check locally before pushing:

```bash
npx -y @anthropic-ai/claude-code plugin validate .
npx -y @anthropic-ai/claude-code plugin validate plugins/altervision
```

The plugin directory only accepts Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO images
from organizations that aren't Verified (plus LICENSE, README and .gitignore). Don't add scripts,
fonts or other binaries; describe what Claude should build in Markdown instead.

## Brand guide

The visual identity is in
[identidade-visual.md](plugins/altervision/skills/relatorio-pdf/references/identidade-visual.md),
with the logo in [relatorio-pdf/assets/](plugins/altervision/skills/relatorio-pdf/assets/).

## Support and license

Support: <https://painelalter.com/tickets>. Proprietary, see [LICENSE](LICENSE).
