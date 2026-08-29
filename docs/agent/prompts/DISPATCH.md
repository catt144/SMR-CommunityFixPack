# Dispatch — general-purpose orientation (model-agnostic) — written 2026-08-29

Paste into a fresh Claude Code session for **ad-hoc work that is not a sitting**:
a code question, an investigation, a bug check, a new finding, a new report, a
triage of something the owner noticed. **Any model; the owner picks per task.**
**Start with `git log --oneline -10` + `git pull`** — the tree moves and this
file, like every record, goes stale the moment another session commits.
Staleness anchor: **written 2026-08-29**; verify against `git log` before trusting
any specific it names.

> ⛔ **THIS IS AN ORIENTATION, NOT A LOGBOOK.** It carries no result, no status,
> no entry ID — those live in the entries, the checklist and `STATE.md`. The only
> edits it takes are corrections to its own instructions. A sitting's lesson goes
> to its proper home (see §3), never here.

> 🧭 **THIS IS THE CATCH-ALL. If the task has a dedicated prompt, SWITCH TO IT** —
> this one only orients and routes. The dedicated ones (§4): a **live playtest**,
> an **upload**, a **post-upload close**, a **public-doc sweep**, **drone** work,
> a **multi-session effort**, a **STATE eviction**. Everything else — one defect,
> one question, one report — is dispatch, and stays here.

You are doing focused, self-contained work in a bug-fix mod for Surviving Mars:
Relaunched (every fix repairs a **verified** defect in the game's shipped Lua,
patched at runtime; no game files are modified). The map is `docs/README.md`.

## 0 · Orient (before you touch anything)

1. `git log --oneline -10` + `git pull` — know what landed since this file's date.
2. **Read `docs/agent/STATE.md`** — the mandatory current-state kernel (gates,
   holds, counts, the active line of work). Every session reads it.
3. Scan `docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md` — one-line rows,
   so you know what already exists (several behaviours are the opposite of what the
   code suggests). Open only the entry/fact files the task touches.
4. ⚠️ **If — and only if — the task launches the retail game for a reading**, the
   STALE-PROBE GATE binds first: `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`,
   put it in your todo list, and CLEAN = zero hits (or every hit declared by this
   session's design). A pure investigation or a doc change launches nothing and
   skips this.

## 1 · The bindings that never bend

- **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\Project
  Spark`). `ModTools\Src` is **read-only truth** for line numbers — cite it, never
  edit it. Check `Mars.exe` is NOT running (`tasklist`) before touching loadable
  code, in a separate step from the edit.
- **Any code you write is `FIX_POLICY.md`'s** — §4a who-benefits, §3a save-safety,
  §2 enable-path/declaring-class, §1 fix-shape — and **judged by enumeration, never
  by an entry's own words.** Before writing ANY new fix, open
  `reports/REACHABILITY_AUDIT.md` "Challenge review" (tier vocabulary, hard tells,
  injection-evidence rule).
- **Parse-sweep every Lua change** before you trust it: `python` + `luaparser`
  (`tools/` has no dedicated wrapper — `from luaparser import ast; ast.parse(...)`).
- **`python tools/doccheck.py` must be GREEN before any doc commit** (red blocks;
  set up once: `git config core.hooksPath tools/hooks`). Counts come from
  `doccheck.py --emit-counts`, **never hand-typed**.
- **Commits:** `git commit -F <file>` (embedded quotes split under PS 5.1),
  project author config, then **push** — pushing the four project repos is
  standing-allowed and is not publishing. ⛔ TestKit is local-only BY DESIGN.
- **Account state and counts: READ them, never assume** — the live `fix pack
  present: N/N` line and `SMRFixPack.ListFixes()` are the only valid reads; the
  totals move.

## 2 · The judgment rules (the ones the project has been burned on)

- **Challenge the cause before filing.** The owner expects a *control*, not a
  plausible story; state the root cause only when a check pins it.
- **Recorded facts are claims too** — re-derive the ROUTE, not just the citations.
  The project has been wrong in both directions in one week with every cited line
  right both times.
- **Never silently discount a log line.** "Not caused by our leg" is an attribution
  verdict, not a dismissal — report unexplained lines VERBATIM with their age.
- **"You can X" needs a route check** — verify a real user can walk the steps on
  each surface; a citation proving the mechanism exists is a different check.
- **Close cases completely.** "Refuted" requires the condition was SAMPLED, not
  that a count happened to be zero. Don't pre-decline a cheap confirmation.
- **Post-launch is patch-note maintenance, NOT the pre-release gate** (owner
  ruling). A single added/changed fix costs an `items.lua` entry (H-10), one boot
  `applied` line, and doccheck counts — never quote `FIX_POLICY` §3a's per-module
  gate cost; run B / lens sweep / audit return only for a **major overhaul**.
- **Design-flavoured calls go to the OWNER, not into an agent doc.** "Is this a
  defect or a rebalance? who benefits?" is `FIX_POLICY` §4a's and the owner's —
  route it to `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you". A **mechanical**
  repair may land same-day, but only WITH a re-verified A/B. Anything too big for
  the session gets FILED (an entry), never half-started.

## 3 · Filing — where a result goes (`docs/README.md` "Where new things go")

- A **defect** → a new `agent/bugs/<ID>.md`. Derive the next id from the files:
  `seq = max(seq)+1`, `row = max(row)+1`; front matter `id, seq, row, title,
  status, status_source, priority, evidence, row_status, updated, copies`. Then
  **regenerate the INDEX** — it is GENERATED, never hand-edited: run
  `split_bugs.load_from_dir()` + `render_index()` and write it (mind the trailing
  newline), then `doccheck` to require an empty diff.
- An **engine fact** → `agent/facts/EF-###.md` with its observation date; keep the
  `lines:` front-matter equal to the body length; regenerate the facts INDEX the
  same way.
- A **report, plan, spec, audit, survey** → `agent/reports/`. ⚠️ Reports are NOT
  authority — when a report and an entry/fact disagree, the entry/fact wins.
- A **rule that binds future work** → `WORKFLOW.md` (process) or `FIX_POLICY.md`
  (code), never buried in a report.
- A **decision the owner must make** → the checklist, never only an agent doc.
- A **session leg** → `archive/SESSION_LOG.md` (append-only, newest first).

## 4 · Route table — hand the task to its own prompt

| the task is really… | switch to |
|---|---|
| a LIVE playtest at the keyboard | `prompts/GENERAL_USE_PROMPT.md` |
| putting an update live (pack/upload/store/site) | `UPLOAD_WORKFLOW.md` (+ `reports/RELEASE_PORTAL_PREP.md`) |
| closing out after a listing exists | `prompts/POST_UPLOAD_CLOSE.md` |
| updating public-facing docs / cards / site | `prompts/PUBLIC_SURFACE_SWEEP.md` |
| the drone system | `prompts/DRONE_PROJECT_PROMPT.md` |
| an effort larger than ~2 sessions | `reports/CHAIN_METHOD.md` (propose a chain) |
| STATE is over its byte cap | `prompts/STATE_EVICTION.md` |

## 5 · End of session

Update `agent/STATE.md` **only if the current-state kernel actually changed** —
it is BYTE-capped by doccheck, so adding a line means evicting a resolved one to
`archive/SESSION_LOG.md` in the same commit; a doccheck WARN is copied VERBATIM
into the owner summary; never evict open gates, holds, owner decisions or the
counts block. Route the session's lesson to its §3 home. Then commit, push,
summarize — and if work was FILED rather than finished, say where.
