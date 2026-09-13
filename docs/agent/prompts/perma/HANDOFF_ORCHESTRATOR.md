# Handoff — session → next session (model-agnostic)

⏳ **TEMPORARY resident of `perma/`** (owner, 2026-09-11): it stays until the pending outbox is empty or the owner says
things have settled, then it is `git rm`'d. **Still true 2026-09-12** — `RELEASE_OUTBOX.md` holds 3 Pending + a Held batch.

⛔ **THIS IS A WORKING DOCUMENT, NOT A SESSION LOG.** History lives in `docs/archive/SESSION_LOG.md` (append-only, newest
first). **If you close something here, DELETE its block** — do not let it accrete. Rewritten end-to-end 2026-09-12 after a
long session; everything settled that day was cut to the checklist and the entries.

⛔ **Verify every specific against `git log` and the tree — the records win, this file is a pointer.** Claude and Codex
sessions both commit here, several at once, and **Codex is invisible to `ListAgents`**.

⛔ **FR-1 is NOT on this handoff.** Every Linux / NVIDIA 580 / workaround-mod item is in `prompts/perma/LINUX_DISPATCH.md`.
The temp workaround mod is LIVE (Steam 3799500849 / Paradox 158711).

## 0 · Orient, then ask

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `docs/agent/STATE.md` ·
`prompts/perma/DISPATCH.md` §0–§3 · `prompts/README.md`. Open a **live todo list**.

**Unless the owner's message names a task, a pasted handoff means ORIENT: summarise and ASK what to take.** Do not execute.

---

## 1 · ⭐ THE ONE THING THE OWNER CAN FIRE RIGHT NOW

**`prompts/SITTING_158.md` — the ck158 sitting, which is the v10 gate.** Written 2026-09-12, **unfired**. Paste it into a
fresh session when the owner is ready to play. It carries the stale-probe gate, the hazards, a **named pass artefact per
leg** so a quiet log cannot read as a pass, and what to do with the result. The owner-facing steps stay in checklist **158**
and are pasted from there.

- **A · C85** minutes, any 1.1.0 colony · **B1 · C89** two seconds, any dome, and it is the real falsifier ·
  **B2 · C89** a fresh colony, 20–30 min of ordinary play (the ⚖️ judgment call the owner asked to watch) ·
  **C · C88** minutes, needs Building Codes → Strict + the Martian Assembly.
- If the owner has ten minutes: **A, B1, C**. Say so before they start B2.
- ⛔ `tested-attended` is **the owner's word to grant** and nothing else grants it.
- ⚠️ `Fix_GhostFarmOxygen` **still ships** — ck156's retirement is staged for v10 and has not landed.

---

## 2 · The v10 critical path, in order

1. ⛔ **ck158, the sitting above.** The only thing between here and v10, and only the owner can do it.
2. **`prompts/perma/RELEASE.md`** over the outbox's **Held** batch + the **3 Pending**. Text = `reports/still-needed/WORDING_RULED.md`
   under the ⚖️ **VOICE RULE**. ⛔ **Re-derive every count once, carry none:** modules ± the retirements, the card count word,
   card headlines, "real defects you cannot see today", **judgment calls three → four (C89)**, and the six `README.md` claims
   staged in `RELEASE_OUTBOX.md`'s batch notes. ⚠️ A **fourth** module changed in v10 with **no public row** — the row-3
   hardening in `Fix_StaleReservations` (§4). Do not go looking for a row for it.
3. **The owner's upload**, then the formatting cleanup pass and the store-card paste backups.
4. **The held site deploy, fired ONCE.** `a061665` (49 rows) has been held since 09-11 for exactly this; the live site shows
   **50** meanwhile, deliberately. ⛔ **Three uncommitted files in `C:\Dev\SMR-CommunityMods` are the owner's to rule on
   first** (`content/faq.md`, `for-modders.md`, `install.md`). **That is a DIFFERENT git repo: do not commit, stash or
   checkout there.** Re-read `git -C C:\Dev\SMR-CommunityMods status --porcelain` rather than trusting this line.

---

## 3 · What is open

### 3a · Owner — only three things, and two are actions not decisions

| | what |
|---|---|
| **158** | ⛔ the sitting = **the v10 gate**. Fire `prompts/SITTING_158.md` |
| **144 (a)** | the owed post-upload boot. ⚠️ ck151 (c) ruled **F52 passage / F54 hub / C83 arrival join it — but only if the loaded colony already has those layouts. Otherwise SKIP THEM BY NAME**; never build a layout to make a check possible |
| **151 (b)** | which sections of `reports/MIGRATION_DEV_REPORT.md` may go to the developers. ⚠️ **ck165 lets the owner defer this indefinitely** — it is messaging. ⛔ Do not raise it |

