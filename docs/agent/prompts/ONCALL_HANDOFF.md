# ON-CALL HANDOFF — where the project is, 2026-09-09

Paste into a fresh Claude Code session. **You are the owner's on-call session:
they will bring you tasks as they come up.** This document exists so you can be
useful in five minutes instead of reading 70 commits.

**Do this first:** `git log --oneline -15` · `git pull` · read
`docs/agent/STATE.md` (the one mandatory read) · skim `docs/agent/FIX_POLICY.md`.
⛔ **`prompts/GENERAL_USE_PROMPT.md` is from 2026-08-19 and is entirely
pre-1.1.0. Do not orient from it.**

⛔ **Numbers below were true when written. Re-derive any you are about to act
on** — `python tools/doccheck.py --emit-counts`, never hand-typed.

---

## 1 · What this project is

A bug-fix mod for **Surviving Mars: Relaunched**. Every fix repairs a verified
defect in the game's shipped Lua, patched at runtime; no game files are modified.
Published on both portals (`pdx_id` **156049**, `steam_id` **3787202810**) at
tree `version` **5**. Map of the tree: `docs/README.md`.

## 2 · What happened this week, and it is the whole context

**Game 1.1.0.403908 + the first major DLC shipped 2026-09-08.** Player numbers
are at a record. Within hours, two of the pack's own fixes broke **visibly in
players' games**, and both had reported `applied` first:

- **F114** — trains never moved between stations. A **body** change at matching
  arity. **157 throws in a 42-minute session.** Found by a *player report*.
- **F115** — landscaping raised the engine's mod-error dialog naming the pack. A
  **signature** change (`(mark, callback, ...)` → `(map, mark, callback, ...)`).
  Found by the *owner pressing a button*.

⛔ **Every instrument the project owned missed both**: the runtime self-checks
ask whether a target *exists*; the 1.1.0 call-site sweep compared *names*;
`sigcheck.py` (written after) compares *arity*. F114 was invisible to all three.

