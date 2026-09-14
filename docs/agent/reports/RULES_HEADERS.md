# RULES_HEADERS — inventory and owner-gate proposal

Analysis only, 2026-09-14. No binding rule, header, kernel line, checker or prompt lifecycle has changed. The owner authorized finishing the inventory with X1 unresolved after the earlier partial stop. Migration is still awaiting explicit approval.

SOURCE anchor: `86c639994044ed07b29fd869013f4b7cf286a131`. All inventoried source bytes still match this anchor. Packaging HEAD: `86c639994044ed07b29fd869013f4b7cf286a131`. Executed agent: Codex, from transcript identity; a precise serving-model identifier is not exposed and is not inferred. No subagents used.

The full [inventory attachment](RULES_HEADERS_INVENTORY.json) contains every counted excerpt, file/line, source SHA-256, heading context, exclusive class, duplicate pair, dead proof, exact candidate header and simulated STATE. Quotes preserve working-source bytes; with core.autocrlf=true, anchored git comparisons normalize only CRLF to LF. Both blob and working hashes are recorded. Future moves must preserve the exact excerpt in the working tree and exact text after git line-ending normalization. Recheck source inheritance with `git diff --stat 86c639994044ed07b29fd869013f4b7cf286a131..HEAD -- CLAUDE.md docs/README.md docs/agent/STATE.md docs/agent/WORKFLOW.md docs/agent/FIX_POLICY.md docs/PLAYTEST_HELP.md docs/UPLOAD_WORKFLOW.md docs/PLAYTEST_CHECKLIST.md docs/agent/prompts/perma tools/doccheck.py`; unchanged paths need no re-read.

## Coverage and counting

Reviewed the scoped Markdown documents in full and the checklist preamble only (lines 1–44, before the decisions H2). tools/doccheck.py was reviewed for the byte-cap model and owner-only temporary-cap guard. Archive bodies, one-offs, chain payloads and checklist decision bodies were excluded. Nothing in the open marker-enforcement decision was adjudicated.

Verbatim imperative occurrence or inseparable same-scope rule group; supporting context in quote is not another rule. Counts are not unique policies or atomic predicates. Records/measurements/pointers/examples excluded. Duplicate and dead clauses separated when adjacent live duties differ.

Declarative content contracts such as reference-only/work-list-only constrain edits and are counted. Menu descriptions, live status, fixture predictions, observed costs, dated rulings and bare routing pointers are not new rules. Operational instructions inside procedures are task-local. This inventory is a manual scope judgment, not a grep of warning glyphs. A quotation can preserve explanatory prose without counting that prose as another imperative.

The definitions matter: editing this prompt and executing its task are different scopes. PUBLIC_SURFACE_SWEEP §2 says “this file” about STORE_CARD_LIVE, not about PUBLIC_SURFACE_SWEEP. FIX_POLICY §5 expressly says kept, not deleted; opt-ins moving is not grounds to delete it. A conditional cloud hold can reapply and is not called dead merely because currently lifted.

## Counts — derived from attachment members

Measurement: `python -X utf8 C:/Users/stkot/AppData/Local/Temp/rh_finish.py`, anchored at `86c639994044ed07b29fd869013f4b7cf286a131`; filter is the explicit scoped manual selections stored in attachment.rules. Portable recheck: load the attachment, Counter each member.classification, and Counter by member.file; total must equal len(rules). Source hashes and exact excerpt membership are separately verified against anchored git blobs.

| Class | Occurrences |
|---|---:|
| doc-local | 30 |
| task-local | 780 |
| global | 16 |
| redundant | 20 |
| dead | 6 |
| **Total** | **852** |

| Document | Doc-local | Task-local | Global | Redundant | Dead | Total |
|---|---:|---:|---:|---:|---:|---:|
| CLAUDE.md | 0 | 4 | 2 | 2 | 0 | 8 |
| docs/README.md | 0 | 13 | 0 | 1 | 0 | 14 |
| docs/agent/STATE.md | 4 | 22 | 1 | 3 | 0 | 30 |
| docs/PLAYTEST_CHECKLIST.md | 2 | 0 | 0 | 0 | 0 | 2 |
| docs/agent/WORKFLOW.md | 0 | 123 | 10 | 0 | 0 | 133 |
| docs/agent/FIX_POLICY.md | 1 | 100 | 0 | 0 | 0 | 101 |
| docs/PLAYTEST_HELP.md | 1 | 71 | 0 | 2 | 0 | 74 |
| docs/UPLOAD_WORKFLOW.md | 2 | 35 | 0 | 0 | 0 | 37 |
| docs/agent/prompts/perma/CO_RUNS.md | 0 | 51 | 0 | 0 | 0 | 51 |
| docs/agent/prompts/perma/COMBINED_SITTING.md | 2 | 32 | 0 | 1 | 1 | 36 |
| docs/agent/prompts/perma/DISPATCH.md | 1 | 26 | 0 | 2 | 0 | 29 |
| docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md | 1 | 45 | 0 | 0 | 0 | 46 |
| docs/agent/prompts/perma/GENERAL_USE_PROMPT.md | 1 | 14 | 0 | 1 | 0 | 16 |
| docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md | 6 | 30 | 3 | 5 | 1 | 45 |
| docs/agent/prompts/perma/LINUX_DISPATCH.md | 2 | 27 | 0 | 1 | 0 | 30 |
| docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md | 1 | 21 | 0 | 0 | 3 | 25 |
| docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md | 0 | 65 | 0 | 0 | 1 | 66 |
| docs/agent/prompts/perma/RELEASE.md | 1 | 31 | 0 | 1 | 0 | 33 |
| docs/agent/prompts/perma/RELEASE_OUTBOX.md | 3 | 1 | 0 | 0 | 0 | 4 |
| docs/agent/prompts/perma/SITE_AUDIT.md | 0 | 35 | 0 | 0 | 0 | 35 |
| docs/agent/prompts/perma/SMRTK_SLOTS.md | 1 | 11 | 0 | 0 | 0 | 12 |
| docs/agent/prompts/perma/STATE_EVICTION.md | 1 | 23 | 0 | 1 | 0 | 25 |

## Redundancy — quoted pairs and proposed homes

Only the quoted overlapping duty is proposed for removal/pointer replacement. Extra obligations in the source paragraph remain. Canonical occurrences retain their substantive class. Generic verification rails are not claimed duplicates of particular API instruments.

### R1 · Mandatory STATE bootstrap

Proposed canonical home: CLAUDE.md bootstrap, mirrored AGENTS.md. Keep the entry bootstrap; a rule inside STATE cannot discover itself. The map READ FIRST label and layout pointers are not extra occurrences.

`CLAUDE.md:3` — CLAUDE.md:5–6

> **Mandatory read, every session: `docs/agent/STATE.md`** —
> build state, open gates, active holds.

`docs/agent/prompts/perma/DISPATCH.md:32` — docs/agent/prompts/perma/DISPATCH.md:32–33

