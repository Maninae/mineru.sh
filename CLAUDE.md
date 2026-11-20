# mineru.sh (agent notes)

Landing page for the Mineru personal assistant, served at https://mineru.sh from Cloudflare Workers static assets.

- **Design intent:** the page is the engine README's banner, extended. The eye lands on the fox emblem and the `mineru` wordmark, then reads down: the 07:00 morning-brief screenshot, what it does by day, the night timeline of memory jobs, the install commands.
- **Palette and type:** navy ground `#1a183a`, cool white ink, mint `#7fe9d8` for prompts, labels and links. One font, JetBrains Mono, self-hosted in `site/fonts/` so the page makes no third-party requests. Dark only; the navy is the brand.
- **Gradient discipline:** the mint-to-violet gradient appears twice only, on the emblem and on the night timeline's spine. Do not add it to buttons, headings or borders.
- **Files:** everything deployable is in `site/`. `wrangler.jsonc` at the root points Workers at it. No build step, no framework, no JS.
- **Images:** `tools/build_assets.py` rebuilds `emblem.webp`, `morning-brief.webp`, `og.jpg` and the icon set from the engine repo's `assets/banner/` and `assets/demo/`. Re-run it when the banner or the demo screenshot changes there.
- **Copy rules:** generic and public, and every claim must be true of the public engine (check its README and `engine/recurring/` before adding one). No personal details about anyone. No Zelda, Nintendo, or "Sage of Spirit" references anywhere public (the name origin stays private). No email address on the page (the domain deliberately has no mail: null MX + DMARC reject).
- **Night timeline times** are the engine's default launchd schedule (`engine/launchd/*.plist.template`); update them if the defaults move.
- **Verify before shipping:** `npx wrangler deploy --dry-run`, then Playwright screenshots at desktop (1440) and phone (390) widths, and read the images.
- **Deploy and hardening runbook:** `HOSTING.md`.
