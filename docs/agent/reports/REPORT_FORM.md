# The site's report form — how it works and what it needs

Built 2026-09-19 on the owner's brief. GitHub refuses a save file: the attachment limit is 25 MB and
`.sav` is not an accepted type. Saves in `saves/` measured 27.0–56.4 MB (66 `.sav` files, median
30.5 MB, `find -L saves -name '*.sav' -printf '%s'`), and gzip saves 0.1–0.3 % because they are
already compressed. So players fell back to Steam comments or public Drive links, and often never
replied. The site now takes the report and the file itself.

## The route

- **Page:** `/report/` on the site, titled *Bug reports & problems* (`SMR-CommunityMods`,
  `content/report.md` and `content/javascripts/report.js`).
- **Worker:** `smr-save-drop` at `https://smr-save-drop.stkotor2.workers.dev`, source in that repo's
  `worker/`. It is deployed with `npx wrangler deploy` from `worker/`. The owner's Cloudflare login
  is on this machine.
- `PUT /upload` streams the file into the private R2 bucket `smr-uploads` under a short code. There
  is no public access and no read route. A lifecycle rule `expire-30-days` deletes files after 30
  days, and the page promises that.
- `POST /report` files an issue on **`catt144/SMR-CommunityMods`** and pings Discord with the link and
  the file code. Labels are `from-form`, one per mod (`fix-pack`, `opt-in`, `site`, `unsure`) and one
  per report type (`mod-problem`, `game-bug`); GitHub created each label on first use. Player text is
  fenced in the issue, so it cannot mention users or link issues.
- **Guards:** the Origin must be `https://catt144.github.io`, files are capped at 100 MB, and only
  `.sav .zip .log .txt` are accepted. A hidden honeypot field catches simple bots. There is **no
  Turnstile**, by owner ruling ("leave it out for now"); it is the next step if spam appears.

## Secrets and upkeep

- `GITHUB_TOKEN` and `DISCORD_WEBHOOK` are Worker secrets. They are set with
  `npx wrangler secret put <NAME>` and are in no repo file. The token is fine-grained, limited to
  `SMR-CommunityMods` with Issues read/write only, and **it expires**; the owner chose the date. Renew it
  before then. An expired token does not lose a report: the Worker falls back to posting the full
  report in Discord with a warning line.
- The test files have been deleted from the bucket. The owner deleted test issue #1.

## Verified, and not

- Verified live on 2026-09-19: an upload round-trip (sha256 matched), refusals for a foreign Origin,
  a bad file type and a missing mod, issue #1 with its labels, and the Discord ping (owner saw it).
- The report-type field was tested locally against a mock GitHub, for both types and for none, then
  deployed.
- **Not verified:** a report sent from the published page in a real browser. The Worker refuses any
  other Origin, so only the owner can run it (checklist ck205). No form-filed issue existed when this
  was written (`api.github.com/repos/catt144/SMR-CommunityMods/issues?state=all` returned none).

## Left as it was, on purpose

The old tracker `SMR-CommunityFixPack/issues` still takes issues. This repo's `README.md` and
`docs/FIELD_REPORT_REPLIES.md` still point to it. The store card no longer does; see
`STORE_CARD_LIVE.md`, 2026-09-19. Repointing those two is agent work that nobody has asked for.
The opt-in pack is a choice in the form's dropdown, but the site has no page about it yet.