> 2. **Read `docs/agent/STATE.md`** — the mandatory current-state kernel (gates,
>    holds, counts, the active line of work). Every session reads it.

### R2 · Doccheck GREEN before document commits

Proposed canonical home: WORKFLOW.md rule 7. The source-generated-file procedure is separate. Task-specific gate sequences remain procedures.

`docs/agent/WORKFLOW.md:103` — docs/agent/WORKFLOW.md:103–104

> 7. **Run `python tools/doccheck.py` before committing doc changes** — red
>    blocks. One-time setup: `git config core.hooksPath tools/hooks`.

`CLAUDE.md:19` — CLAUDE.md:19–20

> Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up
> once: `git config core.hooksPath tools/hooks`.

### R3 · Owner decisions mirrored to checklist

Proposed canonical home: WORKFLOW.md rule 5; existing checklist/register pointers remain. Canonical adds marker/update/regeneration duties; only the common mirroring clause is redundant.

`docs/agent/WORKFLOW.md:54` — docs/agent/WORKFLOW.md:54–62

> 5. **Owner-decision mirroring (R10).** Every item needing the owner's call is
>    mirrored into `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"
>    (one line + pointer), and struck the moment it is decided. **An owner
>    decision recorded only in an entry or a report is not considered asked.**
>    **Changing an item's status ALSO means updating its marker.** Update the
>    checklist's `<!-- ck:N status:... owner:... -->` marker in the same edit,
>    including whether an action is still owed by the owner. Regenerate the
>    owner register after editing its source; for the contained regeneration
>    route, see "Writing in a shared tree" below.

`CLAUDE.md:23-decision` — CLAUDE.md:23–25

> **Owner decisions go in
> `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only in agent
> docs.**

`docs/README.md:95` — docs/README.md:95–96

> - A **decision the owner must make** → `PLAYTEST_CHECKLIST.md` →
>   "Decisions waiting on you". Never only in an agent doc.

`docs/agent/prompts/perma/DISPATCH.md:127` — docs/agent/prompts/perma/DISPATCH.md:127–127

> - A **decision the owner must make** → the checklist, never only an agent doc.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:229` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:229–230

> - **Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, never only in agent
>   docs; `docs/WAITING_ON_YOU.md` is the generated view of them (§2a).

`docs/agent/prompts/perma/STATE_EVICTION.md:105` — docs/agent/prompts/perma/STATE_EVICTION.md:105–105

> - Owner-facing asks always live in the checklist, never only here or in STATE.

### R4 · Handoff retirement requires the owner, even when list empty

Proposed canonical home: HANDOFF_ORCHESTRATOR.md rules header. The reminder repeats 11+16; do not weaken the empty-list ask trigger or owner-only retirement.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:16` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:16–18

> ✅ **What a session MAY do:** when §2's list is genuinely empty — every loose end closed or
> homed elsewhere — **ASK the owner whether to retire it**, in one line, and carry on. Their
> answer is the only thing that closes this file.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:20` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:20–22

> ⇒ An empty list is a **prompt to ask**, never a licence to act. ⛔ Do not treat an
> inherited "removal condition MET" note as authority; the condition being met is exactly
> when the question gets asked, not when the deletion happens.

### R5 · Restore editor-stripped comments before committing metadata/items

Proposed canonical home: RELEASE.md §4 (POST_UPLOAD_CLOSE implementation). The check and prohibition match; historical counts do not become a policy.

`docs/agent/prompts/perma/RELEASE.md:134` — docs/agent/prompts/perma/RELEASE.md:134–137

> ⇒ **Until this step has run, NO session may commit `metadata.lua` or `items.lua` for any
> other reason.** A commit that names either file takes its working-tree content, so an
> unrelated edit would silently bury ~400 lines of load-bearing commentary. Check with
> `grep -c '^\s*--' metadata.lua items.lua` — **0 means the restore is still owed.**

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:193` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:193–196

> 3. ⛔ **After an upload, the Mod Editor writeback STRIPS EVERY COMMENT from `metadata.lua` and `items.lua`**
>    (v10: 319 → 0 and 51 → 0). ⛔ **No session may commit either file until `POST_UPLOAD_CLOSE.md` has restored
>    them** — a commit naming the path takes its working-tree content and buries ~400 lines. Check:
>    `grep -c '^\s*--' metadata.lua items.lua`; **0 means the restore is owed**.

### R6 · Release spans upload and close-out

Proposed canonical home: RELEASE.md opening task contract. Retain the actual §2 HOLD/continuation marker and §4/§5 steps; they implement the policy.

`docs/agent/prompts/perma/RELEASE.md:14` — docs/agent/prompts/perma/RELEASE.md:14–20

> > ⭐⭐ **THIS PROMPT SPANS THE OWNER'S UPLOAD — it does not end at the handoff**
> > (owner ruling, 2026-09-13). §1 writes the words, **§2 HOLDS and waits for the
> > owner**, then §4–§5 close out: ids written back, `metadata.lua`'s stripped
> > comments restored, counts re-emitted, STATE updated, **outbox cleared**. The
> > close-out is **part of this prompt's job**, never a separate errand the owner has
> > to remember to fire. ⚠️ A different session usually resumes at §4 — §2 leaves the
> > marker that lets it. **The release is finished at §6, not at §2.**

`docs/agent/prompts/perma/RELEASE.md:86` — docs/agent/prompts/perma/RELEASE.md:86–90

> ⛔⛔ **THIS IS A PAUSE, NOT AN ENDING (owner ruling, 2026-09-13).** §4 and §5 are part of
> THIS prompt's job, not a separate errand the owner has to remember to fire. A release
> that stops here leaves the outbox uncleared, the ids unwritten and `metadata.lua`'s
> comments stripped — which is exactly what happened on v10 (2026-09-12), where the
> close-out went unrun until a later session noticed the writeback sitting uncommitted.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:224` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:224–226

> - ⭐ **`perma/RELEASE.md` SPANS the owner's upload and is finished at §6, not §2** — the close-out is part of
>   its job, never a separate errand. A release that stops at "ready to upload" leaves the outbox uncleared and
>   `metadata.lua`'s comments stripped (trap 3).

### R7 · STATE holds status and pointers, no derivation

Proposed canonical home: STATE.md rules header. STATE_EVICTION adds five-section placement; that specialisation is not a duplicate.

`docs/agent/STATE.md:3` — docs/agent/STATE.md:3–3

> Kernel only: status + pointer, never derivation.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:227` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:227–227

> **`STATE.md` is a kernel: status + pointer, never derivation.**

### R8 · Game/source directories read-only

Proposed canonical home: DISPATCH.md §1; task-reading pointers stay. GENERAL repeats the game-only subset; LINUX repeats both directories. Version stamps, archiving, running-game checks and evidence-folder protections are separate.

`docs/agent/prompts/perma/DISPATCH.md:45` — docs/agent/prompts/perma/DISPATCH.md:45–56

