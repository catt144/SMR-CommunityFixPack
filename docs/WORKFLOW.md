# Development Workflow

## Reading path for a new session

1. `docs/ENGINE_FACTS.md` — the proven engine behaviors (several are the
   opposite of what the code suggests). Read before writing or reviewing any
   fix.
2. `docs/STATUS.md` — current state: authoritative build counts, open user
   decisions, next gates. Session history lives in
   `docs/archive/SESSION_LOG.md` (append-only, newest first).
3. `docs/BUGS.md` — the canonical defect tracker (index + full entries).
   Update it in the same change that adds or edits a fix; statuses live in
   TWO places (index row + heading tag) — never flip one without the other.
4. `docs/FIX_POLICY.md` — how we patch. Binding for every fix.
5. `docs/PLAYTEST_CHECKLIST.md` — the owner's live playtest queue and the
   reporting protocol (tests ONLY, split 2026-07-30); its companion
   `docs/PLAYTEST_HELP.md` carries the ground rules, console facts, the
   verified command table, Test Kit helpers and save-fixture recipes.

## Layout

- **Dev repo (this folder):** `C:\Dev\SMR-BugFixPack` — git-versioned, canonical.
- **Game install:** `A:\SteamLibrary\steamapps\common\Project Spark`
  (Surviving Mars: Relaunched; "Project Spark" is the Steam folder codename).
