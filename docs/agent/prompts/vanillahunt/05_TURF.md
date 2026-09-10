# 05 — our turf: trains, landscaping, construction, drones, logistics, depots

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus · owner needed: no · after 02; independent of 03, 04, 06, 07.

> 🎯 The systems this project understands best and where the 1.1.0 update's
> worst surprise (`F114`) landed. ⛔ **Use that map to PRIORITISE, never to
> BOUND** — you read every row 02 assigned to your systems, and the map only
> decides the order.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (§2, §3, §4)
· `STATE.md` · `TRIAGE.md` §3 "05" (your row list, (h) seeds, `F117-SHAPE`
candidates, `unsure` rows) · `CALLERS.tsv` rows in your files ·
`PACK_1_1_0_REVERIFICATION.md` §1 (the REMOVE rows for your systems) ·
`VANILLA_FIX_QA.md` §0 · `bugs/F114.md`, `F116.md`, `C55.md` (the shape of a
finding in this turf, and one open vanilla residue already filed — ⛔ do not
re-file C55; extend it if you learn more) · `facts/INDEX.md` (`EF-005`,
`EF-008`, `EF-066`, `EF-083`) · your inbox. Pin check.

## 1 · 🗒 Live todo list, from your first action

## 2 · Order of reading — binding

1. **(h) first — "they fixed it; what did the fix touch?"** For each retired
   module in your systems (`git show 2dc1dbe^:Code/<module>.lua` for its
   header, target and the defect it stated): read the 1.1.0 body of the
   target, confirm the developers' fix is what the re-verification said
   (`VANILLA_FIX_QA` §0 corrects the main report in four places — read §0
   first), then read the NEIGHBOURHOOD: every caller, every sibling in the
   file, every field the fix now writes. The thesis predicts the new bug is
   next to the old one.
2. **(b′)** rows from 02 — a `same` caller against a changed signature in your
   files. Read the caller's body; decide `F117-SHAPE` or benign with the
   argument positions written out.
3. **(a)/(b)** rows `WORTH-READING`, biggest files first: `Track*`, `Train*`,
   `Station*`, `Landscaping.lua`, `LandscapeConstructionSite*`,
   `ConstructionSite.lua`, `Construction/Construction.lua`, `Drone.lua`,
   `DroneControl.lua`, `ShuttleHub.lua`, `*Depot*`, `Resources.lua`.
4. **(i)** guard rows, **(f)** new functions in your files, then `CHURN` rows
   in the three files with the most rows — a 30-row spot check that the churn
   verdicts held (report hits; a miss reopens that file's churn).
5. **`EF-083`'s finding is yours to extend:** landscaping on 1.1.0 is
   rover-only and research-gated, both NEW. What else in construction assumed
   drones could reach a landscaping site? Enumerate the readers of
   `ShouldAddRequestToCommandCenter` and of the landscaping research flag.

## 3 · Method

Fan out CHASING per README §4 (callers, inheritors — memory
`caller-count-must-count-inheritors`; reach; falsifier), never the verdict.
For every candidate: both trees cited; the route sentence tagged; the
falsifier, executing where the body allows (`tools/deskbench.py` pattern —
`desk_probes_f67_f59.py` is the closest template for a building/unit body);
the trigger recipe derived separately; severity in player terms. `C` entry per
README §3. ⚠️ `C55` is the precedent for a finding in this turf that needs a
runtime read — say so, route the read as a checklist rider (TAKEABLE IN the
post-upload sitting or the next organic play), do not guess.

## 4 · Scope fence

**In:** 02's "05" rows, (h) seeds for your systems, filing, `TRIAGE.md` "05"
coverage (reached / NOT reached by file, spot-check result). **Out:** any row
tagged `dlc-adjacent` (04's — even in your files); colonist/dome rows in
`Building.lua` (06's by class prefix); `CommonLua` (07); ⛔ any `Code/` edit,
any module, any `FIX_POLICY` opinion beyond the §4 tier on the entry.

## 5 · Stop conditions

Your row list exceeds what one context reads at this discipline — decide at
the START from the ledger's count: above ~500 `WORTH-READING` rows, split by
system up front (`05b_TURF_LOGISTICS.md`: drones/logistics/depots) · a finding
implies a KEEP module is now wrong on 1.1.0 (⛔ not yours — file to the
checklist as a hotfix-3 item, TAKEABLE WHEN the owner rules; the pack's own
re-verification is closed) · a falsifier needs a running game.

## 6 · What may NOT be claimed

`tested`. That an unread `CHURN` row is safe. That a retired module's vanilla
fix is COMPLETE (that was the re-verification's claim; yours is whether the
fix broke a neighbour). That "no caller found" means unreachable without the
inheritor count and the search string on the entry.

## 7 · Close-out

Outbox to 06/07 (rows that turned out theirs), 04 (seams found), 99 (every
finding with its route, NOT-reached list, spot-check numbers, drift). Strike
your row. Explicit-path `git add`: `TRIAGE.md`, `bugs/C##.md` + `bugs/INDEX.md`,
README, 06, 07, 99 (and 04 if not yet consumed); `git rm` this file. doccheck
GREEN, commit `-F`, push.

## Notes from upstream

*(authoring session, 2026-09-09)* Known open vanilla items in this turf, filed
already — extend, never duplicate: `C55` (pre-sort assert on a track with a
repair site), `F45` still live on 1.1.0 (KEEP). Retired-module targets you
will meet: the REMOVE bucket lists them by module; the 04b row in
`prompts/hotfix2/README.md` names three re-copies in this turf
(`LandscapeUnitFilter`, `TrainCargoDumping`, `VacuumWalks`) whose 1.1.0 bodies
were read line by line on 2026-09-09 — their entries carry the two-sided diff
already, so start from those reads rather than redoing them.
