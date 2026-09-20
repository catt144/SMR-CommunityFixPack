# Stand-down audit — can our full-body replacements turn themselves off?

One-off, authored 2026-09-13 at the owner's ask. Tool-neutral (Claude or Codex).
`git rm` this file and its prompt-map row when it has reported. Design record:
[D14](../bugs/D14.md).

Start with `git log --oneline -6`, `git pull`, and `git status --short`.
The job was authored at `6fccbde`; compare its named code, TestKit, D14 and
policy inputs through HEAD, then re-derive only groups that moved.

## 0 · Your licence

**This brief hands you a measurement and a hypothesis, not a conclusion.** Everything
in §2 is a **claim** — house doctrine (`CLAUDE.md`) says authored text is a claim,
including ours. Test what your conclusion rests on and overturn what is wrong;
"the brief was wrong about X" is a better result than a tidy table.

- ⭐ **Read anywhere relevant.** The pack, the TestKit, the archived trees, the
  shipped packs, logs and archive are evidence sources. Write scope remains the
  report/D14/checklist deliverable below; reading authority is not mutation authority.
- ⭐ **Chase your own reading.** If the real exposure is a shape nobody here has
  described, report that instead and say why it matters more.
- ⭐ **The owner's framing may be wrong too.** They said full-body replacements
  *"bug me, I hate them because we cannot guarantee we cleanly stand down."* If the
  measurement says the exposure is small, or sits somewhere else entirely, say so
  plainly — that is a useful answer, not a failure to deliver.

Binding, and these are house process rather than limits on thinking:

- ⛔ **Report only.** No module edited, no shipped Lua changed, no game launched
  without asking first. Propose anything you like.
- ⛔ **Shared tree.** Peers edit concurrently and **Codex is invisible to
  `ListAgents`**; check `git log` / `git status` before any write, commit with a
  pathspec.
- ⛔ **Negative-evidence discipline** (`EF-088`): a "not found" needs its presence
  control counted through the same instrument.
- A checklist item is deleted in the commit that records the owner's action on it (its
  header rule); a checklist-only edit needs no `--regen`.

## 1 · Orient

Use the project and bindings already supplied by `CLAUDE.md` or `AGENTS.md`. Read
`docs/agent/STATE.md`, grep D14 in `docs/agent/bugs/INDEX.md`, then open only
D14's needed sections. Open a **live todo list** and keep it current — the owner
reads it to decide when to step in. Add items for your own lines of enquiry.

## 2 · What is already measured — verify anything load-bearing

Historical seed at `6fccbde`, 2026-09-13 (`Code/Fix_*.lua`, 45 modules):

| measure | count |
|---|---|
| delegate to the captured original | 24 |
| do **not** delegate — candidate full replacements | **21** |
| carry a `Require` gate of any kind | 41 |
| carry a **behaviour probe** | 15 |
| carry a custom `test` | 8 |

The delegation split came from `grep -lE "\borig\b|_orig|original"`. ⚠️ That is a
**crude proxy** — it will misclassify a module that captures under another name, and
one that mentions the word in a comment. **Re-derive it properly**; the 21 is a
starting list, not a finding.

Also established, and cheap to re-check:

