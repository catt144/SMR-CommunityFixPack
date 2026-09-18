# GAME_PATCH_INSTRUMENTS — design the cheap surface sweep, and the tools and probes behind it

Authored 2026-09-18 at `c823e5b`. One-off investigation. Start with `git pull`, `git log --oneline -5`
and `git diff --stat c823e5b..HEAD -- docs/agent/WORKFLOW.md docs/agent/reports/ tools/`; an empty
diff means the facts below hold.

## Decided (owner, 2026-09-18)

- A perma `GAME_PATCH_PROMPT.md` will run after every game patch. Its core is a **surface sweep**
  whose output is a recommendation: **no deep sweep**, a **scoped deep sweep** (only flagged
  modules), or a **full deep sweep** (1.1.0-style), each with its expected cost.
- 1.0.7 → 1.1.0 was major. Its deep sweep proved its worth and was expensive in tokens; the next
  patch may not justify one. The surface sweep exists to make that call cheaply.
- The save-exposure re-check (W42) is one check inside it, not a separate decision.
- **The prompt runs in this repo first, always.** At patch time this is the critical space:
  players cannot turn off individual fix modules. Anything relevant to the opt-in pack goes into
  an **outbox in the fork**, in a `gamepatch/` folder under its perma prompts with a README. Any
  general agent there reads that README and acts on the outbox when the owner asks, with no
  specific prompt needed. The build brief creates the folder; your sketch says what the outbox
  must carry for that to work.
- The owner wants desk tools **and** in-game TestKit items (slots, probes, run in the style of the
  full probe sweep with the game booted) that make the sweep cheap. This brief is the design; a
  separate brief builds what is chosen. **You write no `Code/`, TestKit code or perma prompt.**

## The question

What instruments should the surface sweep run, how does it decide between the three
recommendations, and would that rule have made the right call on 1.0.7 → 1.1.0?

## Evidence so far (each a claim; re-derive what you lean on)

- Both trees are archived under `C:\Dev\SMR-SrcArchive\` (1.0.7.396349, 1.1.0.403908, with
  `MANIFEST.sha256`); `docs/agent/reports/vanillahunt/` holds the `treediff` output for exactly that
  pair, including `CALLERS.tsv`. Check the header lines of `CALLERS.tsv` for the pair and digests.
- `docs/agent/WORKFLOW.md` "After a game patch" is today's procedure and the canonical trust table
  for what `bodycheck`, `sigcheck`, `treediff` and `presetdiff` output can and cannot license.
- It records that **6 of the 10 FIX rows** in the 1.1.0 re-verification were class c: behaviour
  moved under a wrapper whose target body is byte-identical, which `bodycheck` reports as OK. That
  is the gap a bodycheck-only surface sweep falls into. Source: `reports/PACK_1_1_0_REVERIFICATION.md`
  §1a; re-derive the list of modules before using it as your answer key.
- What the 1.1.0 response cost and found: `reports/GAME_1_1_0_IMPACT.md`, `GAME_1_1_0_AUDIT.md`,
  `PACK_1_1_0_REVERIFICATION.md`, `VANILLA_DIFF_DISPOSITION.md`.
- A mod has no `debug.getinfo` (`[SMRTest] no debug.getinfo (mod sandbox)`, recorded in
  `prompts/STANDDOWN_AUDIT.md` §2), so no in-game probe can hash or read a function body.
  Behaviour is the only runtime instrument. Check it against a log before designing around it.
- `prompts/STANDDOWN_AUDIT.md` (live, not fired) asks for a desk class-c detector and a per-module
  runtime decline; [D14](../bugs/D14.md) is its design record. Your class-c work overlaps its
  product 1. Use or supersede it, and say which in the report.
- Saved code: `reports/D13_EXPOSED_SET.md` (five shapes) and [F86](../bugs/F86.md).
- Reach traps any wiring check must respect: `EF-058` (flattened classes) and `EF-066` (composed
  `Init`); a patch that adds a subclass re-declaring a method escapes a fix silently.
- The TestKit's probe total is emitted by `python tools/doccheck.py` (never typed). Its docs are
  `tools/TESTKIT.md` and `tools/SMRTK.md`.

## Leads from the coordinator (offered, not the route; beat, cut or extend them)

Desk:
- A **triage tool** that emits build id, archive status, the fpk diff summary, bodycheck and
  sigcheck verdicts, and every trigger, ending in a recommendation, with no counts typed by hand.
- **Adjacency**: per module, the count of changed functions within one call of its targets, joined
  from `treediff` callers. It is the proposed class-c proxy, and the backtest decides whether it works.
- A **dependency manifest** stored per build: for each module, hashes of its targets' callees and
  the preset fields it reads, so that at patch time "a dependency moved" is a hash compare.
- The saved-code intersection (W42): changed functions against the D13 set.
- The fact groups that moved (`--emit-fingerprint`), turned into a re-derive list.
- Patch notes mapped to the systems we fix (the notes are claims; they only point).

In game:
- **Fire-rate counters**: how often each fix acts over a standard run, compared with the pre-patch
  baseline. A drop to zero or a spike is a behaviour signal for class c. Check whether the pack
  already counts anything.
- A **wiring and reach sweep**: every wrapper live on every carrier class, and new subclasses that
  re-declare a target.
- A **self-check census**: each module's status and reason in one block that `logscan` reads.
- A **preset census** for the classes our modules touch, compared with a stored manifest.

## Deliverable

`docs/agent/reports/GAME_PATCH_INSTRUMENTS.md`:

1. **The instrument set, ranked by value per cost.** For each item: what it catches (name the
   class), whether it is desk or in-game, the build cost, the per-patch cost in tokens **and in
   owner minutes**, and whether it serves the opt-in pack (`C:\Dev\SMR-OptInPack`, same game) too.
2. **The recommendation rule**: its triggers and how they map to none, scoped or full.
3. **The backtest**: run the rule on 1.0.7 → 1.1.0 with the archived trees and the recorded
   findings as the answer key. It must recommend a full sweep, and its flags must cover the class-c
   modules. Report misses by name. Where a lead cannot be tested at the desk, say so and name the
   test that would settle it.
4. **What cannot be instrumented**, stated plainly: that is where the irreducible risk sits.
5. **A sketch of `GAME_PATCH_PROMPT.md`**: steps, and the order in which to drop things when
   budget runs out, plus what one outbox entry for the opt-in pack must contain so an agent there
   can act on it cold. Just the sketch; the coordinator briefs the build.
6. **Asks for the owner** and **out-of-scope findings**, each as a short list.

Any scratch scripts you write stay out of `tools/`; describe them in the report.

## Stops

- The backtest needs something only a running game can give. Design the in-game item, price it
  and stop there; do not ask the owner to boot.
- An instrument's value depends on a ruling (for example, running something on every patch at an
  owner-time price). Put it in the asks.
- Work would touch `Code/`, the TestKit, or a peer's dirty file.

Agents do not scan or read the owner's saves unless the owner asks (owner, 2026-09-18). Fixtures an
in-game item needs are named, not found.

## Do not claim

- "Adjacency catches class c" from a plausible mechanism. Claim only what the backtest measured, on
  the modules it measured.
- Any in-game item "works" from a desk read. Say "designed; untested in game".

## Lifecycle

One-off. The commit that lands the report deletes this file and its row in `prompts/README.md`.
