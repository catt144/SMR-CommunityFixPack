# Chain — unattended-3 (the two owner-ruled builds: F85 `dont_pause` flip + C39 compensation)

**Authored 2026-08-14 on the owner's word:** *"Lets go ahead and finish the f85
first since its all unattended."* Both builds were RULED 2026-08-12 (F85: the
flip, on the owner's own proposed fix · C39: extend the compensation, delabel
declined) and queued for "the next unattended build chain" — this is that chain.
**Kickoff: open a session on `01_BUILD_OPUS.md`.** ④ (the launch afternoon)
waits for this chain to close, by the owner's ordering.

## What this chain is

Two code builds, their unattended verification, and the release-surface
reconciliation the new counts force. Everything decision-shaped is already
ruled; this chain builds, measures, and makes the numbers true everywhere:

* **F85** — chained wrapper on `PopupNotification.Init` flipping the
  distress-call confirmation's `dont_pause` (`RivalColonies.lua:535-555`, `:546`
  is the flag's SOLE user) so the game's one non-pausing popup pauses like every
  other. Closes F85's entire remaining reachable surface; disclosed as a
  design-judgment tweak. Full record + ruling: `agent/bugs/F85.md`, checklist
  item 5. The bigger per-site rewrite was DECLINED — do not resurrect it.
* **C39** — extend the automation-law compensation to label-carrying buildings
  outside the compensated classes. Sign MEASURED 2026-08-11 (missing uplift,
  ~50% throughput loss for the four Workshops); repair ruled 2026-08-12 with
  scope WIDENED: **sweep all three automation labels** (`ServiceBuildings`,
  `FactoryBuildings`, the expected Research sibling) for out-of-class members
  and cover every mismatch found. Build-shape candidates + the runtime
  discriminator + the verification bracket are recorded on `agent/bugs/C39.md`
  §2026-08-12 — settle the design there against `FIX_POLICY.md` §1.

## Binding chain rules (the house set, in force verbatim)

1. **Staleness check first, every prompt**: `git log --oneline -10` + `git pull`
   in the fix pack (this repo) and the shared TestKit. Live todo list, updated
   per item.
2. **Inbox/outbox in writing**: each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same commit.
   Folder emptiness is the terminal prompt's done-condition (this README goes
   in the terminal prompt's closing commit). Push after committing (owner
   standing word 2026-08-14).
3. **Recorded facts are claims** — every count via
   `python tools/doccheck.py --emit-counts` at your moment; re-derive routes at
   Src, not from entries' prose. Both entries here have been wrong-then-corrected
   before; their §-dated sections name what is measured vs inferred.
4. **The evidence bar is the frozen one** (owner, checklist 14): `fixed` +
   suite + self-checks + verified save-safety tier. State each build's
   save-safety tier explicitly against `FIX_POLICY.md`; neither build may
   persist anything new without saying so.
5. ⛔ **EF-056 for any game launch**: byte-copy EVERY autosave first and
   reconcile by name after EVERY launch — a copy of an autosave IS an autosave
   to the rotation, and firing is timer-driven. ⭐ EF-051's cloud-restore hold
   is LIFTED (08-14) — "gone" claims need a NAMED listing; any of the 17
   historical strays returning re-opens that fact.
6. **Rig norm: BOTH mods loaded** (owner 08-12); gate lines read the FULL
   bracketed token. Load order TestKit→fix→opt-in (`EF-054`).
7. **`python tools/doccheck.py` before any doc commit; red blocks.** Status
   flips hit BOTH the entry heading tag and the index row (regenerate the
   index, never hand-edit).
8. ⛔ **Nothing is published.** Store uploads, Pages, previews stay ④/owner.
9. **The `context` handoff binds every prompt** (release-3 rule 8 verbatim):
   commit at natural boundaries, never `git add -A`; on the owner's bare word
   `context`, stop safe, commit, write `<NN>_<NAME>_B.md` handing on STATE and
   POSITION (point at sources, successor re-emits), delete your own file, one
   line to the owner.

## Scope fence

**In:** the two builds above; their TestKit probes; unattended verification
(suite + the C39 bracket + an F85 flip reading); the BUGS entries' status
flips; the release-surface count reconciliation (prompt 3's job 3 — cards,
metadata string, site, sheet, STATE).
**Out:** publishing anything · any third fix · re-opening frozen evidence ·
F85's per-site consequence-thread rewrite (DECLINED 08-12) · **D10** (parked;
C39's own entry warns a D10 build would confound a C39 log — C39 is now being
FIXED, but D10 stays parked regardless) · the capture sitting · Save Rescue
(reserve, checklist 17).

## Stop conditions

- A design question neither entry's ruling covers → route to
  `PLAYTEST_CHECKLIST.md` "Decisions waiting on you", continue with the rest.
- The C39 label sweep finds a mismatch whose repair would NOT be covered by the
  ruled shape (e.g. a non-`Workplace` member) → build what the ruling covers,
  route the remainder, never improvise scope.
- The F85 flip proves unverifiable unattended (no route to a popup reading
  without a keyboard) → build + probe what is samplable, record the honest
  boundary, and route the witness question; do NOT claim a screen event from a
  log (the item-29 lesson, same week).

## Manifest

| # | file | what it does |
|---|---|---|
| 1 | `01_BUILD_OPUS.md` | staleness check · settle C39's design per its entry vs FIX_POLICY · build both modules + probes · entries updated · counts re-emitted |
| 2 | `02_VERIFY_OPUS.md` | unattended launches: full suite with new probes · the C39 paused bracket on a staged `CP15PT15` copy · the F85 flip reading · logs archived byte-verified · entries flipped on evidence |
| 3 | `03_AUDIT_FABLE.md` | terminal: backward QA re-deriving both builds vs entries/Src · the release-surface count sweep (cards, `metadata.lua` description string, site fix-list additions + counts, portal sheet, STATE) · shipped-module control over every NEW player sentence, firewalled · empty the folder |

Model placement lives in the FILENAME only; bodies stay model-neutral
(`CHAIN_METHOD.md` §2.10; owner rule 2026-08-04: unattended = Opus executes,
Fable audits). Three prompts sit under §4.0's six-prompt bar.

## ⚠️ The release-surface impact prompt 3 must sweep (named here so nothing ships stale)

Both mods' cards are diff-proven VERBATIM to their audited sources — every edit
lands in the STORE file AND its RELEASE copy, re-diffed. The counts that move
when two modules land: **modules 74→76 · `Code/*.lua` 75→77 · probes 94→(re-emit)
· packaged files 78→80 · the fix-pack card's *"a suite of 94 checks"* · the
card's and `metadata.lua`'s *"Five of the fixes are judgment calls"* sentence
(the F85 flip is a design-judgment tweak — whether it makes SIX is prompt 3's
call to settle CONSISTENTLY across card, metadata, site FAQ and fix-list, with
the reasoning recorded) · the site's fix-list (two new entries in player
language, its 76-entry count, "73 of 74 modules" note) · `RELEASE_PORTAL_PREP.md`
§2/§3/§4 numbers · STATE's build-state block.** The site is terminal-audited:
additions get the shipped-module control + `mkdocs build --strict`, and the
change is recorded in `SITE_BUILD_AUDIT.md`'s ledger style.