- `python tools/bodycheck.py` is at **full manifest coverage** — 132 rows, 47 stamped
  modules, **0 without a manifest**; 120 OK, 9 SRC-NONE, 2 NO-DEFECT, 1 DEFECT-GONE
  (F48's paren, already triaged in `90_SaveSanitizer`). Running it after a patch is
  binding procedure (`WORKFLOW.md:171`).
- bodycheck declares its own blind spot: *"does NOT see semantics moving under a
  wrapper (class c), and sees nothing at all for a NO-DEFECT or NO-MANIFEST module."*
- **MEASURED, our own logs:** `[SMRTest] no debug.getinfo (mod sandbox)` — body and
  bytecode inspection is unavailable inside a mod, so a runtime "did the body change"
  probe is not buildable. Behaviour is the only runtime instrument.

## 3 · The question

**Which modules can a vendor fix land under without any instrument we own noticing —
and what would it take for each to stand itself down?**

The product is **a runtime decline for the player**: a behaviour probe that lets the
module refuse to install when the defect is gone, per `FIX_POLICY` §2a. This is the part
that actually delivers "we stand down cleanly", and it works in installs we never see.

The desk class-c detector is settled and out of scope: it is `GAME_PATCH_INSTRUMENTS.md`'s
D1 (hash everything a module names, one hop out; 10/10 FIX on the 1.1.0 backtest), built
by `tools/patchcheck.py`. Use its one-hop limits (that report's §4) to rank exposure:
a module whose class-c case lies outside what it names is where a runtime decline matters most.

## 4 · Per-module disposition — the deliverable

For each non-delegating module, record:

- **(a) Could it delegate?** Could this be re-shaped as a wrapper that calls the
  shipped body — `FIX_POLICY` §3a layer 3/2 — so a vendor change rides along for
  free? If not, why not (a `MsgReaction` with no stop hook, a preset/data patch, a UI
  rebuild, an `OnMsg` with no original to call…).
- **(b) Does its existing gate detect a FIX, or only a RESTRUCTURE?** A structural
  check (function exists, table shape as expected) passes happily after a vendor
  repair. Only a behaviour test catches one. Say which this module has.
- **(c) Is a class-c case constructible?** Can you describe a concrete change to
  shipped data or a callee that removes the defect while leaving our pinned body
  byte-identical and `bodycheck` reporting OK? ⛔ If you cannot construct one, the
  module is **not** class-c exposed — say so and move on. A module being a full
  replacement is not by itself a finding.
- **(d) What probe would settle it?** Name the observable. If no probe is possible,
  say that plainly — an honest "this one cannot be instrumented" is a real result and
  tells the owner where the irreducible risk sits.

Rank the output by exposure, not alphabetically. The owner wants to know **which few
matter**, not that all 21 were visited.

## 5 · Worth considering, not prescribed

- The TestKit already carries a broad probe set. Emit its current total and
  inventory the relevant probes before proposing new ones.
- A decline probe the post-patch suite A/B can also read (the report's G3) is worth more
  than one that serves the player alone.
- If the honest finding is *"the desk instruments are sufficient and the runtime
  decline is the only real gap"* — or the reverse — say that; it changes what gets
  built next.
- ⚠️ Watch the cost side: a probe set that must run on every game patch has an
  ongoing price in owner time. Price it. `docs/agent/support/CHAIN_METHOD.md` applies
  if this turns out to be more than ~2 sessions of work.

## 6 · Deliverable

A report at `docs/agent/reports/STANDDOWN_AUDIT.md`, and — if anything needs an owner
ruling — a new `### ck<n> · opened <date>` item under `docs/PLAYTEST_CHECKLIST.md`'s
`## Decide` section, in its Must_Read_Header format. Update [D14](../bugs/D14.md) with what the audit settles;
leave it `cand` unless the evidence moves it, and if it moves, change the front
matter **and** the body heading tag.

Label claims SOURCE / MEASURED / INFERRED, keep a **Not opened** list, and say what
each refutation depends on. `doccheck` GREEN before committing; commit with a
pathspec after checking `git status` for a peer's uncommitted work.

## 6a · Derived facts and falsifiers

| fact | measured | falsifier |
|---|---|---|
| the 24/21 delegation split is only a historical seed | proxy grep recorded at `6fccbde` | re-enumerate the current registered module set, inspect each classification, and reconcile against `python tools/doccheck.py --emit-counts` |
| bodycheck had full manifest coverage but declared a class-c blind spot | bodycheck output/source at `6fccbde` | run current `python tools/bodycheck.py` and inspect its current declared limits |
| runtime body inspection was unavailable in the mod sandbox | named TestKit log evidence in the authoring pass | search current TestKit/log evidence with a positive control; do not infer continued absence from the old line |
| D14 remains the design record and this prompt remains named by current status | focused bug-index and STATE reads at execution | re-run the two focused lookups; stop if status or owner authority moved |

## 7 · Live todo list — change it as you go

At execution start mark item 1 `IN PROGRESS` and later items `PENDING`; keep
exactly one unfinished commit-and-verify unit in progress and put stable results
in its text.

- [ ] 1. Orient; re-derive the delegation split properly (the grep is a proxy)
- [ ] 2. Per-module (a)–(d) for each genuine non-delegating module
- [ ] 3. Emit and check the current TestKit probe set for existing coverage
- [ ] 4. Rank by exposure; name the few that matter
- [ ] 5. Price the ongoing per-patch cost of whatever you propose
- [ ] 6. Your own hypotheses — add them here as you form them
- [ ] 7. Report written; owner decision block + marker if a ruling is needed
- [ ] 8. doccheck GREEN; committed with a pathspec; this prompt `git rm`'d
