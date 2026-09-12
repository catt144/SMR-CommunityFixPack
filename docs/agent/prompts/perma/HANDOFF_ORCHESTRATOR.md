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
| `7806c0a` | ⭐ **New one-off brief, NOT YET FIRED:** `prompts/VANILLA_DIFF_DISPOSITION.md`. See §3d |
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
| **157** | (a) post the C89 reporter reply · (b) route the developer note — ⚠️ that report came through **our** channel, so the route is the fix list the devs plan from, or the Building Codes thread |
| **151** | (b) which sections of `MIGRATION_DEV_REPORT.md` may be sent · (c) which checks join the ck144 (a) sitting |
| **144 (a)** | the owed post-upload boot, ONE boot, now on v8 (STATE's OWED line carries the recipe list) |
| **148** | ⏳ deferred, not closed — all three calls open |
| **133** | **(2)** what a fix does on an UNKNOWN probe answer · **(4)** `LuaRevision` as an observation label. One `FIX_POLICY` §2a line each |
| **98** | the 1.0.7 branch: pin back, move the baseline to 1.1.0, or both — see §5 |
| **53** | hardening-queue **row 3** (see §5), plus the older timing call (harden now or in 1.0.1, rec 1.0.1) |
| **47** | the veto-snippet rider: the modder-page example still names `DustDevilSpawnGate`, deleted by `2dc1dbe` |
| **83–97** | the opt-in-mod repo decisions, never ruled. ⚠️ **88 is overtaken** by ck148 |
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
- ⭐ **UNFIRED, ready to take: `prompts/VANILLA_DIFF_DISPOSITION.md`** (`7806c0a`) — the only live one-off in the prompts
  root that is not a grave. Tool-neutral, read-mostly, one report + a checklist item. See §3d.

### 3c · The hotfix-3 batch — 135, 137, 138, 140, 141, 142

⚠️ **Being tackled next, and it may have moved since this was written — read the checklist headings, do not trust this table.**
As of 2026-09-12 **the batch as a whole had not been tackled**: no ruling stamp on any of the six.

| # | one line | owed by |
|---|---|---|
| **135** | `luafn.py`'s body delimiter over-spans one-line functions; measured to change **0** shipped hashes | **owner** — (a) leave / (b) ⭐ fix in hotfix 3 (rec) / (c) ⛔ flag-gated, forbidden by the tool's own header |
| **137** | three vanilla politics candidates (C63/C64/C65), need one fresh 1.1 politics colony | owner: provision a fixture, or leave source-only |
| **138** | eight caller-seam candidates (C66–C73), need fresh 1.1 fixtures; none is a gate | owner: take naturally available fixtures only (rec: C66 first) |
| **140** | C75 + C76 answerable in one Incident fixture (two Fusion Reactors, no Eternal Fusion) | owner: only if it arises naturally |
| **141** | vanillahunt leftovers C79/C80/C81/C62. ⛔ **C78 is not owner-takeable on this Steam install** (one branch at a time) | owner (rec: C79 first) |
| **142** | terminal audit re-derived all 12 P2s: 6 hold, 5 weakened, **C80 refuted**, C82 newly filed | owner: name any for hotfix 3, or accept file-and-watch (rec: **none today**) |

✅ **The "unresolved tension" this section used to carry is GONE — checklist 161, 2026-09-12** (`ea91f19`). The owner
explained the 09-08 rule themselves: it was **triage scoped to the 1.1.0 recovery**, not standing policy, and it expired
with that condition; the 09-09 "Leave ck126 in" was never a reversal. Unearned-gain candidates (C64/C75/C78/C67/C79) are
ordinary candidates now, priced on cost; **C82 was always a straight player LOSS and never depended on the rule.**
⛔ **DO NOT RE-DERIVE THE CONTRADICTION.** Three documents already did and handed it back to the owner, which is the exact
attention drain the original triage rule existed to prevent. The generalisable lesson is binding **authoring rule 5a**
(`WORKFLOW.md:60`): *a ruling made under a named condition expires with that condition* — record the state a ruling was
made in, re-read it against today's before treating it as binding, and never call a later ruling a "reversal" without
checking the earlier one's condition first.

⭐ **The standing recommendation for the batch, re-derived on COST on 2026-09-12 after 161 removed the blocker — so it
does not rest on the expired rule.** The owner has seen it; **nothing here is ruled.**
- **Take 135.** 0 shipped hashes affected, and its blocker discharged when vanillahunt closed 09-10. Small standalone change.
- **Leave 137 / 138 / 140 / 141 opportunistic.** All four are source-read candidates with **no field report behind them**,
  so a provisioned fixture is the only route, and none is a release gate. Take one only if a colony arises naturally.
- **Keep C82 + C66 on a watch list** as the two cheapest organic looks.
- ⛔ **142 is explicitly STILL OPEN** — 161 removed the blocker, it did **not** rule 142. The owner has not named anything
  for a hotfix-3 list, and "accept file-and-watch for all" is also unsaid.

### 3d · The four vanilla instruments, and a live procedure gap

**Two pairs, two subjects — routinely conflated, including by the session that wrote this** (source read, 2026-09-12):
`treediff.py` + `presetdiff.py` were written **inside vanillahunt as its instruments** (*what did the GAME change
1.0.7 → 1.1.0?*, and they produced the C-candidates); `bodycheck.py` + `sigcheck.py` came from **hotfix 2 /
`reports/PACK_1_1_0_REVERIFICATION.md`** (*what moved under the code WE patch?*).

⚠️ **The gap: `WORKFLOW.md`'s two after-every-patch rules (`:139` fpk verification, `:974` five-shape enumeration) name
NONE of the four.** The one procedural sentence — *"the update-day checklist becomes: run three tools, read one table,
write the REMOVE/FIX prompts from it"* — is a **recommendation inside a report** (`PACK_1_1_0_REVERIFICATION.md` §4
rec 5), never promoted. Meanwhile the card reworded today (`2e919b5`) publishes *"Every game patch is read against the
pack as well…"* — a **recurring-process claim currently resting on a track record.**

