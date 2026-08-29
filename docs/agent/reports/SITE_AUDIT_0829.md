# Site audit 2026-08-29 — what the PUBLIC pages actually say

**Written 2026-08-29 by `agent/prompts/SITE_AUDIT.md`**, its first run. Subject
is the DEPLOYED GitHub Pages site <https://catt144.github.io/SMR-CommunityMods/>
and the two live store listings — **not** the working tree.

> ⚠️ **This is a report, and reports are not authority.** Where it disagrees with
> an `agent/bugs/` entry or an `agent/facts/` fact, they win. Every number below
> was taken as a reading (deployments API, the deployed blob, the live page, the
> delivered `.fpk`); none was carried forward from a record.

## Verdict

**One finding, already known and already filed as checklist 81.** Everything else
the sheet asks about is clean. No new defect, no new fact, no new owner decision.

## §1 · The control — which commit is live

`GET /repos/catt144/SMR-CommunityMods/deployments?environment=github-pages`, then
the newest row's `/statuses`:

| deployment | sha | status | when |
|---|---|---|---|
| `6149512842` | **`7f4bb78`** | **`success`** | 2026-08-28T22:25:18Z |
| `6149454816` | `7f4bb78` | `success` → `inactive` | 2026-08-28T22:21:28Z |
| `6072497979` | `abe46c9` | (superseded) | 2026-08-24T22:19:08Z |

⇒ **deployed = `7f4bb78`.** `git log 7f4bb78..HEAD` in the site repo is exactly
one commit, `fcb2aa9`, touching one file, `content/index.md`, one line. Both
repos are clean and level with `origin/main`, so nothing is stuck unpushed.

STATE's "deployed `7f4bb78`" line was **correct** at this reading — but it was
re-derived, not trusted, which is the whole point of §1.

## §2 · The count chain — three readings, all 81

| source | reading | how |
|---|---|---|
| what the stores claim | **"Eighty-one repairs"** | the **delivered** archive, below |
| what the site backs | **81** | `??? ` entries in `7f4bb78:content/fix-list.md` |
| the live page witness | **81** | `<details` count on the live `/fix-list/` |

⭐ The store claim was taken off **what a player actually receives**, not off the
tree: `steamapps/workshop/content/3215050/3787202810/ModContent.fpk`, 396,408 B,
md5 `af58c31e07e8586e2b2f31a913eeff7f` — **84 entries, 82 byte-identical to the
tree**, the 2 that differ being `items.lua` and `metadata.lua` (comment
stripping). Packed `version` 4, `pdx_version` "3". This reproduces `EF-068`'s
2026-08-29 measurement exactly, independently.

⇒ **the count claim is BACKED.** A store claim larger than the deployed count is
the highest-severity finding this sheet can produce, and there is none.

Two further card numbers, both checked against the deployed site:

* *"And **four** of them repair things you cannot see at all today"* — the
  deployed fix list's **Under the hood** section holds exactly **4** entries, and
  its own intro line says *"These four…"*. ✓
* Per-section entry counts at the deployed sha: 9 · 18 · 8 · 8 · 11 · 9 · 7 · 7 ·
  4 = **81**, plus a prose-only *"What is not on this page"* section.

## §3 · ⚠️ THE ONE FINDING — the live site contradicts itself on one number

**On the live site, `index.md` says "five fixes are judgment calls" while the
FAQ says six, twice.** Read off both live pages, not off the repo:

```
LIVE /            → "five fixes are judgment"
LIVE /faq/        → "Five other judgment calls"  +  "Six fixes are judgment calls"
```

**Six is the truth.** The deployed fix list marks exactly six entry titles
*judgment call* — dust devil wave sizes · Biorobots and Dust Sickness · colonists
sheltering in vacuum · drones writing a building off · Extractor AI capping
staffed extractors (F108) · Edit Payload. The FAQ names those same six, in both
places. **`index.md` is the only wrong surface.**

