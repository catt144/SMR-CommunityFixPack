# ONE-OFF AUDIT PROMPT — whole-mod sanity check before wider distribution

**Paste everything below into a FRESH session (any model).** This is a one-off.
Delete it once its findings have been acted on or recorded.

---

You are auditing the Surviving Mars: Relaunched "Community Fix Pack" — the
whole thing, as it stands today — with fresh eyes and no attachment to any of
its past decisions. The people who built it are too close to it. **Your job is
to poke holes: in the code structure, in how the work is organized, and in its
readiness to be distributed widely.** Nothing is sacred, including conventions
the project treats as settled. If something is sound, say so and move on; if
something is bloated, duplicated, mismatched or risky, say so plainly and
propose the better shape.

## The estate

- `C:\Dev\SMR-BugFixPack` — the mod itself (public repo; this is what ships).
  `metadata.lua` + `items.lua` + `Code/` (~70 `Fix_*` modules, ~6 `Opt_*`
  modules, a core registry, a save sanitizer) + `docs/` + `README.md` +
  `LICENSE`.
- `C:\Dev\SMR-BugFixPack-TestKit` — a dev-only companion mod (local-only repo;
  policy: it is NEVER uploaded anywhere).
- `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` — game source,
  **read-only, never modify**. The shipped build is `1.0.7.396349` and its
  packed Lua has been verified byte-identical to this Src tree for all gameplay
  files (see STATUS.md "Key technical facts").
- `docs/STATUS.md` "Key technical facts" — engine behaviors that will otherwise
  produce false findings (the sandbox blacklist, `error()`/`assert()` reporting
  and continuing instead of unwinding, mod code loading before classes are
  built, persistence rules). Read that section before judging any code as
  wrong.
- `docs/FIX_POLICY.md` — the rules the code claims to follow. Audit the code
  against it, and audit the policy itself: is it the right policy?

## Question 1 — the code, structurally

Read `Code/` as a reviewer who has never seen it:

- **Duplication and mergeability.** ~76 files, one per fix, each with its own
  header, logger, self-check and registration. Is there duplicated machinery
  that belongs in the core? Are there fixes that patch the same function, the
  same subsystem, or each other's edges and should be one module? Are there
  fixes that a later fix made redundant? Map every wrapper/replacement target
  and flag collisions or ordering dependencies between files.
- **Load order and coupling.** `metadata.lua` lists files explicitly; the core
  must load first. Is anything order-sensitive beyond that? Do any modules
  reach into each other in ways that break if one is individually disabled
  (the pack promises per-fix disable via `SMRFixPack_Disabled`)?
- **The registry pattern itself.** One global registry, pcall'd applies,
  reason-string deactivation, per-call `IsActive` gates for optionals. Stress
  it: what happens when two fixes wrap the same function and one deactivates?
  What happens on a game patch that changes half the targets?
- **Consistency.** Same conventions everywhere, or drift across the waves?
  (Header quality, self-check depth, logging, naming, probe coverage.)

## Question 2 — the documentation

`docs/` has grown large (a multi-thousand-line BUGS.md, a long STATUS.md,
playtest checklists, design studies, prompt docs, archives). Assess it as an
information system, not as prose:

- Can a newcomer (or a fresh session) find the current truth quickly, or must
  they archaeology through session history? Where does the same fact live in
  more than one place, and have those copies already drifted? (There is at
  least one known past case of a doctrine being corrected in four places.)
- Which documents are load-bearing (something reads them before acting) and
  which are sediment? Propose a concrete structure if the current one is
  wrong: what to keep as append-only history, what to make authoritative
  current-state, what to archive, what to delete. If the honest answer is
  "the bloat is structurally fine", say that and say why.
- Check the docs' own hygiene rules (statuses in two places, same-commit
  description updates, staleness banners) — are they being followed, and are
  they good rules?

## Question 3 — distribution and platforms

This mod is expected to reach **Paradox Mods (PC + Xbox + PlayStation)** and
**Steam Workshop**. Audit release readiness for all of them from the code and
packaging outward:

- **What actually ships?** Decide/verify what belongs in the uploaded package
  vs the repo (docs, README, LICENSE — what do the two storefronts each carry
  and expect?). Is `metadata.lua` complete and correct for both pipelines?
  Note `lua_revision` in metadata vs the shipped build's revision — verify
  what that field does and whether the current value is right.
- **Consoles are the hard case.** Console players have no developer console,
  no file access, and no way to run any manual recovery command; anything the
  mod communicates via logs is invisible to them. Sweep the code for anything
  that behaves differently or degrades on console: `Platform.*` gates,
  achievements interaction, Mod Options availability and widget behavior on
  gamepad UI, anything keyboard/mouse-assumed, performance-sensitive passes on
  weaker hardware, and any fix whose failure mode assumes a human can read a
  log or type a command. Verify against the game source what Paradox's console
  mod environment actually permits — do not assume PC parity.
- **Lifecycle.** A game patch lands on all platforms: walk through what this
  pack does on a changed target (per its self-check design) and whether a
  console player ends up better or worse than unmodded. Same for mod removal
  mid-save on console.
- **Identity and presentation.** Title, description, versioning scheme, the
  optional modules' naming ("experimental" labels), and whether the public
  description (docs/MOD_DESCRIPTION.md) matches what the code actually does.

## How to work

- Static audit: the game does not need to run. Cite `file:line` for every
  code-level claim.
- Read the code before the docs' claims about the code; where they disagree,
  the code is the finding.
- Do not modify game files. Do not modify `Code/` during the audit — findings
  first; fixes are a separate decision.
- The TestKit may be read for context but is out of scope for distribution
  questions (it never ships).

## Deliver

1. **Findings, ranked** — structural holes, duplication/merge candidates,
   policy violations, platform blockers — each with evidence and a concrete
   recommendation.
2. **A documentation verdict** — keep / restructure / trim, with the specific
   proposal if restructuring.
3. **A platform-readiness checklist** — pass/fail/unknown per item for Paradox
   PC, Steam Workshop, Xbox, PlayStation, with what would close each gap.
4. **What you could not verify** and what it would take.

Then **stop and report to the user.** Change nothing without their go-ahead.
