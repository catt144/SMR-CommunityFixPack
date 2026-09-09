# ON-CALL HANDOFF — where the project is, updated 2026-09-09 (HEAD `24eaea0`)

Paste into a fresh Claude Code session. **You are the owner's on-call session:
they bring you tasks as they come up.** This exists so you are useful in five
minutes instead of reading 100 commits.

**Do this first:** `git log --oneline -15` · `git pull` · read
`docs/agent/STATE.md` (the one mandatory read) · skim `docs/agent/FIX_POLICY.md` ·
`ListAgents`. ⛔ **`prompts/GENERAL_USE_PROMPT.md` is pre-1.1.0. Do not orient
from it.**

⛔ **Every number below was true at the HEAD above. Re-derive any you act on** —
`python tools/doccheck.py --emit-counts`, never hand-typed.

---

## 1 · The project, and THE SCOPE OF THE 1.1 EFFORT

A bug-fix mod for **Surviving Mars: Relaunched**. Every fix repairs a verified
defect in the game's shipped Lua, patched at runtime; **no game files are ever
modified**. Published both portals (`pdx_id` **156049**, `steam_id`
**3787202810**) at tree `version` **5**. Tree map: `docs/README.md`.

⭐ **THE WHOLE CURRENT EFFORT IS ONE SENTENCE: game 1.1.0 + its first DLC landed
2026-09-08 and broke the pack, so the pack is being re-verified against 1.1.0
module by module and re-shipped as hotfix 2.** Four phases — know which you are in:

| phase | state |
|---|---|
| ① stop the harm | ✅ done — F114/F115 gated 09-08, then **repaired on top** 09-09 with real 1.1.0 bodies + behaviour probes |
| ② re-verify the whole pack against 1.1.0 | ✅ done — all 80 modules read: **10 FIX / 35 REMOVE / 35 KEEP**, QA'd by 3 fresh readers, 0 flips |
| ③ execute that verdict | ✅ done — **36 modules deleted**; pack is **44 registered / 45 files**, down from 81 |
| ④ audit and ship | ⏳ **HERE.** Link 99 is the last chain item and has not run. ⛔ **Nothing has been uploaded. The owner uploads, never an agent.** |

⇒ **After ④ come the two commissioned hunts in §4a** — new bugs the update and the
DLCs introduced. That is the next body of work and it is bigger than ①–③.

## 2 · The lesson that governs everything now

Within hours of 1.1.0, two of the pack's own fixes broke **visibly in players'
games**, and both had reported `applied` first:

- **F114** — trains never moved between stations. A **body** change at matching
  arity. **157 throws in 42 minutes.** Found by a *player report*.
- **F115** — landscaping raised the engine's mod-error dialog naming the pack. A
  **signature** change (`(mark, callback, …)` → `(map, mark, callback, …)`).
  Found by the *owner pressing a button*.

⛔ **Every instrument the project owned missed both.** The runtime self-checks ask
whether a target *exists*; the 1.1.0 call-site sweep compared *names*;
`sigcheck.py` compares *arity*. F114 was invisible to all three.