⇒ **the repo is already right.** `fcb2aa9` corrects it and is the *only*
undeployed commit. This is precisely the partial-deploy shape the sheet warns
about: the FAQ edit landed in `7f4bb78` and the index edit in `fcb2aa9`, so
deploying one and not the other left the public site disagreeing with itself
**while the repo reads perfectly consistent**. A tree-only sweep finds nothing
here.

**Severity: low.** Nobody is misled about what the pack does or does not change;
the fix list itself is right and is where a reader checks. It is a
self-contradiction on a public page, and one deploy clears it.

## §4 · Links, both directions — all clean

Nine URLs, all **200** after redirects: the two store listings, the tracker and
its repo root, and all five site pages. `install.md#what-it-puts-in-your-save` —
linked from three pages — resolves to a real `id=` on the live install page. The
`mkdocs.yml` nav carries all five pages.

**Route checks (a 200 is not the whole check):**

* ✅ **`EF-067` is handled on both surfaces.** The FAQ carries an explicit
  *"Paradox Mods pages have no comment section"* warning that names console
  players — *"which includes every Xbox and PlayStation player"* — and routes
  them to the tracker, noting it works from a browser on any device including a
  phone, and that a plain description is worth filing when there is nothing to
  attach.
* ✅ **The store card survives the auto-fill.** Because one `description` fills
  **both** portals, the card says *"If this page has a comment section, that
  works too"* — portal-agnostic, so it does not promise Paradox readers a route
  that does not exist. Verified in the **delivered** archive, not just the tree.
* ✅ Platform detail is right: Steam Deck omits the `Ctrl-F1` bug reporter;
  Xbox/PlayStation have no logs or console commands.

**Fences (`EF-054`, `FIX_POLICY` §8):** fredware's mod is named **nowhere** on
any player surface or in the shipped card. The three "load order" sections are
explicit *refusals* to advise — *"We have not measured this, and we are not going
to guess at it"*, and the FAQ closes *"it is not a load-order instruction"*. ✓

## §5 · Publishing health — intact

* `publish-site.yml` trigger is **`workflow_dispatch:` only**; the `push:` block
  is still commented out. Identical at `7f4bb78` and `HEAD`.
* The **exposure gate** is intact and still fails the build on all three legs:
  the `docs_dir: content` check, any `../` escape under `mkdocs.yml`/`content`,
  and the presence of `.gitmodules`. `mkdocs.yml` still declares
  `docs_dir: content`, so the gate passes. Build runs `--strict`.
* **Pages source = GitHub Actions: INFERRED, not read.** That setting needs auth.
  The inference is a `success` deployment on the `github-pages` environment with
  `environment_url` set, at 2026-08-28T22:25:18Z.

## §6 · One repo-side correction made (not a public surface)

`metadata.lua`'s comment block closed with *"The count is settled as FIVE
consistently across card, this string, site FAQ and fix list"* — a 2026-08-15
note that went **false on 2026-08-28** when F108 shipped as a judgment call. The
five→six→five history it records is about F85 and is unrelated to the movement
that put the count back to six; F85 remains `wontfix` and out. The block also
instructs future agents on where to recount from, so a future reader would have
been led by it — the trap this project keeps paying for.

**Corrected in place** with a superseding note. ⚠️ **Nothing shipped changes**:
comments are stripped at pack time (the delivered `metadata.lua` differs from the
tree by exactly that stripping), and no string, number or `version` was touched.

## What the owner must press

**One run of *Actions → Publish docs site*** on `catt144/SMR-CommunityMods`.
That deploys `fcb2aa9` and clears the five/six contradiction. **Already filed as
checklist 81** — this audit confirms it against the live pages and adds nothing
new to decide.

⛔ Not taken here, by design: publishing is the owner's act, and this sheet only
reads, measures and reports.

## Nothing else is owed

No falsifiable count claim, no broken link, no dead route, no fence breach, no
publishing-config drift, and no defect in the pack found while reading.