⛔ **NOTHING ELSE IS OWED BY THE OWNER.** ck98, 133, 135, 137, 138, 140, 141, 142, 47, 53, 73, 157, 159–168 are all ruled or
closed; 148 is deferred by the owner's word; 83–97 were offloaded or resolved (ck167). **Do not rebuild an "owed" list from
an older document** — this one was wrong for most of 09-12 because it inherited a table that contradicted its own closed list.

### 3b · Agent work, needing no ruling

- **C90 — shape RULED, NOTHING BUILT.** Per-module apply-success guards in `Fix_SaintBlessing` + `Fix_SinkholeIndestructible`.
  ⛔ **NOT** the shared core's apply-verdict contract. ⛔ **Never gate on `entry.status == "active"`** — `run_apply` sets status
  only *after* apply returns. Must define reset/retry, not treat a once-true flag as an everlasting verdict.
  Evidence + limits: `reports/DESKBENCH_C90.md`.
- **Migration residuals — the honest list, read from the entries 09-12:** **F51** 1.1.0 PARTIAL, permanent migration-block claim
  not established, leg re-filed **UNRUN** · **F53** PARTIAL, no fresh 1.1.0 evidence · **F59** repaired, **A1 expedition half
  UNTESTED** · **F73** PARTIAL, organic benefit unverified · **F80** still `investigating`, causation unproved · **F54** never
  swept. ✅ F60 retired, C83 `tested-attended`.
- **`treediff` gains a `TABLE-HUNK` list** (`HUNT_AUDIT` §8 item 2). ⭐ **With a requirement discovered 09-12: it must compare
  CONTENT between trees, not POSITION.** The classifier reported a block that merely *moved* as a new `DefineClass`, and
  attributed `__parents` across adjacent blocks — one of seven rows in `reports/PINNED_PARENTS_PASS.md` was pure line-shift.
- **Desk NEXT, unclaimed:** `prompts/DLC_DEEP_CHECK.md` (bounded; framing in its banner).
- **`prompts/SELFCHECK_PILOT.md`** — unreachable since ck133/112; **removal recommended, not done.** Owner's word at any time.
- **83 (SHARED TestKit)** — not owed, not urgent, but two of its five proposals (a `RunAll` owner filter, a `PACK_ID` on the
  enable-path leg) improve the kit **for us** regardless of the opt-in mod.

### 3c · Hotfix 3 — one item

**135 only.** ✅ RULED 09-12: take the `luafn.py` delimiter fix in hotfix 3 — desk tool, **0 shipped hashes**, ⛔ **not v10**.
137/138/140/141/142 closed with ck163 (a). ⛔ Do not re-derive the old table or the expired-triage "tension"; both are gone
on purpose (ck161, and `WORKFLOW.md` rule 5a).

### 3d · Watch list, not tasks

- ⏳ **The Foreign Aid Rocket report (Steam, wgtiii, 2026-09-12).** A rocket stuck "Unloading cargo" with 2 Food, 40 sols,
  won't leave. ⛔ **NOT ours and NOT filed** — the owner messaged the reporter and is waiting. **F119's fix cannot touch it**
  (that is scoped to `FuelResourceAmount` on shipped **trade** rockets; this is a `ForeignAidRocketBase` carrying food).
  Source lead, recorded so it is not re-derived: departure runs through `LeaveForever` (`RocketForeignAid.lua:75-85`), which
  sets `launch_after_unload = true` — so **departure is gated on the unload finishing**, and cargo that can never be placed
  strands the rocket permanently. The reporter's warning list showed **Low Storage**. ⇒ **If they reply, file it as a lead.
  If they do not, the owner's read is that their food storage was full.** Do not chase it.
- **Hardening rows 1 + 2 — DEPRIORITISED by ck53, not closed.** Recorded so nobody re-derives it: `SMRFixPack_Disabled = "yes"`
  passes the `or {}` adoption at `00_Core.lua:13` and every id then reads nil ⇒ **the modder's veto is silently ignored and
  every fix applies anyway**; `= true` throws at that index ⇒ **kills the whole pack, log-only**. Row 2 is the same shape for
  `SMRFixPack_Optional` (`:17`, read at `:57`). ⚠️ A plain `type(x) == "table"` guard is **not** enough alone. Row 4 went to
  C90's build; rows 5–7 dropped; row 8 moot. ✅ **Row 3 is BUILT** (§4).

---

## 4 · Landed 2026-09-12 — pointers only, the reasoning is in the checklist and `SESSION_LOG.md`