- **Shipped Lua source (read-only reference):** `<game>\ModTools\Src`
  (`Lua\`, `CommonLua\`, `Data\`, `DLC\`). We never modify anything under the
  game folder.
- **Mod install point:** `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`
  — a directory junction into the dev repo (see below), so edits are live.
- **Companion TestKit** (never shipped): `C:\Dev\SMR-BugFixPack-TestKit`
  (own git repo, local-only by decision — see its README).

## Install for testing

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\Surviving Mars Relaunched\Mods" | Out-Null
New-Item -ItemType Junction -Path "$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack" -Target "C:\Dev\SMR-BugFixPack"
```

Then enable "Community Fix Pack" in the game's Mod Manager. After editing Lua,
restart the game. **Opt-module first-enable caveat is FIXED (audit 2026-07-29):**
hooks now install at file scope, so a first mid-session Mod Options enable
works without a relaunch.

In-game checks: console `SMRFixPack.ListFixes()` prints each fix's status
(active / inactive+reason / disabled / error).

## Per-fix discipline

1. Every fix links to a BUGS.md entry with file:line evidence (FIX_POLICY §4).
2. Before patching, re-verify the target against the cited Src lines; the
   apply() self-check then guards it at runtime and returns a reason string
   (never errors) if a game update changed it.
3. Parse sweep before any commit that touches Lua: python + `luaparser`,
   `ast.parse(open(f, encoding='utf-8-sig').read())` over every edited file —
   a syntax error in ANY listed file breaks the whole pack at load.
4. One commit per fix or tight group; BUGS.md updated in the same commit;
   MOD_DESCRIPTION.md updated in the same commit as the code change it
   describes.

## fpk verification — RELEASE GATE, re-run after every game update

All BUGS.md line numbers come from `ModTools\Src`; the game executes
`Packs\Lua.fpk` + `Data.fpk`. **Parity is PROVEN for the current build
(1.0.7.396349, extraction diff 2026-07-29): 2,250/2,256 shipped Lua files
byte-identical to Src; the 5 divergences are engine/tooling only** (details in
ENGINE_FACTS.md). The discipline guards *future* updates:

1. After every game patch, re-extract `Packs\Lua.fpk` (FLPK container, zstd
   per file) and diff against the new Src tree; re-verify every replacement
   fix's target function byte-for-byte (the ~29 full replacements are the
   pack's patch-rot exposure — C1 in `docs/archive/AUDIT_FINDINGS.md`).
2. Runtime self-checks stay mandatory in every apply() regardless (existence/
   layout checks only — the sandbox has no introspection; they catch renamed/
   removed targets, NOT an edited same-named function — hence step 1).

## ⛔ Probe hygiene — HARD GATE before ANY testing (owner, 2026-08-01)

**No test session — attended or unattended — starts, and NO result is
recorded, until the stale-probe sweep has run and reported clean.** Stale
probes are how false facts got recorded: leftover instrumentation logs, hooks
messages, creates threads, and contaminates both the measurement and the log
it is read from (the 2026-07-31 probes were still armed days after their
questions were answered).

**The sweep (mechanical, one command):**

```
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

**CLEAN =** zero hits, **or** every hit is a probe that THIS session's test
design explicitly declares it needs — named in the brief and in the todo
list. Anything else: the session repairs first (delete the file + its
metadata/items lines, commit) or stops and reports.

**The rules that make this work:**

1. **Every temporary probe/experiment file MUST carry the literal word
   `TEMPORARY` in its header comment** — that is what the sweep greps for.
   A temp probe without the marker is itself a defect: file it on sight.
2. **A probe is STALE the moment its answer is recorded.** Deletion belongs
   in the SAME commit that records the answer (docs-never-lag, applied to
   instrumentation).
3. **The sweep result is part of the record:** every commit that flips a
   BUGS.md status, records a MEASURED fact, or reports a PASS/FAIL carries a
   `PROBE SWEEP:` line — either `clean` or `armed: <files>, declared by
   <test>`. **A result commit without that line is invalid and gets
   re-verified before anything builds on it.**
4. Both repos are in scope (the pack AND the TestKit) — the
   `GetPriorityForRequest` experiment that seeded ENGINE_FACTS lived in the
   PACK's code list.

## Testing checklist per fix

1. Load a save (or new game) where the bug reproduces; confirm reproduction
   with the mod disabled.
2. Enable mod; confirm fixed behavior.
3. Confirm no error spam in the log (`%AppData%\Surviving Mars Relaunched\logs`).
4. Save with mod enabled → disable mod → load: game must not break (PT-20
   shape; FIX_POLICY §3).
5. Update BUGS.md status to `tested` (both places) per the checklist's
   reporting protocol.

The TestKit's `SMRTest.RunAll()` A/B pair (baseline vs full pack) is the
regression harness; run it as pre-flight when STATUS says one is owed.

## Release steps

- Owner tasks first: preview image (PDX ≤2 MB / Steam ≤1 MB), screenshots,
  portal rules check for console publishing (`docs/archive/AUDIT_FINDINGS.md` plan 2.5).
- metadata.lua: bump `version_major`/`version_minor`, refresh `last_changes`.
  `short_description`, `ignore_files`, `optional_mod` are already in place
  (audit 2.1). `lua_revision` stays 350453.
- MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the
  ClassicRockets export half; sync the fix list with BUGS.md statuses.
  **Recount the probe number** quoted in the "What we can promise, and what we
  can't" block — it moves whenever a wave file gains or loses a probe, and a
  stale number there is a false claim in player-facing text. Authoritative count
  is in `STATUS.md`.
- **Drone overhaul, if it has shipped by then:** its design-drift disclaimer is
  MANDATORY (owner requirement — spec in `docs/DRONE_RESEARCH_BRIEF.md`). Do not
  publish the module without it.
- Upload via the in-game Mod Editor (Paradox Mods / Steam Workshop). The
  editor round-trip is SAFE since audit 2.2: items.lua carries one
  `ModItemCode` per Code/ file in metadata order, so SaveDef regenerates the
  same `code` list. If a Code/ file is ever added/removed/reordered, update
  BOTH metadata.lua `code` AND items.lua in the same commit, same order.
- The TestKit must NOT be uploaded.
- Credit ChoGGi (Fix Bugs) + LukeH (Martian Express) as prior art — and the
  prior-art survey (`docs/PRIOR_ART_SURVEY.md`) backs the save-safety claim in
  player-facing text.
- **Save-exit gates (owner, 2026-07-31 — release blockers alongside the fpk
  diff):**
  1. the **uninstall procedure** is published in MOD_DESCRIPTION ("update,
     load, save, then uninstall", backup-first) and is true (latched heal +
     rains migration shipped and verified);
  2. the **standalone save-rescue artifact** (`BUGS.md` **D13**) is built and
     tested, ready to publish (the only console-viable remedy). ⛔ Its spec is
     GATED on Tier 1/2 landing and verifying — scoped against their measured
     output, never today's leak set. ⚠️ **A second shipped artifact doubles
     this checklist**: it needs its OWN metadata, preview image, description,
     PDX portal pass and console cert, plus a version-skew statement (which
     pack versions' residue it handles) and proof its own residue is zero —
     budget the release window accordingly;
  3. the **residual disclosure** (inert layer-2 residue; irreversible-history
     class) appears wherever save-cleanliness is claimed;
  4. after EVERY game update, alongside the fpk extraction diff, **re-run the
     five-shape exposure enumeration** (class-method / table-slot / global
     assignment / preset-field / own-thread) — a live game means persisted-body
     version skew is a standing failure mode, not a launch-time one.

## Authoring a prompt / job brief — required elements

Every brief written for another session (`*_PROMPT.md`, `*_BRIEF.md`,
`*_REVIEW.md`) must include these. They are not optional polish; each one exists
because its absence cost this project something.

**1. A live progress list — REQUIRED, and required to stay current.**

The owner reads the session's todo list to decide **when to step in** — whether
there is time to start a playtest, whether to wait, whether a job is nearly
done. A list that is created and then not maintained is worse than no list,
because it actively misleads that decision.

So every brief must instruct the agent to:

- **Create a todo list covering the whole job before starting.**
- **⚠️ GRANULARITY: one item per commit-and-verify unit — this is the rule that
  actually matters.** If a stage produces its own commit, or its own
  verification run, it is its own item. Never bundle several of those behind one
  checkbox. *Observed failure, Phase 4, 2026-07-31:* the list carried
  `S6a-d: Require migration in 4 waves` as a **single** item covering four
  waves, four commits and four legs — so the owner saw the list at S4 and the
  next time it moved it read "final phase", with no signal across the longest
  stretch of the job. Per-item discipline cannot fix a list that is coarser than
  the work.
- **If a stage turns out to contain more units than the brief anticipated,
  expand it in the list at that moment** — do not carry one checkbox through
  work you have already discovered is four things.
- **Mark each item complete the moment it completes** — before starting the
  next one, never as a batch at the end. "I'll tidy the list later" is the
  failure mode.
- Keep **exactly one item in progress** at a time.
- **Rewrite the list when reality diverges** — if a stage splits, grows, or
  turns out unnecessary, the list changes. A stale item is a wrong answer to
  the owner's question.
- Put **useful state in the item text** where it is short and stable (which
  stage, what the last verification read), so the list answers "where are we"
  without the owner reading the transcript.

**2. `git log` + `git pull` first**, and a named commit to check staleness
against — briefs go stale the moment another session commits.

**3. An explicit scope fence** — what is in, what is out, and what to do with
something interesting found out of scope (**file it, do not fix it**).

**4. Stop conditions** — the situations where reporting beats pushing through,
stated as permission, not as failure.

**5. What may NOT be claimed** — for any brief that ends in a verdict or a
certification. An agent that cannot cite evidence for a claim must say the
narrower true thing instead.

**6. Whether the brief deletes itself.** One-off jobs delete their brief on
completion (precedent: the popup audit). Re-runnable ones say plainly that they
do not.

**7. The stale-probe gate — for any brief that runs or records a test.** The
brief must instruct: run the probe sweep (the hard gate above) BEFORE testing,
put the sweep line in the todo list, and refuse to record results without it.
A brief that omits this is non-compliant; add the gate before running it.

## `[FAQ]` — the tag for "a player will ask about this"

Owner intends to write an FAQ doc at some point. Rather than start one early
(and rather than let the material scatter), **tag the source of truth in place**
with the literal marker `[FAQ]` and collect it later:

```
grep -rn "\[FAQ\]" docs/ Code/
```

Rules that keep the tag worth having:

- Put it on the **entry that already explains the thing** — a BUGS.md entry, a
  parked item, a module header. Never create a doc just to hold a tag.
- Tag **behaviour a player could reasonably mistake for a bug**, or a question
  the design deliberately answers "no" to. Not every quirk.
- A `[FAQ]` tag is **not work and not a promise** — it is a bookmark. Writing
  the FAQ is a launch-time task, and tagging things is not progress toward it.
- If the tagged behaviour is later changed or fixed, **remove the tag** in the
  same commit, or the FAQ inherits a stale answer.

Currently tagged: D01's parked-rocket activation limitation (`BUGS.md` D01
entry + `FUTURE_IDEAS.md` entry 2); the save-repair framework's honest-limits
wording (`BUGS.md` F03/F35 + the sanitizer section of `MOD_DESCRIPTION.md`).
