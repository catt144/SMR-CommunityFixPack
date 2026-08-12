# Chain prompt 4 — the verification matrix: three cells and a witness

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. **Precondition: prompt 3's Notes below carry both HEAD shas and the
predicted readings — verify the shas match the working trees before anything
launches.** The game/Steam must be free (coordinate via the todo list; the
owner is NOT needed at the keyboard — this is the unattended-harness pattern:
parked .txt instruments landed in TestKit `Code/` only for the run, ARM gate
(a script FILE with resolution cross-check) before every launch, instruments
fire on load, no console typing; resurrect the u2-run pattern per WORKFLOW).

**Every cell's reading was PREDICTED upstream. You record readings against
predictions — a miss is a finding, chase its mechanism before filing.**

## The matrix (fresh launch per cell — D13's rule: a Mod-Manager toggle needs
## a FULL PROCESS RESTART to take effect; sequence the cells to minimize
## toggles and note every toggle + restart in the log via the harness)

* **(a) BOTH mods installed+enabled:** opening gate reads both registries
  (predicted `74/74` fix pack + `8/8` opt-in — the emitted numbers from
  prompt 3 are the prediction); suite runs; tally vs predicted; both Mod
  Options pages present (harness-readable or screenshot-free log evidence per
  design); zero `[LUA ERROR]`; zero cross-mod lines. ⭐ **This cell is the
  rig's standing configuration from here on (README rule 12)** — its measured
  numbers are the baseline every future leg quotes, so read them with that
  weight.
* **(b) OPT-IN ALONE** (fix pack disabled + full restart): loads clean,
  `8/8`, its options seed from its own `default_options`; ⛔ zero
  `SMRFixPack`-named lines beyond a loaded save's own recorded-mod-list echo
  (grep the archived log, EF-047); the 8 modules' probes run against its
  registry.
* **(c) FIX PACK ALONE** (opt-in disabled + full restart): `74/74`, suite
  tally re-baselined (this number replaces `77/0/10/0` in the records — it is
  measured HERE, quoted forever), zero references to the opt-in mod.
* **(d) SAVE-COMPAT WITNESS** (runs inside cell (a)): stage a byte COPY of
  `CP15PT15` (a KEPT save that ran with opt-ins ON under the old single-mod
  world; MD5 the original first — protected for this chain), load it, read
  back EVERY item on the persisted-name inventory live (D09 dial modifiers
  by exact id, fields, options state), then save/reload once (R4) and read
  again. Predicted: every name present where the old world wrote it, no
  duplicates, no orphans, zero errors. ⚠️ Mod-id change resets Mod Options
  account state — the dials are expected at BASE here, and that expectation
  is part of the prediction, not a miss (the owner re-ticks once; report it).

## Discipline

- One archived log per launch, copied + MD5'd at close (R8 `git add -f`).
- EF-047: absence claims only from archived files. EF-050: savenames
  verbatim. Staged saves: "deleted, listing verified" (EF-051 HOLD), listing
  BY NAME; the `CP15PT15` original byte-verified untouched at close.
- Any cell missing its prediction: record verbatim, keep independent cells
  running, route per README stop conditions. DISARM at end: TestKit `Code/`
  clean, PROBE SWEEP line in the result commit.

## Close

Append Notes-from-upstream to `05_FABLE_AUDIT.md`: per-cell verdicts with log
names/lines, the measured new baselines (both suite tallies, both gate
reads), the save-compat readings, every unexplained log line verbatim with
age, owner-time actually consumed (predicted: zero), and anything the audit
must settle. doccheck green ×2, commit (`-F`), push what has a remote, delete
this file in the same commit.

---

## Corrections from prompt 2 (QA, 2026-08-12) — these OVERRIDE the body above

The body predates the design. Where it disagrees with `90_DESIGN.md` §6.2,
the design (as amended by the QA block at its top) wins:

* **Cell (a) is TWO sub-cells.** At fresh account defaults the opt-in gate
  reads **`1/8`**, not `8/8` (mod id change resets Mod Options — design
  §2.4): that is cell (a1), 72 PASS / 0 FAIL / 16 SKIP of 88. Cell (a2)
  activates the 7 toggles in-session via the design §4.4 instrument (which
  must fire AFTER ClassesBuilt) and predicts `8/8` and **78/0/10/0 of 88**
  with the SAME 10 SKIP names as u2run3 (read BY NAME).
* **Cell (b)'s `8/8` likewise holds only after activation** — at defaults it
  is `1/8`; match whichever (a) sub-cell you pair it with.
* **Cell (d): the D09 dial modifiers are expected ABSENT after load** — the
  new mod id means base dials, and `PostLoadGame` reconcile REMOVES our ids
  (design §6.2's per-row table). Absence there is the PASS; "every name
  present where the old world wrote it" applies to the POLICY/ACK FIELDS
  (rows 1–3), not the dials. Report population sizes per row, and confirm
  the staged copy actually carries stamps/flags BEFORE the run (QA weak
  claim 2).