| sha | what |
|---|---|
| `59c8c47` `98d0461` `4dc5073` | the three v10 builds: C85 · **C89** (⚖️ judgment call) · C88. Attended check = ck158 |
| `4c7b11a` · `690a1ee`→`1d625e4` | surface audit (ck159) · Astra: F60 harness repaired, C90 measured, deskbench 20/20 |
| `cc3edf2` `7e445d3` `4b6beda` | peer `smr-bugfixpack-b2`: the vanilla-diff disposition, `WORKFLOW.md:156` after-patch section **BINDING**, ck163 |
| `fb87a6e` `e7d1eef` `441cc92` | the §4 loose ends · ⛔ **a correction: my `LAKECHK` "defect" was refuted by a peer** · attribution + the pathspec rule |
| `7351821` | **ck163 (b) RAN — nothing found.** `reports/PINNED_PARENTS_PASS.md`, 7/7 rows clean, option (ii) NOT triggered |
| `ce73f4a` | ⭐ `prompts/SITTING_158.md` — the sitting prompt, unfired |
| `38875a2` | **ck165 — replies are PULL-ONLY** (`WORKFLOW.md` rule 5b) |
| `b162e37` `e4600f2` `5665ee2` | ck166 (133 closed, 135→hotfix 3) · ck167 (opt-in offload, + `11a5528` in `SMR-OptInPack`) · ck168 (98, row 3 built, 151 c) |

**Built 09-12 beyond the three fixes: hardening row 3.** `Fix_StaleReservations`' `OnMsg.NewDay` sweep now runs one `pcall`
**per colonist** — ⛔ not per residence, which would still abandon the rest of that residence's list on one bad slot. A raise
logs the residence handle and slot and the sweep continues; a **separate** line says the sol's sweep was incomplete, kept out
of the "released N" line on purpose. ⚠️ Limit recorded in the module: per `EF-008` `pcall` does **not** catch an `assert()` in
shipped code. ✅ `parsecheck` clean, `desk_f59_expedition.py` **23/23**, no TestKit probe invalidated.

---

## 5 · Method the owner set — inherit this

- ⛔⛔ **REPLIES ARE PULL-ONLY (ck165).** Never draft one unasked, never put one on the owner's owed list, never nudge a
  waiting `DRAFT`, never gate work on one. ✅ **Triaging a report into `agent/bugs/` is UNAFFECTED** — never cite the rule to
  avoid reading, filing or investigating a report.
- **Delegate heavy reads; keep the conclusion.** Review peers at **SURFACE level** and **escalate rather than deep-check** —
  a high-context session is at *higher* hallucination risk than a fresh one, so a deep check from here is *less* reliable.
- **Chain:** Astra fans out → Astra re-verifies its own subagents → orchestrator sniff test → a cross-vendor Claude agent
  **only if the sniff test fails**. Hunts, broad diffs and heavy coordination go to **Astra (Codex)**; builds to a Claude session.
- ⚖️ **The VOICE RULE binds every public surface:** plain for players, precise for the two Paradox developers who plan
  hotfixes from our fix list. **No "no guarantees" / "unverified" / "not witnessed" hedging.** If the owner cannot follow a
  sentence, it is word salad and it fails.
- ⭐ **A ruling carries the condition it was made under** (`WORKFLOW.md` rule 5a). Record the state; re-read it against today's
  before treating it as binding; never call a later ruling a "reversal" without checking the earlier one's condition.

---

## 5a · ⛔ LANDED AFTER THIS HANDOFF WAS WRITTEN — four things every v10 agent must be told

**Not this session's work; recorded from the owning session's report on 2026-09-12 (`d56293a` → `2b1fd91`).**
What matters here is only that v10 runs straight through the first two.

⛔⛔ **IT IS NOT YOUR JOB TO RE-DERIVE, RE-CHECK, AUDIT OR "FINISH" ANY OF IT — owner, 2026-09-12.**
This is **an ongoing multi-agent, mixed-model effort running in a SEPARATE TREE.** What you can see here is
a deliberate **partial** landing: that part had to be in **before this tree moved again**, and **the rest
lands only once v10 has left.** ⇒ **Partial is not unfinished.** Do not read the gaps as work owed, do not
tidy them, do not re-run their measurements, and do not start the documentation they say is missing beyond
saying the marker obligation out loud in your own briefs (point 1). ⚠️ **If you think you have found a real
problem with it, tell the owner — do not act on it**, and do not spend a session proving it first.