⛔ **`prompts/VANILLA_DIFF_DISPOSITION.md` is what resolves this — DO NOT SOLVE IT TWICE.** It carries all three owner
questions (what we do with the diff, how far we trust it, where the information should live) and it is unfired.

**Open thread it also names:** `bodycheck` reports **2 NO-MANIFEST modules** against `FIX_POLICY` §2b (*every module
carries `SRC:` + `DEFECT:` headers or it does not ship*) — **unnamed and unexamined**; the brief asks for them to be
named and classified as violation or exemption. Re-confirmed at exit 0, 2026-09-12.

---

## 4 · Loose ends that were flagged and NEVER answered

Each of these was raised, recorded, and then nothing happened. None is release-blocking; all four are cheap.

1. **The dropped F54 sentence.** The ruled wording batch *drops* F54's dust-storm sentence ("Suspensions the game imposes on
   itself — a dust storm, for instance — still count as before") because the case was never measured. **The audit found the
   opposite: the dropped sentence was the TRUE one** (`SURFACE_AUDIT_2026-09-12.md`, finding D3). It has **not** been restored.
   ⇒ **restore it, or ship without it — the owner's word, and v10 ships the row either way.** Recorded inside ck159.

2. **The ck144 (b) follow-up draft is marked SUPERSEDED and is therefore due for DESTRUCTION at the next release sweep**
   (`docs/FIELD_REPORT_REPLIES.md`'s own rule: a draft reaching `POSTED` or `SUPERSEDED` is cut). **Its text is held nowhere
   else.** It went dead only because its posting condition ("post only if the owner's post said 'still checking'") can no
   longer be evaluated — ck144 (b) was cleared without saying what went up. ⇒ **before the sweep cuts it, either get the
   owner's word to revive it as a `DRAFT`, or accept the loss deliberately.** Its two *leads* are safe in `bugs/C74.md`;
   the *prose* is not.

3. **The C87 lake draft's gate is still `HELD on ck147` after ck147 CLOSED.** The hold is on the **2-minute lake check**,
   which is **still unrun**, and the closure explicitly does not discharge it. The check: build menu → Lakes → Small Lake,
   hover flat ground; "Excavation too deep" ⇒ broken for everyone on 1.1.0, then paste the `LAKECHK` line. C87 is **not our
   pack either way** — the check only decides "every 1.1.0 map" vs "that player's map", which changes the reply's wording.

4. **The 133(5) / 73-tier-0 breadcrumb contradiction.** `bef5e81` closed item 73 and recorded that 133(5) "stays open and you
   have not ruled it"; `2e919b5`, later the same day, takes 73's closure as deciding (5). Both records carry the tension,
   flagged rather than smoothed. **Nothing was built either way, so being wrong costs nothing** — leave it flagged unless the
   owner says (5) was a separate call, in which case it re-opens.

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