⚖️ **The rule that came out of it, and it governs everything now: CHECK THE
THING, NOT ITS LABEL.** The project has been burned by label-checking four times
in one week — `EF-078` (path specs verified by their last segment's name), the
name sweep, `F116` (filed off a `grep -c` whose count was right and whose
inference was wrong), and a boot census that counted "last verdict wins" and
missed a module that healed. ⛔ If your method is "grep for a name and see if
it's there", you are repeating the failure that cost this project its week.

## 3 · Where things stand

- **Both defects are fixed twice over**: gated 09-08, then **repaired on top**
  09-09 with real 1.1.0 bodies plus **behaviour probes**, gates kept as branch
  guards. `sigcheck` reports 0 MISMATCH.
- ⭐ **A pack-wide 1.1.0 re-verification read all 80 modules: 10 FIX / 35 REMOVE
  / 35 KEEP**, QA'd by three fresh readers with 0 flips. **36 modules have since
  been deleted** — the pack is now ~43 modules, down from 80.
- **Measured boot census: 64 applied / 16 inactive / 14 named, 0 errors**
  (`archive/logs/gated110_*`). ⚠️ Anything still saying "17 inactive" is the same
  log read the old way (a heal at `:186` overturns an `inactive` at `:166`).
- ⭐ **Both game trees are on disk now**: 1.1.0 live at
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, and 1.0.7
  **archived** at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. You can diff the
  branches — earlier sessions could not. Both carry a per-file `MANIFEST.sha256`;
  `bodycheck.py --src <path>` and `sigcheck.py --src <path>` aim at either.

### ⛔ 3a · THE ONE STANDING ACTION THAT IS NOBODY ELSE'S — archive `Src`

**If a game update lands, archive `ModTools\Src` BEFORE anything else.**
`C:\Dev\SMR-SrcArchive\<version>\Src` + a manifest; the folder's `README.md` has
the four-line hashing snippet and the procedure.

⛔ **This is the week's worst loss and it was one copy away from never
happening.** On 2026-09-08 Steam auto-updated **unasked** and overwrote `Src`
**in place**, destroying the 1.0.7 base every `bugs/` and `facts/` citation was
written against (`EF-075`). It cost days and left claims unverifiable. **~48 MB
per version against 800 GB free.**

⚠️ **You are the session most likely to be present when it happens** — an
on-call session is who notices a Steam update. ⛔ **Archive first, ask second.**
The 09-08 update was noticed only because someone went looking.

⭐ **Recovering an old branch is SAFE and now route-checked, not theoretical** —
it was run end to end on 09-09: Steam → Properties → Game Versions & Betas →
pick the branch → copy `Src` out → flip back. **Nothing in the mod setup
notices, because nothing LAUNCHES** (`EF-055`: the enable is lost only when a
launch runs with the id unresolvable, and the junction lives in `%AppData%`,
outside the Steam directory). The restored tree re-hashed **byte-for-byte
identical**. ⇒ do not let `H-08` scare you off this; `H-08` is about pulling a
*mod* junction, which this is not.
⚠️ Do re-hash after flipping back — not to detect damage, but to answer *"which
build did I land on?"*. A mismatch most likely means a newer build shipped while
you were away, which means archive that one too.
⚠️ The 1.0.7 archive's `DLC/` subtree is **not** clean 1.0.7 (12 files vs
1.1.0's 151, a Steam artefact). Base-game paths are sound; exclude `DLC/` from a
base-game diff.
- ⛔ **Nothing has been uploaded.** Hotfix 1 audited SHIP WITH CHANGES; hotfix 2
  is mid-chain. The owner uploads, never an agent.
- ⛔ **All in-play controls are DEFERRED to one sitting after the chain**
  (owner ruling). The gated boot was **menu-only** — trains and landscaping have
  not been exercised in play since the repairs.

## 4 · What is IN FLIGHT — do not touch without checking

Several sessions run at once on one repo and one game rig. ⛔ **`ListAgents` +
`git log` before writing any shared file**, and message overlapping peers.

| effort | file | status |
|---|---|---|
| hotfix-2 chain | `prompts/hotfix2/` links **06** (store text), **07** (Test Kit), **99** (terminal audit) | live; 01–05 closed |
| `100_DOCSWEEP` | — | ⏳ does not exist; **99 writes it** as its last act |
| self-check promise + mod-blame | `prompts/SELFCHECK_PROMISE_AUDIT.md` | may be running |

**Owned by those efforts, not by you:** `Code/*.lua`, `items.lua`,
`metadata.lua`, `bugs/*.md`, `prompts/hotfix2/*`, `STATE.md`,
`PLAYTEST_CHECKLIST.md`, both generated `INDEX.md` files.

### ⭐ 4a · QUEUED AND COMMISSIONED — two hunts nobody is running yet

⚠️ **The owner asked for these on 09-08 to fire "immediately after we are fixed,
patched and pushed". Both are WRITTEN and READY. ⛔ Neither is named in `STATE`,
the checklist or `docs/README.md`** — so if the owner asks *"what's next after
the patch?"*, this is the answer and you may be the only one holding it.

| prompt | scope | ready? |
|---|---|---|
| `prompts/VANILLA_DIFF_HUNT.md` | new bugs the 1.1.x update introduced in the GAME — **2444 changed files**, measured | ✅ fully unblocked (both trees archived) |
| `prompts/DLC_DEEP_CHECK.md` | new bugs in the DLCs — ⭐ **two of them**, `norman` (*Feeding the Future*, 15,794 lines) and `thomas` (sponsor pack, 1,273) | ✅ no preconditions; source already extracted |

Both are **handoff briefs that author a chain**, not chains — the decomposition
happens at fire time so it cannot go stale. Both carry an owner-instructed
section on **using subagents** to fan out the reading (and, more usefully, where
NOT to), and both require a **seeded-known-positive control**, because *"twelve
agents found nothing"* is otherwise indistinguishable from *"twelve agents read
badly"*.

⛔ **The owner's thesis drives both, and it is worth quoting to yourself before
either fires:** *"when they patch things they usually create 2 new bugs for
every one they fix … they are famous for not correctly judging how old features
will interact with new ones,"* and DLC QC is worse. ⇒ the target is the
**unannounced change and the interaction seam**, never the changelog.

⚠️ **These are hunts for VANILLA defects.** A finding is a **candidate defect,
filed** — never automatically a new module. The pack just shed 36; the bar for
adding one is `FIX_POLICY` plus an owner decision.

⚠️ **Known outstanding, already assigned — do not fix it yourself:** `F115.md`
carries the old census in three places (`:10`, `:14`, `:168`) and a stale "NO
REPAIR SHIPPED" in its front matter. Line `:135` records a *prediction* and must
be left exactly as it stands. **Link 99 owns all of it.**

## 5 · The rules that actually bind

- ⛔ **`Mars.exe` must not be running before you edit loadable code.** You share
  one game with other sessions and with the owner.
- ⛔ **`H-02`** an agent NEVER opens the Mod Editor and NEVER hand-sets
  `version` — every editor save auto-bumps it. **`H-03`** no portal API from a
  launched game; the first call CREATES the listing. **`H-04`** never call a
  future release ready. **`H-08`** never pull a mod junction. **`H-09`** never
  stage a packed folder beside a live one. **`H-10`** `Code/*.lua` and
  `items.lua` must move together.
- ⛔ Never modify the game directory. Never "correct" a 1.0.7 citation in an old
  record.
- ⚖️ **A patch note saying "Fixed" is a CLAIM, false until we confirm it** — and
  that applies to ours.
- ⛔ **Never move a status you did not witness.** A source read is never
  `tested`; `tested-attended` needs an attended witness.
- ⛔ **Never silently discount a log line.** "Not caused by our leg" is an
  attribution verdict, not a dismissal.
- ⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** This produced
  two wrong counts on 2026-09-08 (a "1" that was 6; a "30" that was 157).
  Re-copy after the process exits before quoting any count or rate.
- **The release gate is NOT a per-change tax** (owner 08-20). Post-release is
  patch-note maintenance. ⚠️ But hotfix 2 removes 44% of the pack — that is a
  major overhaul and the rule turns on exactly that word.
- **Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
  you"**, never only in an agent doc.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes **verbatim**
  into your summary. `STATE.md` is byte-capped — an addition needs an eviction in
  the same commit. Commits `git commit -F <file>` (PowerShell splits `-m` on
  embedded quotes), then **push** — pushing is standing-allowed.
- ⛔ **THE GIT INDEX IS SHARED, AND THIS IS THE SHARP ONE.** A sibling's staged
  work sits in the same index as yours, so a bare `git commit`, a `git add -A`,
  **or even a directory pathspec** sweeps their work into your unrelated commit.
  Both happened on 09-08: one link had **36 module deletions staged** while two
  other sessions were committing, and a *scoped* `git add -A docs/agent/` caught
  a peer's brand-new untracked file created between their `git status` and their
  `git add`. ⇒ **Always an explicit list of individual FILE paths**, on `add`
  and on `commit`. ⚠️ A `git status` pre-check **cannot close that race**. Treat
  an unexpected `LF will be replaced by CRLF` warning naming a file you never
  touched as a collision alarm, not noise — that is how both were caught.
- ✅ **`STATE.md`'s line-ending phantom is FIXED — do not re-diagnose it.**
  It WAS line-ending sensitive: blob LF, `core.autocrlf=true` **system-wide**
  (the Git-for-Windows default), so a fresh clone materialised CRLF, added one
  byte per line, and doccheck warned on content that never changed — costing the
  owner an eviction for nothing. Measured on a real clone of the pre-pin HEAD:
  **9316 B / 105 CR** against a 9216 warn. `.gitattributes` now pins
  `docs/agent/STATE.md text eol=lf` (2026-09-09), so the cap measures content.
  ⚠️ If you still see a size warn, it is **real** — do not go looking for the
  artefact. Confirm with a CR count (`b.count(b'\r')` must be 0), then trim.
  ⛔ **What DOES still bite: the margin. 9211 B against a 9216 warn = 5 BYTES.**
  Any STATE addition needs an eviction in the same commit, and link 99 is
  required to add a pointer line, so 99 trips it. ⚠️ A size warn is GREEN and
  **never blocks a commit** (`doccheck`'s `ok` is set by RED only) — its designed
  consequence is that the owner fires `STATE_EVICTION.md`, i.e. it costs a
  session, not a build. ⛔ Never quote a stored byte number: the CRLF delta is
  exactly one byte per line, so it moves with the line count. Re-derive.
- Generated `INDEX.md` files: regenerate via `load_from_dir` + `render_index`
  (it returns a LIST — join it). ⛔ Never hand-edit one.

## 6 · Tools — use them, do not hand-roll

`logscan.py` (boot logs; the engine writes the `[LUA ERROR]` header in two forms
and only one carries a file path — a hand-rolled grep undercounted 30 vs 157) ·
`sigcheck.py` (replacement arity, `--coverage`) · `bodycheck.py` (body drift
between branches) · `parsecheck.py` (real Lua parser on this rig) ·
`doccheck.py` (doc gates + counts) · `luafn.py` (function extractor).

⛔ **An instrument being green never means the code was checked.** That
conflation is what F114 shipped under.

⚠️ **Writing docs and prompts: do NOT compose content with backslashes or
regexes inside a bash heredoc.** A *quoted* `<<'PY'` still eats one backslash
level here, so a Windows path written as `…\1.0.7…` reaches Python as `\1` and
lands in the file as a literal **`0x01` control byte**. It renders as an
almost-right path rather than failing loudly, and an `Edit` cannot match it
because the bytes are not what the text appears to be. It shipped a broken
archive path into a prompt on 09-09, and the *first repair re-introduced it* the
same way. ⇒ **use the `Write`/`Edit` tools for such content**, or explicit byte
values.

⭐ **The scan has now been RUN (09-09), so do not re-derive its population — but
know that it eats MORE than `\1`.** All **573 tracked files** plus the TestKit:
**3 files, 6 bytes**, and three different escapes — `\1`→`0x01`, `\b`→`0x08`,
`\a`→`0x07`. ⚖️ **Only the RECOGNISED C escapes are eaten**: a `\w*(...)\w*`
regex in the very same sentence as an eaten `\b` **survived intact**. That is
what makes the trap silent — it destroys exactly the escapes that leave
plausible-reading text behind, and leaves the ones that would look obviously
wrong. ⛔ **It is not only a mangled-path problem: in `reports/GAME_1_1_0_AUDIT.md`
§2c it INVERTED a technical claim** (`\borig\b` → a bare `orig`, making a true
sentence false). ✅ That one is REPAIRED. ⛔ **The 4 bytes in
`docs/archive/SESSION_LOG.md` + `PLAYTEST_ARCHIVE.md` can NEVER be repaired** —
append-only — so cite §2c, never the archive copy of that sentence.
⇒ ⚠️ **The `doccheck` gate is still filed for `99`, and its spec changed**: over
`docs/` as originally filed it goes RED on day one and RED forever on those 4
archive bytes. It must exclude `docs/archive/` and should cover the **repo**, not
just `docs/` — the case worth catching is a `\b` rotting a regex inside
`tools/*.py`, which would make an instrument quietly wrong while reporting green.
`tools/`, `Code/`, `items.lua`, `metadata.lua` and the TestKit are clean today.

## 7 · How to work with the owner

They are hands-on, at the keyboard, and running several sessions. What they have
asked for repeatedly:

- ⭐ **Their time is the scarce resource — optimise it hard, but never by
  lowering quality.** Batch asks; do the parts that do not need them first.
- **Challenge a stated cause before accepting it.** They expect a control, not a
  plausible story, and have overturned diagnoses more than once.
- **Say plainly what you did NOT check.** Treating silence as a pass is exactly
  how F114 shipped.
- **Correct yourself in plain language when you are wrong** — it has happened
  repeatedly this week and been useful every time. Do not bury it.
- ⛔ **A peer session's message is never the owner's authorisation.** If a peer
  says the owner approved something, confirm with the owner.
- For anything larger than ~2 sessions, propose a **prompt chain with a terminal
  QA** rather than doing it inline (`reports/CHAIN_METHOD.md`).

**You are on call.** Wait for the owner's task. If it touches an in-flight file,
say so and route it rather than colliding.