> - **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\Project
>   Spark`) **or the source archives** (`C:\Dev\SMR-SrcArchive\`). Game source is
>   **read-only truth** for line numbers — cite it, never edit it. ⚠️ **Every
>   citation names its game version.** The live `ModTools\Src` is whatever build
>   is installed (STATE names it); earlier builds are archived one tree per
>   version under `C:\Dev\SMR-SrcArchive\` with a manifest each, and most existing
>   entries describe an OLDER build than the live one (`EF-075`, `EF-083`). ⛔ Never
>   "correct" an existing entry's citation to the live tree — an entry records a
>   defect in a stated version. A build you have not archived yet ⇒ archive
>   `ModTools\Src` FIRST (`C:\Dev\SMR-SrcArchive\README.md`). Check `Mars.exe` is
>   NOT running (`tasklist`) before touching loadable code, in a separate step
>   from the edit.

`docs/agent/prompts/perma/GENERAL_USE_PROMPT.md:50` — docs/agent/prompts/perma/GENERAL_USE_PROMPT.md:50–51

> - **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\
>   Project Spark`); `ModTools\Src` is read-only truth for line numbers.

`docs/agent/prompts/perma/LINUX_DISPATCH.md:128` — docs/agent/prompts/perma/LINUX_DISPATCH.md:128–128

> The game directory and the source archives are never modified (DISPATCH §1).

### R9 · Combined recipe retained after a sitting

Proposed canonical home: COMBINED_SITTING.md rules header. Keep strike-the-moments as a separate editing rule. Old predictions remain historical measurements, not current debt.

`docs/agent/prompts/perma/COMBINED_SITTING.md:5` — docs/agent/prompts/perma/COMBINED_SITTING.md:5–6

> This brief does not delete itself — PT-20 is a
> standing per-era re-check and this is now its measured recipe

`docs/agent/prompts/perma/COMBINED_SITTING.md:450` — docs/agent/prompts/perma/COMBINED_SITTING.md:450–451

> **This brief does NOT delete itself** — PT-20 is a standing per-era re-check and
> this is now its measured recipe.

### R10 · No trailing comments in console snippets

Proposed canonical home: PLAYTEST_HELP.md console rules. 319 also requires one-command-at-a-time authoring; retain that distinct instruction rather than delete its whole paragraph.

`docs/PLAYTEST_HELP.md:253` — docs/PLAYTEST_HELP.md:253–259

> - **ONE command per line** — a pasted multi-line block silently concatenates
>   into one line and fails `not understood`. And `not understood` means the
>   line did not COMPILE — overwhelmingly a `--` comment inside a `*r`/`*g`
>   snippet (they splice onto one line); never write a console snippet with a
>   trailing comment. Bare expression for simple reads; `*r`/`*g` for
>   multi-statement snippets and assignments (an assignment is not an
>   expression).

`docs/PLAYTEST_HELP.md:312` — docs/PLAYTEST_HELP.md:312–318

> - ⚠️ **NEVER put a `--` comment in a `*r` / `*g` snippet** (found the hard way
>   2026-07-29). Those rules splice your code into a template **on one line**:
>   `CreateRealTimeThread(function() %s end) return` (`uiConsole.lua:360`). A
>   trailing comment therefore swallows the closing `end) return`, the chunk will
>   not compile, no rule matches, and the console answers **`not understood`**
>   (`console.lua:24`). The same goes for annotations like `--> nil` pasted from
>   documentation.

### R11 · Never read MarsDebug tally as retail tally

Proposed canonical home: PLAYTEST_HELP.md MarsDebug section. Heading repeats the body; detailed build/lens explanation stays.

`docs/PLAYTEST_HELP.md:608` — docs/PLAYTEST_HELP.md:608–624

> **The debug build's `87/87` is not a better version of retail's `78 PASS / 9
> SKIP` — it is a DIFFERENT measurement, and for at least one probe a misleading
> one.** `TechDescriptionBuilding` SKIPs on retail (`the tech has no description
> T`) and **PASSes on MarsDebug** (`description names Underground Medium Dome`).
> That is not the probe improving: it is **F98** — `T(id, text)` discards the
> replacement literal in a non-dev build (`localization.lua:250-252`) but keeps it
> in a dev build, so `Fix_TechDescriptionBuilding` genuinely works here and is a
> no-op in the build players use. The probe therefore reports green in the only
> environment where the fix works and is silent in the one that matters.
> **Quoting "87 PASS" as evidence the pack is healthy on retail would be wrong,
> specifically about F25/F98.** Retail coverage was `78/87` in the single-mod era;
> ⛔ **as of 2026-08-13 the suite is 94 probes and the both-mods retail read is
> `78 PASS / 16 SKIP` (measured, log `archive/rs_r0_*`)** — the six SKIPs added
> since the 88-probe era are the Save Rescue probes standing down because that
> separate rescue mod is not part of your standing rig (with it loaded the same
> run reads `84 PASS / 10 SKIP`). SKIPs enumerated BY NAME in `agent/STATE.md`
> — the non-reporting set is known and enumerated; that is the number to quote.

`docs/PLAYTEST_HELP.md:606` — docs/PLAYTEST_HELP.md:606–606

> ### ⛔ NEVER read a MarsDebug tally as a retail tally

### R12 · Tracker through JSON API, never HTML

Proposed canonical home: PUBLIC_SURFACE_SWEEP.md §4; explicit tracker-reading pointer in STATE. Canonical preserves issue-list comment-count positive control and comments endpoint, rather than merely generic R-A verification.

`docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:328` — docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:328–341

> * ⛔⛔ **READ THE TRACKER THROUGH THE JSON API, NEVER THROUGH THE ISSUE PAGE.**
>   ```
>   api.github.com/repos/catt144/SMR-CommunityFixPack/issues?state=all      # state + COMMENT COUNT
>   api.github.com/repos/catt144/SMR-CommunityFixPack/issues/<n>/comments   # the comments
>   ```
>   This sweep's own first run fetched issue #1's rendered HTML **three times**,
>   once with a cache-busting URL, and got **zero comments** every time. There were
>   three — including the posted reply and the reporter thanking us for it. On that
>   reading it reported to the owner that a reporter had been left unanswered, and
>   wrote that into four documents. ⭐ **The control is free and it was skipped:**
>   the list endpoint's `comments` count. If it is non-zero and your reader shows
>   nothing, **your reader is wrong**, not the tracker. Generalise it — a rendered
>   page is a derived surface, and this file's whole doctrine is that derived
>   surfaces are checked against the record, not trusted.

`docs/agent/STATE.md:49` — docs/agent/STATE.md:49–49

> - ⛔ Read the GitHub tracker via `api.github.com/.../issues/<n>/comments`, never the HTML page.

### R13 · Read deployment API instead of stored deployed SHA

Proposed canonical home: SITE_AUDIT.md §1; explicit deployment-reading pointer in STATE. 37 invokes §1; 53/60 define newest successful deployment and endpoint. This is not equated with the broader R-A rule or Actions-run SHA.

`docs/agent/prompts/perma/SITE_AUDIT.md:37` — docs/agent/prompts/perma/SITE_AUDIT.md:37–39

