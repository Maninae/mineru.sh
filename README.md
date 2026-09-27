# mineru.sh

The landing page for [Mineru](https://mineru.sh), a personal AI assistant that lives on your own machine. One static page, no build step.

- `site/` is the whole site: `index.html`, `style.css`, `fox.svg`.
- `wrangler.jsonc` deploys `site/` as a Cloudflare Workers static-assets project.
- `HOSTING.md` records the domain, hosting, and DNS hardening setup.

The assistant's engine lives in a separate repo, `mineru-assistant`, which opens on GitHub soon.

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