1. ⭐⭐ **THE MARKER OBLIGATION — the one real documentation gap, and v10 walks into it.** Checklist items
   now carry a status marker, e.g. `<!-- ck:162 status:ruled owner:no -->`, and a register is built from
   them. **Nothing in `WORKFLOW.md`, `CLAUDE.md`, `README.md` or `perma/` yet tells an agent that changing
   an item's status ALSO means updating its marker.** v10 will close items and add them, and **every item
   that moves without its marker makes the register quietly wrong.** ⇒ **Say this explicitly in any brief
   you write until it is documented.** ⚠️ `doccheck` currently reports **41 marked, 28 needing a marker** —
   and **ck158 is one of the unmarked**, so the sitting has to ADD one rather than update one. ⛔ Match the
   vocabulary of neighbouring items; do not invent a new status word.
2. ⛔ **After a CHECKLIST-ONLY edit, run `python tools/doccheck.py --regen-waiting`, NOT `--regen`.**
   `--regen` rebuilds both indices from **every entry on disk, a peer's uncommitted ones included**.
   `--regen-waiting` rewrites only `docs/WAITING_ON_YOU.md`. ⚠️ An edit that touches **entries** as well as
   the checklist still needs the full `--regen` — the distinction is about what you changed, not a
   preference.
3. **Co-runs moved to `agent/prompts/perma/CO_RUNS.md`** (`WORKFLOW.md` keeps a stub). ⚠️ **Sign-off tiers
   did NOT move** — they stayed behind as their own `## Sign-off tiers` section, so anything citing "the
   co-run section" for **tier** rules is still correct.
4. ⚠️ **`STATE.md`'s `WORKFLOW.md:407` pointer is STALE** — the `RunAll()` re-stamp line is now at **`:537`**.
   Pre-existing, not caused by the co-run move. **The owed sitting (ck144 a) is what acts on it.**

⭐ **One finding from that session worth carrying, because it is about our own records:** an archival script
proposed moving **163, 164, 166, 167 and 168** into `docs/archive/`, which sits behind an `.rgignore`
boundary. Those are the bodies `STATE.md` pins **by number** as "do not re-derive" — so an agent following
STATE would have grepped the checklist, found a stub, and a default `rg` would never have surfaced the body.
It was caught in dry-run and the rule was corrected. ⇒ **Archiving a checklist body that STATE cites by
number is a silent failure, not a tidy-up.**

---

## 6 · Traps that have each cost this project a real error

1. ⛔ **All sessions share ONE git identity** — `git log --author` cannot attribute work. Identify by **sha + diff**, and list
   your own shas when relaying.
2. ⛔ **A pathspec is only HALF a commit fence.** It protects every OTHER file, but for a path you *name*, git commits that
   path's **working-tree** content — a peer's unstaged edits included (this happened 09-12, `cc3edf2`). On a file two sessions
   are inside at once: stage **your own hunks** (`git add -p`, or `hash-object` + `update-index`) and commit **without** a
   pathspec. Before `--regen`, check `git status docs/agent/bugs/` for foreign ` M`/`??`.
3. ⛔ **Never state an absence from a truncated grep.** `| head -5` is not an enumeration. A claim that something is *nowhere*
   needs the presence side counted — I called a shipped call form "witnessed nowhere" on 09-12 and a peer found it in 19 files.
4. ⛔ **A status flip must hit BOTH the front matter and the body's heading tag** — doccheck goes RED on one without the other.
5. ⛔ **Never discard or overwrite a file you did not write without reading it first.**
6. ⚠️ **A declined check can leave a promise standing in a player-facing draft** — when a check is dropped, grep the drafts.

---

## 7 · Where things live

- **`STATE.md` is the kernel** — status + pointer, **never derivation**. ⚠️ **It is at ~16.2 KB against an 18,432-byte HARD
  cap that BLOCKS commits** (warn 12,288, ruled accepted by ck132 SKIP). ~2.2 KB of headroom. It was compressed 09-12 by
  cutting that day's closed-ruling derivation back to pointers. ⇒ **Put closed rulings in the checklist, not here**, and if
  the hard cap is approached, that is an owner decision (raise the warn, or authorise an eviction pass) — not a silent trim.
- **Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, never only in agent docs.
- Release machinery `prompts/perma/RELEASE.md` + `perma/RELEASE_OUTBOX.md`; surfaces `perma/PUBLIC_SURFACE_SWEEP.md`
  (`README.md` is its §3b). Site audit `perma/SITE_AUDIT.md`.
- Field-report reply drafts: `docs/FIELD_REPORT_REPLIES.md` (**pull-only**, see §5).
- Prompt map `prompts/README.md`; reusable prompts in `prompts/perma/`, one-offs in the root, `git rm`'d when fired.
- History `docs/archive/SESSION_LOG.md` · defect truth `agent/bugs/INDEX.md` · engine facts `agent/facts/INDEX.md`
  (⭐ **`EF-###` ids are allocated by THIS repo** for both repos — ck167/86).
- The opt-in mod's own decisions: **`C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md`** (moved there 09-12, ck167).