> 2. Read `docs/agent/STATE.md`. ⛔ **Its "deployed = <sha>" line is a claim with a
>    date on it, not a reading.** Re-derive it in §1 — on 2026-08-29 that line was
>    four days and two deploys stale, and a session repeated it twice as current.

`docs/agent/STATE.md:50` — docs/agent/STATE.md:53–53

> ⛔ Never quote a stored "deployed = <sha>"; read the deployments API (`perma/SITE_AUDIT.md`).

### R14 · No fredware name on player surfaces/no load-order advice

Proposed canonical home: SITE_AUDIT.md §4 + FIX_POLICY.md §8; player-surface pointer in STATE. Issue-reply exception in PUBLIC_SURFACE_SWEEP 314-315 must be preserved; do not expand the exception silently.

`docs/agent/prompts/perma/SITE_AUDIT.md:114` — docs/agent/prompts/perma/SITE_AUDIT.md:114–115

> * ⛔ Never name fredware's mod on a player surface; no load-order advice
>   (`EF-054`, `FIX_POLICY` §8).

`docs/agent/STATE.md:98` — docs/agent/STATE.md:98–98

> - Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).

## Dead instructions — command-supported referents

Proof commands below are small equivalents of the executed Python presence/rg checks; they are re-run directly before packaging. File absence is scoped to the named live target, not a claim that its historical record never existed.

`docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:71` — docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:71–74

> - `STATE.md`: strike the ④ hold and the *NOTHING IS PUBLISHED* line — ⭐ **this is
>   the one moment in this project's history when striking them is correct**
>   (`H-04` exists to stop it happening early; the owner's completed upload is the
>   word it waits for).

Command: `git rev-parse HEAD; rg -n '④|NOTHING IS PUBLISHED' docs/agent/STATE.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; rg exit 1, no matches. Remove only the vanished first-launch hold clause; the live record/count/WARN duties remain.

`docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:79` — docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:79–83

> - ⭐ **Hand off to the opt-in pack** (checklist 68, the owner's stated next
>   priority). Its first session reads **that repo's own STATE** and its standing
>   pre-upload obligation, `reports/PARKED_OPTIN_REFERENCES.md` — ~46 parked
>   passages that restore only when that mod launches, several of them in **this**
>   repo and on the site. ⛔ Do not scope that effort here.

Command: `git rev-parse HEAD; Test-Path -LiteralPath C:/Dev/SMR-OptInPack/docs/agent/reports/PARKED_OPTIN_REFERENCES.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; False. Remove obsolete first-launch kickoff; retain the other-repo scope boundary through the current dispatch.

`docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:96-consume` — docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md:3–3

> `git rm` this file

Command: `git rev-parse HEAD; rg -n 'instruction is retired|step below is void' docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; source line 6 explicitly voids the self-consuming process. File exists; its self-consumption process was retired. Keep commit/push close-out.

`docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:27` — docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:27–37

> **Held follow-through, 2026-09-12 — still-needed sweep (ck156).**
> All 46 modules reviewed; proposed F37/F43 retirement and 14 retained-claim
> corrections are **not applied**. Read `reports/STILL_NEEDED_SWEEP.md` and exact
> `reports/still-needed/SURFACE_PLAN.md`. **TAKEABLE WHEN:** v9 F59/F60 close-out is
> complete and the owner has ruled on retirement/constituency and wording in
> `docs/PLAYTEST_CHECKLIST.md` item156. Then run this whole sheet, including every
> card copy/intro/category/count, and use RELEASE_OUTBOX's **Held after-v9** batch.
> Do not consume it in v9 or equate this audit's report push with public publication.
> **Update 2026-09-12:** v9 is closed and item 156 is RULED — the text to apply is
> `reports/still-needed/WORDING_RULED.md` (owner-ruled; supersedes `SURFACE_PLAN.md`
> where they differ), gated on `prompts/SURFACE_AUDIT_FABLE.md` reporting first.

Command: `git rev-parse HEAD; Test-Path -LiteralPath docs/agent/prompts/SURFACE_AUDIT_FABLE.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; False. Missing one-off gate; this block still claims the now-released batch unapplied. Keep live site-file owner hold (§1), not this spent batch trigger.

`docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:89-gone` — docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md:89–90

> ③ `prompts/CHECKLIST_ARCHIVE.md` — the checklist cleanup, ruled and never run (ck176); ⚠️ its own brief
> carries the unnumbered-items risk on its face, so read that before firing.

