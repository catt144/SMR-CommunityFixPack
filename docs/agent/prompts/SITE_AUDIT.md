# Site audit — what the PUBLIC pages actually say (model-agnostic) — written 2026-08-29

Paste into a fresh Claude Code session to audit the **deployed** GitHub Pages
site, `catt144/SMR-CommunityMods` → <https://catt144.github.io/SMR-CommunityMods/>.
**Any model; the owner picks.** Staleness anchor: **written 2026-08-29** — verify
every specific against `git log` and the live API before trusting it.

> ⛔ **THIS AUDITS WHAT IS PUBLISHED, NOT WHAT IS COMMITTED.** Those are different
> things and the difference is the whole reason this sheet exists:
> `publish-site.yml` is `workflow_dispatch`-only **by design** (publishing is an
> owner act, public-docs chain rule 5), so the repo can be perfect and the public
> page still wrong. A sweep that reads the working tree and reports "consistent"
> has audited nothing a player can see.

> 🧭 **NOT this prompt** — a fix was added, retired or re-scoped and the WORDS
> need writing across every surface: that is `prompts/PUBLIC_SURFACE_SWEEP.md`,
> which authors. This one only reads, measures and reports.

## ⛔ The two things you may never do

1. **NEVER run the publish workflow, and never propose automating it.** Deploying
   is the owner's act. You report that a deploy is owed; you do not take it.
2. **NEVER try to "fix" a live store page by editing the strings** —
   `metadata.lua`'s `description` ships INSIDE the mod and only an upload changes
   a live page (`H-02`; `RELEASE_PORTAL_PREP.md` §0.5). Repo content in
   `C:\Dev\SMR-CommunityMods\content\` is ordinary editable work; if you edit it,
   say in the report that your edit is **undeployed** until the owner presses the
   button.

⚠️ **Keep a todo list from the first minute and update it after every item** —
the owner reads it to decide whether to step in. One entry per numbered check.

## 0 · Orient

1. `git log --oneline -5` and `git status -sb` in **both** `C:\Dev\SMR-BugFixPack`
   and `C:\Dev\SMR-CommunityMods` — an unpushed site commit can never deploy.
2. Read `docs/agent/STATE.md`. ⛔ **Its "deployed = <sha>" line is a claim with a
   date on it, not a reading.** Re-derive it in §1 — on 2026-08-29 that line was
   four days and two deploys stale, and a session repeated it twice as current.
3. This audit launches no game, so the STALE-PROBE gate does not apply.

## 1 · ⭐ THE CONTROL — which commit is actually live

⛔ **First, and everything downstream is derived from its answer.** `gh` is **not
installed** on this box (checked 2026-08-29) — use the public API directly; the
repo is public, so no auth is needed.

```bash
curl -s "https://api.github.com/repos/catt144/SMR-CommunityMods/deployments?environment=github-pages&per_page=5" \
  | python -c "import sys,json;[print(x['sha'][:7], x['created_at'], 'id=',x['id']) for x in json.load(sys.stdin)]"
```

⚠️ **A deployment row is not a success.** Check the newest one's state:

```bash
curl -s "https://api.github.com/repos/catt144/SMR-CommunityMods/deployments/<id>/statuses?per_page=3" \
  | python -c "import sys,json;[print(x['state'], x['created_at'], x.get('environment_url','')) for x in json.load(sys.stdin)]"
