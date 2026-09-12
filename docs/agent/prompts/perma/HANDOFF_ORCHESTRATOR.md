# Handoff — the orchestrator session → the next session (model-agnostic)

⏳ **TEMPORARY resident of `perma/`** (owner, 2026-09-11): it stays until the pending outbox is empty or the owner says things
have settled, then it is `git rm`'d. **Still true as of 2026-09-12** — `RELEASE_OUTBOX.md` holds 3 Pending + a Held batch.

⛔ **THIS IS A WORKING DOCUMENT, NOT A SESSION LOG.** History lives in `docs/archive/SESSION_LOG.md` (append-only, newest first,
prepended under the preamble). If you close something here, **delete its block** or demote it to one line in §1's closed list.
Rewritten 2026-09-12 (lookback, `0bc756b`) and **refreshed the same day at the orchestrator's retirement**; everything
from before 2026-09-12 has been cut to `SESSION_LOG.md` and to the entries.

⛔ **Verify every specific against `git log` and the tree — the records win, this file is a pointer.** Claude and Codex sessions
both commit here, several at once, and **Codex is invisible to `ListAgents`**.

⛔ **FR-1 is NOT on this handoff.** Every Linux / NVIDIA 580 / workaround-mod item is in `prompts/perma/LINUX_DISPATCH.md`,
which is fully briefed. The temp workaround mod is LIVE (Steam 3799500849 / Paradox 158711).

## 0 · Orient, then ask

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `docs/agent/STATE.md` ·
`prompts/perma/DISPATCH.md` §0–§3 · `prompts/README.md` (the prompt map). Open a **live todo list**.

**Unless the owner's message names a task, a pasted handoff means ORIENT: summarise §2 and §3 and ASK what to take.**
Do not execute (memory: handoff-invocation-means-orient-first).

⚠️ **Your first `doccheck` will print a STATE.md warn (14,915 bytes against a 12,288 warn, hard 18,432).
That is a RULED, ACCEPTED state, not a task** — the owner answered ck132 with **SKIP** on 09-12: the warn
stays where it is, no eviction is authorised, and `perma/STATE_EVICTION.md` is not to be fired. doccheck is
GREEN with it. Do not spend your first act on it, and do not re-propose eviction unless the owner asks.

---

## 1 · What landed on 2026-09-12

⛔ **This is a pointer list, not the record.** Every sha below has a full entry in `docs/archive/SESSION_LOG.md`
(`git show <sha>` for the reasoning) — read there, not here, and do not grow this list.

| sha | what |
|---|---|
| `59c8c47` `98d0461` `4dc5073` | **The three v10 builds:** C85 clogged release · **C89** faction dome gate (⚖️ judgment call) · C88 Building Codes vs prefabs. Attended check = ck158, §2 |
| `690a1ee` → `576581c` + `1d625e4` | Astra: F60 harness repaired, C90 measured. Deskbench **20/20**, C90 control **18/18**, 8 scratch falsifiers. `reports/DESKBENCH_C90.md` |
| `4c7b11a` | Surface audit: F37/F43 retirements confirmed, **F31 settled → RETIRE**, three ruled sentences refuted |
| `929a293` `cf8f04a` `bef5e81` | The three owner ruling batches: the four approved sentences, seven closures, the 39/41 dialog fixes, items 47/53/73, modder-doc paring |
| `2e919b5` | ck133/ck112 **reword** — HOW IT WORKS bullet 3 now matches what `Require` can do; all five live copies, byte-verified. ⚠️ Its card sentence is what makes §3d urgent |
| `7d8c384` `42eab2a` | `FIELD_REPORT_REPLIES` purged to live drafts + posted record (C74 leads rehomed); ck144 (b) recorded |
| `5c21f36` `6f5abaf` | Lookback: ck152 (c) CLOSED as DESIGN · `README.md` filed as a public surface · the 3 site files recorded · **F59 cost of ours** (§4) |
| `ea91f19` | ⭐ **ck161** — the 09-08 "small positives" rule was 1.1.0-recovery triage and **EXPIRED with it**; corrected in 7 places, lesson = binding **rule 5a, `WORKFLOW.md:60`**. See §3c |
| `7806c0a` → `cc3edf2` `7e445d3` `4b6beda` | **FIRED and landed 09-12** (peer `smr-bugfixpack-b2`): `reports/VANILLA_DIFF_DISPOSITION.md`, the brief `git rm`'d, `WORKFLOW.md` gained a BINDING after-patch section, `FIX_POLICY` §2b a pointer. Owner calls = **ck163**. See §3d |
| last one | ck160 closed to the release lane; this refresh; §3d added |