Command: `git rev-parse HEAD; Test-Path -LiteralPath docs/agent/prompts/CHECKLIST_ARCHIVE.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; False. Remove only the gone prompt fire/read instruction; C92 shipping hold and other queued prompts remain.

`docs/agent/prompts/perma/COMBINED_SITTING.md:421` — docs/agent/prompts/perma/COMBINED_SITTING.md:422–422

> STATE ② cleared and ③ (MOD_DESCRIPTION ×2(+1)) promoted to NEXT.

Command: `git rev-parse HEAD; rg -n '②|③' docs/agent/STATE.md`. Result: HEAD 86c639994044ed07b29fd869013f4b7cf286a131; rg exit 1, no matches. Remove old release-state promotion, not the reusable recipe or earned checklist/status/log recording.

## Header specification — approval requested

Immediately after H1 and its blank separator, before prose, exactly one block on each approved Markdown document:

```markdown
<!-- RULES -->
visible rules governing edits to this document
<!-- /RULES -->
```

Proposed warning **1,536 B**, hard **2,048 B**. Count raw UTF-8 bytes from the first byte of the opening marker through the closing marker and its newline, including source wrapping/blank lines and CRLF bytes. Exact marker lines, one pair, ordered, nonempty visible interior. Preserve verbatim wrapping and blockquotes; allow a same-scope rule to span lines rather than rewrite it into a mandatory single-line format. This departs from the sketch to preserve meaning and source bytes.

RULES HEADERS would be RED for a missing/duplicate/reversed marker pair, wrong placement, empty block, invalid UTF-8 or a listed block above 2,048 B; WARN above 1,536 B. The checker uses an explicit approved Markdown allowlist. Unlisted files receive no empty block. An unexpected marker block should be RED to prevent an unreviewed expansion of the header list. Preserve existing STATE caps, generated-file checks and owner-only temporary-cap switch.

The check cannot tell whether an agent read the header, understood it, obeyed it, or whether the human inventory captured every semantic rule. It does not validate canonical pointer scope or turn prose hazards into machine gates. Task agents still read the task procedures they are executing. After approval, watch structural failures on isolated broken copies (missing/reversed/duplicate/empty/oversized/wrong position), verify warning boundary, restore by hash and run doccheck GREEN. No structural checker has been implemented during analysis.

## Proposed document list

| Header | Bytes | Reason |
|---|---:|---|
| docs/agent/FIX_POLICY.md | 568 | Explicitly protects §5 against deletion, despite opt-ins moving repos. |
| docs/PLAYTEST_HELP.md | 455 | Reference-only content contract; tests belong in checklist. |
| docs/PLAYTEST_CHECKLIST.md | 1692 | Work-list-only content and whole-body section retirement; preserve the open marker enforcement question verbatim. |
| docs/UPLOAD_WORKFLOW.md | 427 | Upload-only content and backup-copy matching constraint; sweep-update duty stays in task body. |
| docs/agent/prompts/perma/DISPATCH.md | 323 | Only corrections to instructions; no results/status/logbook. |
| docs/agent/prompts/perma/GENERAL_USE_PROMPT.md | 387 | Only instruction corrections; same-commit lessons go to their other homes. |
| docs/agent/prompts/perma/RELEASE.md | 84 | Reusable; do not remove after a release. Incorrect Unlike POST_UPLOAD_CLOSE comparison is excluded as stale context. |
| docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md | 371 | Reusable lifecycle; explicit voiding of its old self-consumption step. |
| docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md | 147 | Reusable and updated in place after drone sessions. |
| docs/agent/prompts/perma/COMBINED_SITTING.md | 180 | Standing measured recipe retained after moments taken. |
| docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md | 1537 | Owner-only retirement, active-only content, Linux routing, generated owner-list ban and no copied toolkit manifest. |
| docs/agent/prompts/perma/LINUX_DISPATCH.md | 711 | Standing lifecycle, situation updates in place and explicit retirement condition. |
| docs/agent/prompts/perma/RELEASE_OUTBOX.md | 733 | Append pending entries, clear through release, no silent deletion. |
| docs/agent/prompts/perma/SMRTK_SLOTS.md | 99 | Standing prompt updated in place, never consumed. |
| docs/agent/prompts/perma/STATE_EVICTION.md | 68 | H1 explicitly forbids deletion after a run. |
| docs/agent/STATE.md | 307 | Kernel-only content, emitted build counts and protected owner-register syntax. |

Exact interiors and source IDs are in attachment.headers; the STATE text there is a simulation. No header exceeds hard cap. Initial headers above warning are: docs/PLAYTEST_CHECKLIST.md (1692 B), docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md (1537 B). These WARNs are explicitly part of the proposal; do not shorten binding wording to hide them.

| No header | Reason |
|---|---|
| CLAUDE.md | General bootstrap/folder/source-trust procedures; no imperative specifically governs edits to this entry file. AGENTS mirror unchanged unless later separately approved cleanup. |
| docs/README.md | Filing/search/translation procedures govern other work; no editing-only constraint on the map. |
| docs/agent/WORKFLOW.md | General authoring/testing/release protocols govern named work across files; no editing-only rule for WORKFLOW. |
| docs/agent/prompts/perma/CO_RUNS.md | Situational co-run procedure; evidence/save safeguards bind execution, not edits to this recipe. |
| docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md | Task rules govern other surfaces and audit execution; no editing-only rule for this prompt. "This file" under §2 refers to STORE_CARD_LIVE. |
| docs/agent/prompts/perma/SITE_AUDIT.md | Site audit execution rules; no constraint specifically on editing this audit prompt. |
| tools/doccheck.py | Python checker model, not a Markdown document. Owner-only temporary-cap guard retained. |
| AGENTS.md | Generated byte-identical mirror of CLAUDE; no independent editing/header migration. |

## Stand-alone wording and presentation changes — separate approval

These are proposals, not verbatim moves. Rejecting any leaves its existing rule and binding scope intact.

### E1 · docs/agent/STATE.md

Before:

> ⛔ This enumeration feeds `WAITING_ON_YOU.md` — keep the
>   literal `STILL OPEN:` and `Owner OWES: ck##` idioms, or the owner's register silently drops items.

After:

> Keep the literal `STILL OPEN:` and `Owner OWES: ck##` idioms when editing owner enumerations; `WAITING_ON_YOU.md` reads them.

This enumeration would lose its referent in the header; preserve literal parser idioms and editing scope.

### E2 · docs/agent/prompts/perma/STATE_EVICTION.md

Before:

> # STATE_EVICTION — standing cleanup prompt (reusable; do not delete after a run)

After:

> Reusable; do not delete after a run.

Keep H1 as title; its parenthetical lifecycle constraint must stand alone in a header.

### E3 · docs/agent/STATE.md

Before:

> ## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

After:

> Build state — `python tools/doccheck.py --emit-counts`, never hand-typed

Remove only H2 syntax for the rule in the header; leave ## Build state at the count block. Keeping a second instruction-bearing H2 inside the header would violate the five-section format.

## STATE byte effect — conditional on approved pointers and wording

Raw-byte simulation: **12331 → 12274 B; net -57 B**. Candidate header 307 B; the one new kernel line 58 B (existing CRLF included). It reads:

> - Read the rules header of any doc you are about to edit.

Funding: move existing STATE-local constraints into its header, use E1/E3 only if explicitly approved, and replace precisely R12/R13/R14 task restatements with these scoped pointers:

> - Tracker reads: `perma/PUBLIC_SURFACE_SWEEP.md` §4.
> Deployment rechecks: `perma/SITE_AUDIT.md` §1.
> - Player surfaces: `perma/SITE_AUDIT.md` §4 + `FIX_POLICY.md` §8.

The simulation retains the current owner enumeration, every shipping hold, NEXT/OWES obligations, probe debt and emitted count block. It evicts duplicate policy wording, not obligations; it does not squeeze lines to fit. Without approved duplicate removals/rewording, merely moving STATE text within itself saves no bytes and markers plus kernel line add bytes; the affordable net above is not claimed for that fallback.

Current checker warning is **15,360 B TEMPORARY**, permanent warning **12,288 B**, hard **18,432 B**, line cap **200 B**. ck178’s temporary raise expires only on the owner’s word; this task does not retire it. Proposed STATE is under the permanent warning by 14 B. Header-only Stage C and final Stage D arithmetic must both be re-emitted from the then-current source before writing; a peer change invalidates this snapshot.

## Revert risks and unresolved scope

### X1 · MOD_DESCRIPTION live edit versus archive prohibition

Unresolved, already owner-authorized to flag while continuing analysis. Archived successor exists; not dead. No redirect or deletion in base header proposal.

`docs/agent/WORKFLOW.md:153` — docs/agent/WORKFLOW.md:153–155

> 4. One commit per fix or tight group; agent/bugs/ updated in the same commit;
>    MOD_DESCRIPTION.md updated in the same commit as the code change it
>    describes.

`docs/agent/WORKFLOW.md:640` — docs/agent/WORKFLOW.md:640–649

> - MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the
>   ClassicRockets export half; sync the fix list with agent/bugs/ statuses.
>   ⭐ **Add the "judgment calls" section** (owner ADOPTED the relabel proposal
>   2026-08-04: F55, F40, F73(b), F70, F97 presented as design-judgment repairs,
>   not plain bugs) — ⚠️ **its wording is OWED BY THE OWNER** and must be asked
>   for if it does not exist yet; the checklist line tracks it.
>   **Recount the probe number** quoted in the "What we can promise, and what we
>   can't" block — it moves whenever a wave file gains or loses a probe, and a
>   stale number there is a false claim in player-facing text. Authoritative count
>   is in `agent/STATE.md`.