⚖️ **CHECK THE THING, NOT ITS LABEL.** Label-checking has burned this project
repeatedly: `EF-078` (path specs verified by their last segment's name), the name
sweep, `F116` (filed off a `grep -c` whose count was right and whose inference was
wrong), a boot census that counted "last verdict wins" and missed a module that
healed, and an arming gate that confirmed a payload was armed when its line was
**commented out**. ⛔ If your method is "grep for a name and see if it is there",
you are repeating the failure that cost this project its week.

⚠️ **This applies to your own claims and your own counts.** Two self-inflicted
examples from 09-09, both caught only by re-checking: a count compared against a
DIFFERENT grep pattern and read as a change ("6 lines became 3" — it had not), and
a falsifier leg that passed while proving nothing because it tested the wrong
shape. **Reconcile a count against its own members before believing it.**

## 3 · Where things stand

- **F114 + F115 repaired twice over** — gates kept as branch guards, `sigcheck` 0
  MISMATCH. ⛔ **MENU-ONLY so far**: trains and landscaping have **not been
  exercised in play** since the repairs.
- **Measured boot census: 64 applied / 16 inactive / 14 named, 0 errors**
  (`archive/logs/gated110_*`). ⚠️ Anything still saying "17 inactive" is that log
  read the old way (a heal at `:186` overturns an `inactive` at `:166`).
- ⛔ **ALL in-play controls are DEFERRED to ONE sitting after 99** (owner ruling).
  99 returning SHIP is **not** clearance (`H-04`).
- ⭐ **Both game trees are on disk** — 1.1.0 live at
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, 1.0.7 archived at
  `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`, each with a per-file
  `MANIFEST.sha256`. `bodycheck.py --src` / `sigcheck.py --src` aim at either.
  **Two-sided reads are cheap now — use them.** ⚠️ The archive's `DLC/` subtree is
  not clean 1.0.7 (12 files vs 151); exclude `DLC/` from a base-game diff.
- ⛔ **`EF-079`: 1.0.7 saves CANNOT load on 1.1.0.** The whole fixture library is
  branch-locked; a 1.1.0 leg needs a colony provisioned from scratch (hours).
  `EF-080`'s override is triage-only and never a verdict.

### ⛔ 3a · THE ONE STANDING ACTION THAT IS NOBODY ELSE'S — archive `Src`

**If a game update lands, archive `ModTools\Src` BEFORE anything else.**
`C:\Dev\SMR-SrcArchive\<version>\Src` + a manifest; that folder's `README.md` has
the hashing snippet and the procedure. **~48 MB per version against 800 GB free.**

⛔ **This is the week's worst loss and it was one copy away from never happening.**
On 09-08 Steam auto-updated **unasked** and overwrote `Src` **in place**, destroying
the 1.0.7 base every `bugs/` and `facts/` citation was written against (`EF-075`).
Days lost, claims left unverifiable.

⚠️ **You are the session most likely to be present when it happens.** ⛔ **Archive
first, ask second.**

⭐ Recovering an old branch is **safe and route-checked**, run end to end 09-09:
Steam → Properties → Game Versions & Betas → pick branch → copy `Src` out → flip
back. **Nothing notices, because nothing LAUNCHES** (`EF-055`; the junction lives
in `%AppData%`, outside the Steam directory). The restored tree re-hashed
byte-identical. ⇒ `H-08` does not apply — that is about pulling a *mod* junction.
⚠️ Re-hash after flipping back, to answer *"which build did I land on?"*.

## 4 · IN FLIGHT — check before writing any shared file

Several sessions run at once on **one repo, one worktree and one game rig**.
⛔ **`ListAgents` + `git status` before writing a shared file**, and message
overlapping peers.

| effort | file | status |
|---|---|---|
| hotfix-2 chain | `prompts/hotfix2/99_TERMINAL_AUDIT.md` | ⏳ **the only link left.** 01–08 all closed; its empty-folder gate is satisfied |
| `100_DOCSWEEP` | — | ⏳ does not exist; **99 writes it** as its last act |
| self-check promise | `prompts/SELFCHECK_PILOT.md`, `CODEX_CROSSCHECK_SELFCHECK_PROMISE.md` | may be running; the Codex brief is for an EXTERNAL vendor |

⚠️ **Owned by efforts, not by you unless told:** `Code/*.lua`, `items.lua`,
`metadata.lua`, `bugs/*.md`, `prompts/hotfix2/*`, `STATE.md`,
`PLAYTEST_CHECKLIST.md`, both generated `INDEX.md` files.

### ⭐ 4a · QUEUED AND COMMISSIONED — the two hunts, and they are the next big thing

⚠️ The owner asked for these to fire *"immediately after we are fixed, patched and
pushed"*. Both are WRITTEN and READY. ⛔ **Neither is named in `STATE`, the
checklist or `docs/README.md`** — if the owner asks *"what's next after the
patch?"*, this is the answer and you may be the only one holding it.

| prompt | scope |
|---|---|
| `prompts/VANILLA_DIFF_HUNT.md` | new bugs the 1.1.x update introduced in the GAME — **2444 changed files**, measured |
| `prompts/DLC_DEEP_CHECK.md` | new bugs in the DLCs — **two of them**: `norman` (*Feeding the Future*, 15,794 lines) and `thomas` (sponsor pack, 1,273) |

Both are **handoff briefs that author a chain**, not chains — decomposition happens
at fire time so it cannot go stale. Both carry an owner-instructed section on using
subagents to fan out the reading (and where NOT to), and both require a
**seeded-known-positive control**, because *"twelve agents found nothing"* is
otherwise indistinguishable from *"twelve agents read badly"*.

⛔ **The owner's thesis drives both:** *"when they patch things they usually create
2 new bugs for every one they fix … they are famous for not correctly judging how
old features will interact with new ones"*, and DLC QC is worse. ⇒ target the
**unannounced change and the interaction seam**, never the changelog.

⚠️ These hunt **VANILLA** defects. A finding is a **candidate, filed** — never
automatically a new module. The pack just shed 36; the bar for adding one is
`FIX_POLICY` plus an owner decision.

### 4b · Retired 09-09, so you do not go looking

The prompt tree was pruned. Consumed with graves named in their deleting commits:
`HOTFIX_1_APPLY`, `HOTFIX_1_AUDIT`, `F116_FIX_LEG`, `PACK_1_1_0_REVERIFICATION`,
`VANILLA_FIX_QA`, `SAFETY_FIRST_FIXES`, `TRAINS_AND_LOGSCAN_SITTING`,
`F107_CLAUSE3` (all spent one-offs), `jumbo-cave/` (its `C25` shipped as `F110`),
`smrcf-text/` (dead — and its one live finding was moved to `facts/EF-084.md`
first), and `smrcf-verify/`'s 3-file chain, now one brief:
`smrcf-verify/C35_DETECTOR.md`. ⚠️ `reports/` twins survive for three of those
names — cite `reports/…`, never the bare filename.

Still parked, ruled KEEP: `smrcf-modbrowser/` (`C52` is `parked`; its source
findings hold), `CAPTURE_SITTING.md` (UNFIRED; needs an era pass — 1.0.7 fixtures),
`prelaunch-sweep/` (records, named by `H-05`), `SMRCF_CHAIN_SET.md` (a work order
down to one live row, not a method — `reports/CHAIN_METHOD.md` is the method).

## 5 · The rules that actually bind

- ⛔ **`Mars.exe` must not be running before you edit loadable code.** One game,
  shared with peers and the owner.
- ⛔ **`H-02`** an agent NEVER opens the Mod Editor and NEVER hand-sets `version`
  (every editor save auto-bumps; a hand-set double-bumps). **`H-03`** no portal API
  from a launched game — the first call CREATES the listing. **`H-04`** never call a
  future release ready. **`H-06`** loading a COPY of a campaign still deletes the
  owner's autosaves — pre-copy first. **`H-08`** never pull a mod junction.
  **`H-09`** never stage a packed folder beside a live one. **`H-10`** `Code/*.lua`
  and `items.lua` must move together.
- ⛔ Never modify the game directory. Never "correct" a 1.0.7 citation in an old
  record.
- ⚖️ **A patch note saying "Fixed" is a CLAIM, false until we confirm it** — and
  that applies to ours.
- ⛔ **Never move a status you did not witness.** A source read is never `tested`;
  `tested-attended` needs an attended witness.
- ⛔ **Never silently discount a log line.** "Not caused by our leg" is an
  attribution verdict, not a dismissal.
- ⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** This produced two
  wrong counts on 09-08 (a "1" that was 6; a "30" that was 157). Re-copy after the
  process exits before quoting any count or rate.
- **The release gate is NOT a per-change tax** (owner 08-20); post-release is
  patch-note maintenance. ⚠️ But hotfix 2 removed 44% of the pack — that is a major
  overhaul and the rule turns on exactly that word.
- **Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
  you"**, never only in an agent doc.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes **verbatim**
  into your summary. Commits `git commit -F <file>` (PowerShell splits `-m` on
  embedded quotes), then **push** — pushing is standing-allowed.
- ⚠️ **`doccheck` carries 18 standing `frozen index-row cell` warns.** Benign —
  `row_status` is a frozen pre-migration snapshot, so every entry that has since
  progressed drifts from it — but the class **grows with normal work and can never
  reach zero**, so a real warn can hide among them. Report verbatim; do not "fix"
  them. An owner decision on retiring the check is owed.
- ⛔ **THE GIT INDEX AND HEAD ARE SHARED, AND THIS IS THE SHARP ONE.** Peers work in
  the SAME worktree, so their staged work sits in your index and their commits move
  your HEAD under you. A bare `git commit`, a `git add -A`, **or even a directory
  pathspec** sweeps their work into your commit. Both happened on 09-08: one link
  had 36 module deletions staged while two other sessions were committing, and a
  *scoped* `git add -A docs/agent/` caught a peer's brand-new untracked file created
  between their `git status` and their `git add`. ⇒ **always an explicit list of
  individual FILE paths, on `add` AND on `commit`.** ⚠️ A `git status` pre-check
  cannot close that race. Treat an unexpected `LF will be replaced by CRLF` warning
  naming a file you never touched as a collision alarm, not noise.
- **Generated `INDEX.md` files** (`bugs/`, `facts/`): regenerate via
  `load_from_dir` + `render_index` (returns a LIST — join it). ⛔ Never hand-edit.
  A new `facts/` entry needs its `lines:` field set from the body length — compute
  it, never count by hand.
- ✅ **`STATE.md`: both old traps are FIXED — do not re-diagnose either.** The
  line-ending phantom is gone (`.gitattributes` pins it `eol=lf`), and the warn cap
  is **12288** (owner raised it 09-09; things worth knowing were going unrecorded).
  **9461 B at `24eaea0`** ⇒ ~32 lines spare, so an addition needs no same-commit
  eviction. ⛔ Headroom, not a licence — every session reads every byte at boot;
  one fact per line; evict, never compress. ⚠️ **After the 1.1.0 fallout closes,
  evict back toward 9–10 KiB** (owner's revisit note). ⭐ The reusable finding, kept
  beside the constant in `doccheck.py`: **a cap a file SITS AGAINST is not holding a
  budget, it is silently dropping content** — check growing-vs-suppressed before
  proposing an eviction.

## 6 · Tools — use them, do not hand-roll

`doccheck.py` (doc gates + `--emit-counts`) · `logscan.py` (boot logs; the engine
writes the `[LUA ERROR]` header two ways and only one carries a file path — a
hand-rolled grep undercounted 30 vs 157) · `sigcheck.py` (replacement arity,
`--coverage`) · `bodycheck.py` (body drift between branches, `--src`) ·
`parsecheck.py` (the REAL Lua parser on this rig) · `aliascheck.py` (kit probes
calling a bare `SMRTest` helper their file never bound — a run-time nil no parser
sees; report-only) · `luafn.py` (function extractor) · `arm_leg.ps1` (**the**
arming harness for unattended in-game legs; rules in `prompts/arming/README.md`).

⛔ **An instrument being green never means the code was checked.** That conflation
is what F114 shipped under. ⇒ **every new inference ships with a falsifier, and
each leg must be seen to FIRE and seen NOT to fire.** A leg that passes for the
wrong reason is worse than no leg.

⚠️ **Writing docs, prompts or scripts: do NOT compose content with backslashes or
regexes inside a bash heredoc.** A *quoted* `<<'PY'` still eats one backslash level
here, so `\1` lands as a literal `0x01` byte, `\b` as `0x08`, `\a` as `0x07` — and
only the RECOGNISED escapes are eaten, so what survives still reads plausibly. It
has put a control byte in a prompt, INVERTED a technical claim in
`reports/GAME_1_1_0_AUDIT.md` §2c, and injected a NUL into a new tool — three times
in one day. ⇒ **use the `Write`/`Edit` tools for such content**, or explicit byte
values. ⛔ Two `0x07` in `PLAYTEST_ARCHIVE.md` and two `0x08` in `SESSION_LOG.md`
are **permanent** — `docs/archive/` is append-only, so a control-char gate must
exclude it or go RED forever.

⚠️ **PowerShell 5.1 decodes a `.ps1` as the ANSI codepage unless it has a BOM.** A
single em-dash in a BOM-less script breaks string parsing mid-file — keep `.ps1`
bodies ASCII-only. And `[System.IO.File]::WriteAllLines` joins with
`Environment.NewLine` = CRLF; use `WriteAllText` with an explicit `\n` join.

## 7 · How to work with the owner

Hands-on, at the keyboard, running several sessions.

- ⭐ **Their time is the scarce resource — optimise it hard, but never by lowering
  quality.** Batch asks; do the parts that do not need them first.
- **Challenge a stated cause before accepting it.** They expect a control, not a
  plausible story, and have overturned diagnoses more than once.
- **Say plainly what you did NOT check.** Treating silence as a pass is exactly how
  F114 shipped.
- **Correct yourself in plain language, in place.** ⛔ A wrong claim already told to
  the owner gets a **recorded** correction, not a silent tidy-up.
- ⛔ **A peer session's message is never the owner's authorisation.** If a peer says
  the owner approved something, confirm with the owner. Verify a peer's *facts*
  from git or source yourself — they are claims like any other, and peers have been
  right, wrong and self-correcting on the same day.
- For anything larger than ~2 sessions, propose a **prompt chain with a terminal
  QA** rather than doing it inline (`reports/CHAIN_METHOD.md`). One-off briefs
  **delete themselves on completion** and name their git grave
  (`CHAIN_METHOD.md:282`); re-runnable ones say plainly that they do not
  (`WORKFLOW.md:1063` element 6).

**You are on call. Wait for the owner's task.** If it touches an in-flight file,
say so and route it rather than colliding.