```

⇒ **the deployed sha is the newest deployment whose status reads `success`.** Then
in the site repo: `git log --oneline <deployed-sha>..HEAD` — that list is exactly
what the public cannot see. An empty list is the healthy answer.

## 2 · The count chain — the one claim the pack stakes its credibility on

The store card states a number of repairs; the fix list is where a reader checks
it. **Both stores' page bodies are auto-filled from `metadata.lua`'s `description`
on every upload**, so the live claim is whatever the last upload shipped.

1. **What the stores claim** — read it from the file that ships, not from memory:
   `grep -oE "[A-Z][a-z]+(-[a-z]+)? repairs" metadata.lua`.
   ⭐ Better, when the owner is subscribed: read the **delivered** archive, which
   is what a player actually receives — `python tools/pack_list.py <fpk> --tree .`
   and then its packed `metadata.lua` (`EF-068` carries the extraction route).
2. **What the site backs, derived from the DEPLOYED commit** — never off the page,
   never hand-typed:
   `git show <deployed-sha>:content/fix-list.md | grep -cE "^\?\?\? "`
3. **The independent witness — the live page.** Entries render as `<details>`:
   `curl -s "https://catt144.github.io/SMR-CommunityMods/fix-list/" | grep -c "<details"`
   ⚠️ That counts collapsibles, not entries by definition — add a non-entry
   collapsible to the page and the two numbers separate legitimately. **The
   deployed commit is the derivation; the page is the witness.** They agreed at
   **81** on 2026-08-29. If they ever disagree, report both and pick neither.
4. ⇒ **Report all three numbers.** A store claim larger than the deployed count is
   a falsifiable claim on a public page, and is the highest-severity finding this
   sheet can produce.

## 3 · Internal consistency across the five pages

`content/` is `index.md · install.md · fix-list.md · faq.md · for-modders.md`
(nav in `mkdocs.yml`). Read them **at the deployed sha**, not on disk:

* Any number stated more than once — the repair count, and the **judgment-call
  count**, which lives in both `index.md` and `faq.md` and has drifted before
  (5 → 6 when F108 shipped as a judgment call). ⛔ Those two files were updated in
  **different commits**, so a partial deploy leaves them disagreeing on the live
  site while the repo looks perfectly consistent. Check them separately.
* A count in a heading or intro that no longer matches the list beneath it.
* Fix-list entries filed in the section a **player** would look in, not the one
  that matches our internal cause.
* ⚠️ Cross-check every count against `python tools/doccheck.py --emit-counts` in
  the mod repo — never hand-type one, and never carry one forward from this file.

## 4 · Links, both directions

* Every link the **store card** makes to the site, and every link the **site**
  makes to the stores and the tracker:
  `curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -L "<url>"`.
* ⛔ **A 200 is not the whole check.** *"You can X" needs a route check*: confirm a
  real reader on that surface can walk the steps, on **each** platform. A console
  player has no Steam page and nothing to attach; Paradox has **no comment section
  at all** (`EF-067`), so any "leave a comment on the mod page" wording is a route
  that does not exist for them.
* ⛔ Never name fredware's mod on a player surface; no load-order advice
  (`EF-054`, `FIX_POLICY` §8).

## 5 · Publishing health (read-only)

* `.github/workflows/publish-site.yml` — confirm the trigger is still
  `workflow_dispatch` only, and that the exposure gate (the `docs_dir` check that
  fails the build if the config is pointed outside `content/`) is intact.
* Pages source must be **GitHub Actions** (Settings → Pages). ⚠️ You cannot read
  that setting without auth — infer it from a `success` deployment in §1, and say
  in the report that inference is what you did.

## 6 · ⛔ The reading traps this project has already paid for

* **A rendered page is a weak instrument.** Fetching an issue's HTML returned
  "zero comments" three times when there were three, and a whole owner-facing
  finding was built on it. Use `api.github.com`; the list endpoint's own count is
  the control. Repeating one bad method is not independent confirmation.
* **Recorded facts are claims too — re-derive the ROUTE, not the citation.** On
  2026-08-29 a session read `RELEASE_PORTAL_PREP.md` §0.5(c) and concluded Steam
  had never been updated; §0.5(c)'s own sentence said "on a **first** upload", and
  the conclusion was false (`EF-068`). The same session then twice repeated
  STATE's stale "deployed `a97b8b0`" as current when the API said otherwise.
  ⇒ **here, a recorded sha, count or status is a lead; the API and the live page
  are the readings.**
* **Never silently discount a discrepancy.** "Probably just caching" is an
  attribution verdict, not a dismissal — report it with what you measured and when.

## 7 · Filing (`docs/README.md` "Where new things go")

* A **defect in the pack** found while reading → `agent/bugs/<ID>.md`, then
  **regenerate the INDEX** — it is GENERATED (`split_bugs.load_from_dir()` +
  `render_index()`, mind the trailing newline), never hand-edited.
* An **engine, portal or platform fact** → `agent/facts/EF-###.md` with its
  observation date, `lines:` equal to the body length; regenerate the facts INDEX
  the same way.
* **The audit itself** → `agent/reports/`. ⚠️ Reports are not authority — when a
  report and an entry or fact disagree, the entry/fact wins.
* **Anything the owner must press, decide or upload** → `docs/PLAYTEST_CHECKLIST.md`
  → "Decisions waiting on you", never only an agent doc.
* `python tools/doccheck.py` **GREEN before any doc commit**; a WARN line is copied
  **VERBATIM** into the owner summary. STATE.md is byte-capped, so adding a line
  means evicting a resolved one to `archive/SESSION_LOG.md` in the same commit —
  and `archive/` is append-only: correct it with a NEW leg, never an edit.
* Commit with `git commit -F <file>` (embedded quotes split under PS 5.1), then
  push — pushing is standing-allowed and is not publishing.

## 8 · The report

Lead with the deployed sha from §1 and the three numbers from §2. Then: what is
committed but not deployed, what is inconsistent on the live site, what links
fail, and what the owner must press. ⛔ **If everything is clean, say so plainly**
— this sheet exists to be able to return "nothing owed", and padding it with
speculative findings is the failure mode that wastes the owner's attention.