**Closed today, do not re-ask:** ck133(1)(3)(5)(6) · ck144 (b) · ck147 · ck150 (a) · ck151 (a)/(d) · ck152 (all) · ck153 ·
ck155 · ck156 · ck159 (1)(2)(3) · **ck160** (ordinary release-lane work; all six `README.md` claims, the store-status line
included, are staged in `RELEASE_OUTBOX.md:122-134`) · **ck161** · items 39/40/41/47/50/73. ⏳ **ck148 DEFERRED** (owner:
skip; chain not started, all three calls still open). ⏳ **ck132 SKIPPED** — see §0.

---

## 2 · The v10 critical path, in order

**1. ck159 (1)(2)(3) — ✅ RULED.** F31 retires · F37's load-time clean-up is an accepted loss (does **not** move into
`90_SaveSanitizer.lua`) · all four sentence replacements go in, verbatim in `reports/still-needed/WORDING_RULED.md`.

**2. ⛔ THE ck158 SITTING — the gate. ONE boot does all three legs.** This is the only thing between here and v10, and only the
owner can do it. `tested-attended` is the owner's word to grant and nothing else grants it.
- **A · C85** — minutes, any 1.1.0 colony. Force the state, save/quit/reload, read the `CloggedBuildingRelease: released …` line.
- **B · C89** — ⚖️ the judgment call the owner asked to watch. **B1** is a two-second falsifier on any dome; **B2** is a
  **fresh one-shot colony, 20–30 minutes of ordinary play** (first dome → Martian Assembly → a sol → a faction seated →
  an unconnected second dome with three adults). Real play time, not a loadable fixture.
- **C · C88** — minutes, needs **Building Codes → Strict** and the Martian Assembly; deploy a prefab with a maintenance figure.

**3. `RELEASE.md` over Held + the 3 Pending.** Text = `WORDING_RULED.md` (supersedes `SURFACE_PLAN.md`) under the ⚖️ **VOICE
RULE**. ⛔ **Re-derive every count once, carry none:** modules ±the retirements, the card count word, card headlines,
"real defects you cannot see today", **judgment calls three → four (C89)**, and the six `README.md` claims now filed in
`RELEASE_OUTBOX.md`'s batch notes.

**4. The owner's upload,** then the formatting cleanup pass and the store-card paste backups.

**5. The held site deploy, fired ONCE.** `a061665` (49 rows) has been held since 09-11 for exactly this; the live site shows
**50** meanwhile, which is deliberate. ⛔ **Three uncommitted files in `C:\Dev\SMR-CommunityMods` must be ruled on first** — see §3.

---

## 3 · Everything still open

### 3a · Owner decisions owed (nothing an agent can do)

| ck | what |
|---|---|
| **158** | the three-leg sitting above — **the v10 gate** |
| **151** | (b) which sections of `MIGRATION_DEV_REPORT.md` may be sent · (c) which checks join the ck144 (a) sitting |
| **144 (a)** | the owed post-upload boot, ONE boot, now on v8 (STATE's OWED line carries the recipe list) |
| **148** | ⏳ deferred, not closed — all three calls open |
| **133** | **(2)** what a fix does on an UNKNOWN probe answer · **(4)** `LuaRevision` as an observation label. One `FIX_POLICY` §2a line each |
| **98** | the 1.0.7 branch: pin back, move the baseline to 1.1.0, or both — see §5 |
| **53** | hardening-queue **row 3** (see §5), plus the older timing call (harden now or in 1.0.1, rec 1.0.1) |
| **47** | the veto-snippet rider: the modder-page example still names `DustDevilSpawnGate`, deleted by `2dc1dbe` |
| **83** | the SHARED Test Kit's opt-in coverage — ⏸ not owed; 2 of its 5 proposals help us regardless. ✅ **84/85/89–97 OFFLOADED to the opt-in repo 09-12 (ck167); 86 is already in force; 88 rides with ck148** |
| — | the **C89 in-game A/B** the owner flagged to observe personally, and the **three site files** below |

⛔ **`C:\Dev\SMR-CommunityMods` has three uncommitted files waiting on the owner** (2026-09-12): `content/faq.md`,
`content/for-modders.md`, `content/install.md` — today's modder-doc paring. **That is a DIFFERENT git repo: do not commit,
stash or checkout there.** Recorded in `RELEASE_OUTBOX.md` (Held) and `PUBLIC_SURFACE_SWEEP.md` §1. Re-read
`git -C C:\Dev\SMR-CommunityMods status --porcelain` rather than trusting this line.

### 3b · Work owed to / by agents

- **C90 — shape RULED, nothing built.** Per-module apply-success guards in `Fix_SaintBlessing` + `Fix_SinkholeIndestructible`.
  ⛔ **NOT** the shared core's apply-verdict contract. ⛔ **Never gate on `entry.status == "active"`** — `run_apply` sets status
  only *after* apply returns. Must define reset/retry, not treat a once-true flag as an everlasting verdict.
- **C91** — vanilla leaks the Building Codes maintenance modifier on repeal. Developer-thread material; no fix owed.
- **F59's A1 expedition half is UNTESTED** and the change note says so. **F80** is still capture-before-mitigate.
- **F54 was never swept**; F52/F53/F73 are PARTIAL with named residuals.
- **`prompts/SELFCHECK_PILOT.md`** was authored for ck133(1), never fired, now unreachable. Marked "do not fire"; **removal
  recommended to the owner, not done.** The two `SELFCHECK_PROMISE_*` reports stay — reports are not consumed by rulings.
- **Desk NEXT, unclaimed:** `prompts/DLC_DEEP_CHECK.md` (bounded; framing in its banner).
- ✅ **Both of the disposition report's owed items are DONE (ck163 ruled 09-12).** C80 flipped `cand`→`closed` (heading tag
  AND front matter — doccheck goes RED on one without the other); both `NO-MANIFEST` modules stamped, `bodycheck` now
  reports **0 with no manifest**. ⚠️ That immediately surfaced **ck164**: F48's upstream defect was fixed by vanilla in
  1.1.0, but savegame fixups never re-run (`SavegameFixup.lua:33-39`) and the name is unchanged, so the repair cannot reach
  an already-damaged save — the pass is the only thing that can. Recommendation KEEP; owner's call.
  ⛔ `90_SaveSanitizer.lua`'s F48 `DEFECT:` line now reports **DEFECT-GONE every run, deliberately** — do NOT rewrite the
  regex to silence it; it is the ck164 flag and doccheck does not gate on it.

