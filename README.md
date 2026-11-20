# mineru.sh

The landing page for [Mineru](https://mineru.sh), a personal AI assistant that lives on your own machine. One static page, no build step, no JavaScript, no third-party requests.

- `site/` is the whole site: `index.html`, `style.css`, the images, and a self-hosted copy of JetBrains Mono (SIL Open Font License, `site/fonts/OFL.txt`).
- `tools/build_assets.py` rebuilds the images from the engine repo's banner and demo sources.
- `wrangler.jsonc` deploys `site/` as a Cloudflare Workers static-assets project.
- `HOSTING.md` records the domain, hosting, and DNS hardening setup.

The assistant's engine lives in a separate repo, [mineru-assistant](https://github.com/Maninae/mineru-assistant).

## Edit the page

Change the copy in `site/index.html`, the look in `site/style.css`. Preview locally:

```bash
python3 -m http.server 8765 --directory site
```

Deploy (needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment):

```bash
npx wrangler deploy --dry-run
npx wrangler deploy
```
