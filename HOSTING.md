# Hosting: mineru.sh

- **Registrar + DNS:** Cloudflare (registered 2026-09-16, renews yearly). Registrar lock on by default (`clientTransferProhibited`).
- **Hosting:** Cloudflare Workers static assets, Worker name `mineru-sh`, deployed with `npx wrangler deploy` from this repo. `workers_dev` is off so the site only answers on the custom domain.
- **Canonical host:** the apex `mineru.sh`. `www.mineru.sh` 301-redirects to the apex.

## Deploy

```bash
export CLOUDFLARE_API_TOKEN=...   # scoped token, see below
export CLOUDFLARE_ACCOUNT_ID=...
npx wrangler deploy --dry-run
npx wrangler deploy
```

Then attach the custom domain: Worker `mineru-sh` > Settings > Domains & Routes > Add > Custom domain > `mineru.sh` (and `www.mineru.sh` if you want the redirect handled by a Redirect Rule on a proxied placeholder record; see the client-site-cloudflare skill).

## Hardening (done once, verify yearly)

| Item | Where | State |
|---|---|---|
| Registrar lock | Registrar > Manage domains | on by default |
| DNSSEC | Zone > DNS > Settings > Enable DNSSEC (Cloudflare publishes the DS for Registrar domains, 1-2 days) | pending |
| Account 2FA | My Profile > Authentication | human-only |
| Always Use HTTPS | Zone > SSL/TLS > Edge Certificates | pending |
| No-mail records | DNS: `MX @ 0 .` (null MX), `TXT @ "v=spf1 -all"`, `TXT _dmarc "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s"` | pending |

## Token scope (for terminal automation)

Account: Workers Scripts Edit. Zone (mineru.sh only): DNS Edit, Zone Settings Edit, Workers Routes Edit, SSL and Certificates Edit. Keep the token in the macOS Keychain, never in a file.