`CLAUDE.md:8` — CLAUDE.md:8–15

> **Folder contract** (doccheck enforces it). `docs/` root holds ONLY the six
> human files (PLAYTEST_CHECKLIST, PLAYTEST_HELP, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,
> FUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`
> (`bugs/`, `facts/`, `reports/`, `prompts/`, STATE/WORKFLOW/FIX_POLICY);
> `docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
> is GENERATED — edit the entry or fact file, never the index** (line-1 banner).
> Prompts: the map is `docs/agent/prompts/README.md`. Reusable prompts live in `prompts/perma/`
> (ad-hoc work: `perma/DISPATCH.md`; all FR-1/Linux work: `perma/LINUX_DISPATCH.md`).

`docs/README.md:100` — docs/README.md:100–100

> - **Spent** anything → `archive/`, which is append-only and never edited.

### X2 · Standing entry folder allowlist omits generated owner register

README map includes WAITING_ON_YOU; doccheck accepts it. Correcting the entry contract is a separate explicit wording decision; no header copying the incomplete list.

`CLAUDE.md:8` — CLAUDE.md:8–15

> **Folder contract** (doccheck enforces it). `docs/` root holds ONLY the six
> human files (PLAYTEST_CHECKLIST, PLAYTEST_HELP, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,
> FUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`
> (`bugs/`, `facts/`, `reports/`, `prompts/`, STATE/WORKFLOW/FIX_POLICY);
> `docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
> is GENERATED — edit the entry or fact file, never the index** (line-1 banner).
> Prompts: the map is `docs/agent/prompts/README.md`. Reusable prompts live in `prompts/perma/`
> (ad-hoc work: `perma/DISPATCH.md`; all FR-1/Linux work: `perma/LINUX_DISPATCH.md`).

### X3 · Explicit-path commits versus shared-hunk exception

DISPATCH forbids a bare commit; WORKFLOW requires no pathspec on a concurrently edited file. Keep unresolved; future commit-rule pointer cleanup must preserve the exception.

`docs/agent/prompts/perma/DISPATCH.md:72` — docs/agent/prompts/perma/DISPATCH.md:72–78

> - **Commits:** `git add <explicit paths>`, then `git commit -F <file> -- <the
>   same paths>`. ⛔ Never `git add -A`, a directory pathspec, or a bare `git
>   commit`: the index is SHARED between sessions and a bare commit takes a
>   peer's staged work with it (this has already swept a peer's staged rename).
>   `-F` because embedded quotes split under PS 5.1. Project author config, then
>   **push** — pushing the four project repos is standing-allowed and is not
>   publishing. ⛔ TestKit is local-only BY DESIGN.

`docs/agent/WORKFLOW.md:930` — docs/agent/WORKFLOW.md:930–937

> - ⛔ **A pathspec is only HALF a commit fence.** `git commit -- <paths>` protects every OTHER
>   file, but for a path you *name* git commits that path's **working-tree** content — a peer's
>   unstaged edits included (09-12, `cc3edf2`). On a file two sessions are inside at once, stage
>   **your own hunks** (`git add -p`) and commit **without** a pathspec.
>   ⚠️ It cuts both ways: on 09-13 this session's two uncommitted `STATE.md` edits were swept into
>   a peer's commit (`bf2d75f`) seconds later. Nothing was lost, but neither commit message
>   describes what it actually contains. **Re-check `git status` on a shared file immediately
>   before the write, not at the top of the session** — a clean status 20 minutes old is not a fence.

### X4 · Reply part of shipping versus owner pull-only/no release gate

PUBLIC_SURFACE_SWEEP 306 makes reply part of shipping; WORKFLOW 5b forbids unsolicited drafting and gating other work. Propose later pointing reporter section to 5b, with exact before/after separately approved.

`docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:306` — docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md:306–306

> If the fix answers an open field report, the reply is part of shipping it.

`docs/agent/WORKFLOW.md:79` — docs/agent/WORKFLOW.md:79–92

> 5b. **Player replies are PULL-ONLY (R10c, owner ruling 2026-09-12, checklist
>    165).** Rule 5's mirroring obligation ⛔ **does NOT extend to replies to player
>    reports.** Never draft one unasked, never put one on the owner's owed list
>    (`STATE.md`'s OWES line, a handoff's decisions table, a session summary's
>    "waiting on you"), never raise a waiting `DRAFT` as a nudge, and never gate
>    other work on a reply going out. A draft in `docs/FIELD_REPORT_REPLIES.md`
>    waits indefinitely **by design**. When the owner asks for one, write it and
>    stop — one ask, one draft, no follow-on queue. ✅ **This does not touch
>    triage:** a player's report is evidence about a defect, and filing it into
>    `agent/bugs/` is ordinary bug-fixing work that continues unchanged — ⛔ never
>    cite this rule to avoid reading, filing or investigating a report. ⚖️ Condition
>    (per 5a): the owner had fielded a day of reply questions while the project's
>    real gate was an unrun playtest. The cost being cut is **owner attention
>    diverted from fixing bugs**, not the replies themselves.

### X5 · Linux ASK/report-request playbooks versus pull-only reply policy

Clarify whether requested FR-1 triage authorizes a draft/log request; do not create an owed reply from old playbooks. Record both scopes, resolve neither here.

`docs/agent/prompts/perma/LINUX_DISPATCH.md:56` — docs/agent/prompts/perma/LINUX_DISPATCH.md:56–58

> - **Posts (the owner posts; no agent posts).** The original dev post and follow-up 1 are POSTED. "CURRENT DEV NOTE" (it replaces
>   posts 2 and 3) and "PLAYER REPLY" are drafted in the dev-reply doc; whether they were posted is **unknown, so ask**. No dev
>   response as of 09-11.

`docs/agent/prompts/perma/LINUX_DISPATCH.md:66` — docs/agent/prompts/perma/LINUX_DISPATCH.md:66–67

> - (a) If there is no log yet, hand the owner the "PLAYER LOG REQUEST" block (in the dev-reply doc) to post. It has six plain steps,
>   the dump path is `/tmp`, and one grep line prints the result.

`docs/agent/WORKFLOW.md:79` — docs/agent/WORKFLOW.md:79–92

> 5b. **Player replies are PULL-ONLY (R10c, owner ruling 2026-09-12, checklist
>    165).** Rule 5's mirroring obligation ⛔ **does NOT extend to replies to player
>    reports.** Never draft one unasked, never put one on the owner's owed list
>    (`STATE.md`'s OWES line, a handoff's decisions table, a session summary's
>    "waiting on you"), never raise a waiting `DRAFT` as a nudge, and never gate
>    other work on a reply going out. A draft in `docs/FIELD_REPORT_REPLIES.md`
>    waits indefinitely **by design**. When the owner asks for one, write it and
>    stop — one ask, one draft, no follow-on queue. ✅ **This does not touch
>    triage:** a player's report is evidence about a defect, and filing it into
>    `agent/bugs/` is ordinary bug-fixing work that continues unchanged — ⛔ never
>    cite this rule to avoid reading, filing or investigating a report. ⚖️ Condition
>    (per 5a): the owner had fielded a day of reply questions while the project's
>    real gate was an unrun playtest. The cost being cut is **owner attention
>    diverted from fixing bugs**, not the replies themselves.

### X6 · Legacy bare tested wording versus attendance labels

Bare tested is closed to new work; old recipes still grant it. Keep definitions/records separate and do not silently change historic grants during header work.

`docs/agent/WORKFLOW.md:422` — docs/agent/WORKFLOW.md:422–426

>    * ⛔ **`tested` (bare) is LEGACY and closed to new work.** The 46 entries
>      holding it predate this rule and their attendance was never recorded —
>      17 carry the bare word with no narrative at all — so it means "attendance
>      unaudited", not "attended". Do not promote one without re-deriving it
>      from the archived record; do not read one as if it were attended.

`docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md:338` — docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md:338–339

> - **Do not report a module `tested`** without a playtest. Only the playtest flips
>   that status.

`docs/agent/prompts/perma/COMBINED_SITTING.md:385` — docs/agent/prompts/perma/COMBINED_SITTING.md:385–387

> * Not **"D13 is `tested`"** unless the dialogs were actually seen and said so —
>   that grant is the whole point of the attended half, and `tested` still means a
>   pass at the keyboard (WORKFLOW).

### X7 · Release first-launch assumptions remain mixed with current procedures

Major/minor differs from editor version rail, not automatically a contradiction. Old ignore_files-not-in-place and cloud-ON assertions are stale claims, not proven dead rules. RELEASE comparison to reusable POST_UPLOAD_CLOSE is false context; rule remains verbatim.

`docs/agent/WORKFLOW.md:609` — docs/agent/WORKFLOW.md:609–639

> - metadata.lua: bump `version_major`/`version_minor`, refresh `last_changes`.
>   `short_description`, `optional_mod` are already in place (audit 2.1).
>   `lua_revision` stays 350453.
>   ⛔ **`ignore_files` is NOT already in place — owner ruling 2026-08-13
>   (checklist 23), do it in this pass, in ALL THREE mods.** The upload packs the
>   **entire mod folder recursively** and filters only on these patterns
>   (`ModTools\Src\CommonLua\Classes\GedModEditor.lua:678-741`), so everything
>   unlisted ships inside the player's download. Nothing *runs* (only `code`-listed
>   files execute), but `CLAUDE.md` is agent instructions and does not belong on a
>   player's disk. ⭐ 2026-09-10: `AGENTS.md` (the Codex mirror of `CLAUDE.md`)
>   joined the list — `*AGENTS.md` sits in `metadata.lua`'s `ignore_files`, in
>   `tools/pack_predict.py`'s own copy of that list, and in `upload_preflight.py`'s
>   check, all three together; the predictor does NOT read `metadata.lua`, so a
>   pattern added in one place only makes the predicted count lie.
>   ⭐ **Re-derived per mod 2026-08-13 (`public-docs/02_QA.md`) —
>   the three lists are NOT the same:**
>   | mod | add |
>   |---|---|
>   | fix pack | `tools/` · `CLAUDE.md` · `LICENSE` · `.gitattributes` |
>   | opt-in pack | the same four |
>   | **save rescue** | **`LICENSE` only** — it already ships a `*CLAUDE.md`
>     pattern the other two lack, and has no `tools/` and no `.gitattributes` |
>   ⭐ **Copy the rescue mod's `*CLAUDE.md` line into the other two** rather than
>   inventing a pattern. ✅ `.github/` is no longer a question — the fix pack has
>   none since the site moved out, and neither of the others ever had one.
>   ⚠️ **One wildcard question survives and one command settles it:** whether `*`
>   crosses `/` decides whether `*/docs/*` filters the whole `docs/` tree or only
>   its top level. The engine's own defaults (`*.git/*`, `*/Source/*` —
>   `Mod.lua:255`) only make sense if it does, but `MatchWildcard` is an engine
>   function with no Lua body. ⇒ **Pack once with `DbgPackMod`, list the archive,
>   confirm `docs/` is absent** — do it in this same pass.