### 3c · The hotfix-3 batch — FIVE OF SIX CLOSED 2026-09-12, only 135 is left

✅ **ck163 (a) closed 137, 138, 140, 141 and 142 in one ruling** by dispositioning all 25 source-only candidates as four
groups instead of one by one. ⛔ **Do not re-open them and do not re-derive the old table** — it is gone from this file on
purpose. The groups: **A** (C63, C66, C82) stay candidates as **organic riders only**, never provisioned for · **B** (C64,
C67, C75, C78, C79) are player *benefits*, no action ever absent a field report · **C** (C58, C68, C69, C76, C80) weakened
or refuted · **D** the 12 P3s, source-only. ⛔ A disposition, **not** a dismissal: any field report naming one reopens it.

**Still open: 135 only.** `luafn.py`'s body delimiter over-spans one-line functions; measured to change **0** shipped
hashes; blocker discharged when vanillahunt closed 09-10. Owner options: leave / ⭐ fix in hotfix 3 (rec) / ⛔ flag-gated,
which the tool's own header forbids.

✅ **The "unresolved tension" this section used to carry is GONE** (ck161, `ea91f19`) and the generalisable lesson is
binding authoring **rule 5a** (`WORKFLOW.md:60`): *a ruling made under a named condition expires with that condition.*
⛔ **DO NOT RE-DERIVE THE CONTRADICTION** — three documents already did and handed it back to the owner.

### 3d · The four vanilla instruments — RESOLVED 2026-09-12, do not re-open

✅ **The procedure gap this section existed to flag is CLOSED.** `WORKFLOW.md` now carries a **BINDING**
"After a game patch — the source-diff instruments" section (`:156`, adopted 09-12), promoted out of
`PACK_1_1_0_REVERIFICATION.md` §4 rec 5 where it had sat as a recommendation inside a report; `FIX_POLICY` §2b points at
it as the canonical copy. So the card's *"Every game patch is read against the pack as well…"* now rests on a written
procedure rather than a track record. The whole disposition is `reports/VANILLA_DIFF_DISPOSITION.md`; the owner's four
calls are **ck163**, and (c) asks whether anything else joins the after-patch step.
⚠️ **Note when relaying (c): the procedure is already IN FORCE, not awaiting the ruling** — it is an agent-side
authoring doc, so it landed ahead of the word and is reversible. The owner is confirming, not choosing from scratch.

