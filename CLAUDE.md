# mineru.sh (agent notes)

One-screen landing page for the Mineru personal assistant, served at https://mineru.sh from Cloudflare Workers static assets.

- **Design intent:** the eye lands on the name, then the one-line "what", then three short facts. The fox-orange accent appears exactly twice (blinking cursor, fox mark). Keep it that way; do not add sections, cards, or a second accent.
- **Files:** everything deployable is in `site/`. `wrangler.jsonc` at the root points Workers at it. No build step, no framework, no JS.
- **Fonts:** Fraunces (headline, lede) and JetBrains Mono (prompt, fact labels) from Google Fonts, with serif and monospace fallbacks. Choose fonts deliberately; never fall back to the tool default.
- **Copy rules:** generic and public. No personal details about anyone. No email address on the page (the domain deliberately has no mail: null MX + DMARC reject).
- **Verify before shipping:** `npx wrangler deploy --dry-run`, then Playwright screenshots at desktop and phone widths, and read the images.
- **Deploy and hardening runbook:** `HOSTING.md`.