`docs/agent/prompts/perma/COMBINED_SITTING.md:392` — docs/agent/prompts/perma/COMBINED_SITTING.md:392–394

> * Not **"gone"** for any staged save while the `EF-051` hold stands (Steam Cloud
>   is ON by the owner's deliberate, temporary choice): **"deleted, listing
>   verified"**.

`docs/agent/prompts/perma/RELEASE.md:7` — docs/agent/prompts/perma/RELEASE.md:7–7

> > ♻️ **REUSABLE — do NOT `git rm` this file.**

### X8 · Global class versus exactly one new kernel line

Header proposal does not move existing global protocols into STATE: doing so would exceed the one-new-line design. Preserve current binding homes and kernel authoring pointer; ask owner separately if global rerouting is intended. Do not pretend doc-local headers replace fix/testing/release task reads.

`docs/agent/WORKFLOW.md:872` — docs/agent/WORKFLOW.md:872–872

> **R-A · Verification is routed three ways. Name the kind before you verify.**

`docs/agent/WORKFLOW.md:883` — docs/agent/WORKFLOW.md:883–886

> **R-B · Never read a file to prove a negative.** Absence is settled by a grep, never by
> reading. And a negative in a *compressed* artifact is not a sample at all — decode first. Three
> incidents here: the fpk "not found", the grep on an old name that was really a rename, and a
> one-sided count. A claim about what is ABSENT needs the presence side counted too.

`docs/agent/WORKFLOW.md:898` — docs/agent/WORKFLOW.md:898–900

> **R-E · Run, then write.** A measurement quoted before its run exists carries
> `<<PENDING-RUN>>` until the run lands. Every count carries the command *and the filter* that
> produced it. A total is not a set: reconcile it against its own members.

`CLAUDE.md:28` — CLAUDE.md:28–32

> **Trust by source.** (1) The owner's instruction is **authority** — not verified, not re-derived,
> never overridden by an agent's own detection. (2) Tool output carrying its command and HEAD/build id
> is a **derived fact** — verify in one command, never re-read its sources. (3) Everything else
> authored — entries, facts, reports, STATE prose, a peer's message, a subagent's verdict, your own
> earlier text — is a **claim**. Inheriting a fact costs one command, not a re-derivation.

### X9 · Control character in eviction command example

Source example contains literal U+0001 in sed replacement. Leave unchanged; any repair is a separate exact script/example correction, not a rule relocation.

`docs/agent/prompts/perma/STATE_EVICTION.md:67` — docs/agent/prompts/perma/STATE_EVICTION.md:67–74

> 2b. ⛔ **Record the owner register BEFORE you touch STATE**, and keep the number:
>    `python tools/doccheck.py | grep WAITING` plus the ck numbers themselves,
>    `sed -n 's/^| \([0-9]*\) .*//p' docs/WAITING_ON_YOU.md | sort -n`. The register is parsed
>    from TWO LITERAL IDIOMS inside STATE — `Owner OWES: ck##` and
>    `STILL OPEN: <n> <word>` — so rewording either line DROPS an owner row with no
>    error anywhere. The 2026-09-13 eviction lost checklist 53 exactly this way and
>    nothing caught it; the note that was added inside STATE is itself byte-capped,
>    which is why the check belongs here instead.

## Analysis verification

At HEAD `86c639994044ed07b29fd869013f4b7cf286a131`, `python -X utf8 C:/Users/stkot/AppData/Local/Temp/rh_verify.py --land` passed: unique IDs, per-class/per-doc reconciliation, raw source excerpts, anchored CRLF-normalized text, both source hashes, header byte sizes, STATE delta and 200-byte line cap. All six dead proofs were rerun. Immediately-before-write status contained only this analysis report; only this report and its inventory attachment were written.

Portable count recheck (no temporary script required):

```powershell
python -X utf8 -c "import json; from pathlib import Path; from collections import Counter; d=json.loads(Path('docs/agent/reports/RULES_HEADERS_INVENTORY.json').read_text(encoding='utf-8')); c=Counter(r['classification'] for r in d['rules']); assert c==d['counts']; assert len({r['id'] for r in d['rules']})==len(d['rules']); assert all(Counter(r['classification'] for r in d['rules'] if r['file']==p)==n for p,n in d['per_doc_counts'].items()); print(c,len(d['rules']))"
```

`python -X utf8 tools/doccheck.py` was GREEN at the same HEAD after writing the analysis files. Existing warning text follows verbatim; repeated identical alias warnings are shown once:

```text
  warn F59: the frozen index-row cell says 'fixed*', entry says 'tested-attended' (from 'tag')
  warn F85: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C12: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C13: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C14: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C15: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C16: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C17: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C37: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C35: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C34: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C38: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C39: the frozen index-row cell says 'filed', entry says 'tested-unattended' (from 'tag')
  warn F100: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C43: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C49: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C50: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C51: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C52: the frozen index-row cell says 'filed', entry says 'parked' (from 'tag')
STATE + STUBS: STATE.md 12331 bytes (warn 15360 TEMPORARY, hard 18432, line 200); 3 stubs present and pointing
  ⏳ STATE warn is TEMPORARILY raised +25% (12288 → 15360) by owner ruling 2026-09-14, checklist 178, for the duration of the doc overhaul. Restore: set STATE_WARN_TEMPORARY = False in this file. ⛔ Owner's word only — no agent retires this on its own judgement.
  warn duplicate ck:144 at lines 2733, 2807 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.order is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.probes is defined by no kit file
  WARN UNKNOWN   76_SMRTK_Kit.lua           SMRTest.last is defined by no kit file
```

## Migration units — after owner all-clear

One commit per source doc, with only that source’s approved header/clauses and necessary approved pointers/presentation changes. Recheck status immediately before each write, use exact pathspecs for exclusively owned source files, prove each moved excerpt byte-identical somewhere in the live tree (literal git grep, or raw-byte multiline check plus literal per-line controls), and run doccheck GREEN after each. Any CLAUDE cleanup is a separately announced source+AGENTS regen commit. A global rule or task obligation must not silently become conditional on editing a particular doc.

Checker/kernel land last, once approved headers exist. The new kernel rule is exactly one line; existing global protocols remain in their current binding homes per X8. The final checked report records source commits, measured caps, byte-preservation checks and watched-fail structural check. Consume RULES_HEADERS and its prompt-map row together only once the whole task is complete. No tombstones replace removed clauses.

## Live progress

- [x] Anchor, scoped reads and owner-authorized continuation with X1 unresolved.
- [x] Inventory CLAUDE.md.
- [x] Inventory docs/README.md.
- [x] Inventory docs/agent/STATE.md.
- [x] Inventory docs/PLAYTEST_CHECKLIST.md — preamble only.
- [x] Inventory docs/agent/WORKFLOW.md.
- [x] Inventory docs/agent/FIX_POLICY.md.
- [x] Inventory docs/PLAYTEST_HELP.md.
- [x] Inventory docs/UPLOAD_WORKFLOW.md.
- [x] Inventory docs/agent/prompts/perma/CO_RUNS.md.
- [x] Inventory docs/agent/prompts/perma/COMBINED_SITTING.md.
- [x] Inventory docs/agent/prompts/perma/DISPATCH.md.
- [x] Inventory docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md.
- [x] Inventory docs/agent/prompts/perma/GENERAL_USE_PROMPT.md.
- [x] Inventory docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md.
- [x] Inventory docs/agent/prompts/perma/LINUX_DISPATCH.md.
- [x] Inventory docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md.
- [x] Inventory docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md.
- [x] Inventory docs/agent/prompts/perma/RELEASE.md.
- [x] Inventory docs/agent/prompts/perma/RELEASE_OUTBOX.md.
- [x] Inventory docs/agent/prompts/perma/SITE_AUDIT.md.
- [x] Inventory docs/agent/prompts/perma/SMRTK_SLOTS.md.
- [x] Inventory docs/agent/prompts/perma/STATE_EVICTION.md.
- [x] Review tools/doccheck.py byte-cap model and owner-only temporary-cap guard.
- [x] Classification/count reconciliation against own members.
- [x] Redundancy pass with both instances quoted.
- [x] Dead pass with scoped command evidence.
- [x] Header spec, eligibility and exact byte-measured candidates.
- [x] Package analysis report and attachment; verify anchored source bytes and doccheck.
- [ ] **In progress / blocked waiting:** owner migration gate — shape/caps, doc list, R12–R14 pointers and E1–E3; conflicts X1–X9 remain unresolved unless separately ruled.
- [ ] Migrate docs/agent/FIX_POLICY.md — commit and verify, owner-gated.
- [ ] Migrate docs/PLAYTEST_HELP.md — commit and verify, owner-gated.
- [ ] Migrate docs/PLAYTEST_CHECKLIST.md — commit and verify, owner-gated.
- [ ] Migrate docs/UPLOAD_WORKFLOW.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/DISPATCH.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/GENERAL_USE_PROMPT.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/RELEASE.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/COMBINED_SITTING.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/LINUX_DISPATCH.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/RELEASE_OUTBOX.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/SMRTK_SLOTS.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/prompts/perma/STATE_EVICTION.md — commit and verify, owner-gated.
- [ ] Migrate docs/agent/STATE.md — commit and verify, owner-gated.
- [ ] Conditional duplicate-copy cleanup per source doc — expand units on approval; conflict clauses excluded.
- [ ] Land the single kernel line and verify then-current STATE budget.
- [ ] Implement RULES HEADERS, watch broken-copy failures, restore by hash, doccheck GREEN.
- [ ] Final report with each approved source commit and verification.
- [ ] Consume task prompt and map row in the same commit, after completion.