⛔ **Do not re-derive the two-pairs distinction** — it is in the report. In one line: `treediff`/`presetdiff` ask *what
did the GAME change?* (vanillahunt's instruments, they produced the C-candidates, now **on trigger, never retired**);
`bodycheck`/`sigcheck` ask *what moved under the code WE patch?* (hotfix 2's, now **every patch**).
⭐ The step that matters most is free and irreversible if missed: **archive `ModTools\Src` BEFORE an update or a Steam
branch switch** — 09-08 overwrote it unasked.

⚠️ **One stale pointer this section used to carry, corrected:** the five-shape enumeration is `WORKFLOW.md:1059`,
**not `:974`** — the new section pushed everything below `:156` down by ~90 lines. `:60` (rule 5a) and `:139` (fpk
verification) are unmoved. Re-check any `WORKFLOW.md` line number written before 09-12.

**Still open from it:** the **C80 status flip** and the **two NO-MANIFEST modules**, both in §3b above.

---

## 4 · The four loose ends — ALL FOUR CLOSED 2026-09-12 (checklist 162)

✅ **Nothing is owed here and this section is a receipt, not a task.** All four were raised, recorded, and then
asked of nobody until they became checklist **162**; the owner ruled every one the same day. ⛔ **Do not re-open
or re-derive any of them** — read 162 for the reasoning.

1. **The dropped F54 dust-storm sentence — STAYS DROPPED.** The surface audit's D3 recorded it as the TRUE one;
   re-derived from the shipped tree it is false — a dust storm sets `self.suspended`, which
   `GetWorkNotPossibleReason` returns, while the lax clause only ever forgave a not-PERMITTED reason. A
   storm-suspended hub never counted, before our fix or after. Route in `bugs/F54.md` (09-12);
   `still-needed/WORDING_RULED.md` says ⛔ do not restore.
2. **The ck144 (b) follow-up draft — CUT.** The owner does not remember what the 09-10 post said, so its posting
   condition was permanently unevaluable. Both `SUPERSEDED` C74 blocks are **removed** from
   `docs/FIELD_REPORT_REPLIES.md` and logged in its cut table with a `git show` pointer. **An accepted loss,
   deliberately taken** — do not reconstruct the prose. Both leads survive in `bugs/C74.md`.
3. **The C87 lake check — DECLINED ON COST:** *"a lead not a test … only ever had one report."* C87 is
   **file-and-watch**; a second report reopens it. ⛔ Do not re-ask for that sitting.
   ⭐ **The transferable bit: a declined check can leave a promise standing in a player-facing draft.** The held
   reply still read *"we're checking whether it happens on every 1.1.0 map"* — removed rather than left to go
   quietly false; it is now a plain postable `DRAFT`.
   ⛔ **Do not repeat the claim that went with the earlier `LAKECHK` edit:** I called `map:GetHeight(x,y)`
   witnessed nowhere and said the line would have thrown; a peer refuted it — **19 shipped files use it**,
   including the exact `obj:GetMap():GetHeight(x, y)` form (`Landscaping.lua:225`). The old line would have run.
4. **The 133(5) / 73 breadcrumb contradiction — RESOLVED.** The owner was asked directly and confirmed that
   closing 73 closes (5); the breadcrumb is **not built**, and both records are reconciled.
   ⚖️ **Closed under a named condition (rule 5a):** the rate is effectively zero — two sightings, one reporter,
   one day, nothing since. **More false-blame reports reopen it.**

---

## 5 · Still open from today's rulings — a fresh session will otherwise miss these

- ⛔ **Hardening-queue ROW 3 is open and INDEPENDENT of item 53's ruling.** `Code/Fix_StaleReservations.lua:120-159` (⚠️ the
  file records 120-159, not the 127-159 some notes carry) walks every Residence's reservation list on `OnMsg.NewDay` **with no
  per-item `pcall`**. Its trigger is **save corruption, not another mod**, so paring the modder surface does nothing for it: a
  throw mid-sweep abandons the rest of the list every sol while the fix still reads `active`, and it can reach the player's
  error box. Donor shape is live at `Code/90_SaveSanitizer.lua:224`. ⚠️ The audit's donor pointer `Fix_TrainMinors:141` is
  **stale** — deleted by `2dc1dbe`.
- **Rows 1 + 2 are DEPRIORITISED, not closed.** Recorded so nobody re-derives it: `SMRFixPack_Disabled = "yes"` passes the
  `or {}` adoption at `00_Core.lua:13` and every id then reads nil ⇒ **the modder's veto is silently ignored and every fix
  applies anyway**; `= true` throws at that index ⇒ **kills the whole pack, log-only**. Row 2 is the same shape for
  `SMRFixPack_Optional` (`00_Core.lua:17`, read at `:57`). ⚠️ A plain `type(x) == "table"` guard is **not** enough alone.
  Row 4 is reassigned to C90's build; rows 5–7 dropped; row 8 moot.
- **Item 133 (2) and (4) are left OPEN** — one `FIX_POLICY` §2a line each, independent of the collapsed prototype.
- **Item 98's rig half.** ⛔ `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` is **93 MB of source and a sha256 manifest — no
  executable and no data packs**, so it **cannot do a runnable A/B**. A runnable 1.0.7 needs the Steam install switched to the
  1.0.7 branch, and **Steam serves one branch at a time**, so the 1.1.0 install goes away while it is switched (and `EF-079`:
  1.0.7 saves cannot load on 1.1.0, so the whole fixture library is branch-locked).
- **`reports/PARKED_OPTIN_REFERENCES.md:697` carries the SAME over-promise the 09-12 reword removed** — *"stands down if an
  official patch changes what it was written for"* — inside §P38, the parked `metadata.lua` `description`. The parked file was
  **not** updated, and its restore checklist says to paste P38 back verbatim at the opt-in launch. ⇒ **if it is restored as
  written, the retired over-promise goes straight back onto the store card.** ⛔ **H-07 forbids touching the parked references
  now** ("that is ITS launch obligation"), so this is a note for the opt-in launch, **not** work to do today.

---

## 6 · The working method the owner set on 2026-09-12 — inherit this

- **The orchestrator delegates heavy reads to subagents rather than burning its own context.** Fan out; keep the conclusion.
- **The orchestrator reviews other agents' work at SURFACE level only, and ESCALATES concerns rather than deep-checking them.**
  ⭐ **The reason the shallow review is deliberate, not lazy: the orchestrator runs at high context and is therefore at higher
  hallucination risk than a fresh agent.** A deep check from here is *less* reliable than the same check from a clean session.
- **The verification chain:** Astra fans out → **Astra re-verifies its own subagents adversarially** → orchestrator sniff test
  → **a dedicated cross-vendor Claude agent ONLY if the sniff test fails.**
- Standing: **hunts, broad diffs and heavy subagent-coordination legs go to Astra (Codex); builds go to a Claude session.**
  Write such briefs tool-neutral, make coordination git-visible (the push is the claim), commit agent reports verbatim.
- ⛔⛔ **REPLIES TO PLAYERS ARE PULL-ONLY (owner, 2026-09-12, ck165; `WORKFLOW.md` rule 5b).** Never draft one unasked; never
  put one on the owner's owed list, in this table or a session summary; never raise a waiting `DRAFT` as a nudge; never gate a
  fix, a release or a sitting on a reply. The owner had fielded a day of reply questions while the real gate was an unrun
  playtest. ✅ **Triaging a report into `agent/bugs/` is UNAFFECTED and continues** — the report is evidence about a defect;
  what is pull-only is the messaging. ⛔ Never cite this to avoid reading, filing or investigating a report.
- ⚖️ **The VOICE RULE binds every public surface:** plain for players, precise for the two Paradox developers who plan their
  hotfixes from our fix list. **No "no guarantees" / "unverified" / "not witnessed" hedging.** State scope by saying what the
  fix does and for whom; the dated entry keeps the limits. If the owner cannot follow a sentence, it is word salad and it fails.
- ⭐⭐ **TWO PARADOX DEVELOPERS PLAN FROM OUR FIX LIST.** A stale or overstated row costs a developer's time, not just our
  credibility.

---

## 7 · Where things live

- **STATE.md is the kernel.** Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only here.
- Release machinery `prompts/perma/RELEASE.md` + its ledger `perma/RELEASE_OUTBOX.md`; surfaces `perma/PUBLIC_SURFACE_SWEEP.md`
  (⭐ `README.md` is now §3b of it — it had rotted precisely because it was on no list).
- Field-report reply drafts: **`docs/FIELD_REPORT_REPLIES.md`** (a human file — the owner posts, agents draft).
- Prompt map `prompts/README.md`; reusable prompts in `prompts/perma/`, one-offs in the prompts root, `git rm`'d when fired.
- History: `docs/archive/SESSION_LOG.md`. Defect truth `agent/bugs/INDEX.md`, engine facts `agent/facts/INDEX.md`.

**Three standing traps, each of which has cost this project a real error:**
1. ⛔ **All sessions share ONE git identity** — `git log --author` cannot attribute work. Identify by sha + diff, and list your
   own shas when relaying.
2. ⛔ **Commit with an explicit pathspec** (`git commit -F msg -- <paths>`): a bare commit takes a peer's staged deletions.
   Before `--regen`, check `git status docs/agent/bugs/` for foreign ` M`/`??` — regen builds the index from every file on disk.
3. ⛔ **Never discard a file you did not write without reading it first** (the 09-12 `git checkout -- items.lua` disclosure).
