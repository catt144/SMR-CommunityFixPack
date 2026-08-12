# Chain prompt 5 — adversarial audit, integration, chain close

**Read `README.md` first — binding chain rules apply. You are the terminal
prompt: this folder must be EMPTY when you finish.** Staleness check (both
repos), todo list. Precedents set the floor: corun-pt15's and corun-pt60's
audits (SESSION_LOG 2026-08-11/-12 — logs byte-compared over the FULL length
and read whole, every conclusion re-derived from the logged numbers, residues
the upstream left unruled get ruled).

**Every "done", "PASS", "clean" and predicted-vs-read verdict upstream is a
claim.**

## Job 1 — audit the record

* Byte-compare every archived log against its on-disk original over the FULL
  length; read each whole. Re-derive every matrix-cell verdict from the logs'
  own lines: recount gate reads and tallies (never trust a quoted tally —
  count the verdict lines), grep cell (b) for `SMRFixPack` yourself, settle
  every absence claim HERE (EF-047).
* **⛔⛔ Invariant 6c re-audit:** take the persisted-name inventory and
  re-derive it from the SHIPPED post-split code one more time (both repos),
  then check cell (d)'s readings name-by-name. A break here outranks
  everything else in this chain.
* **Invariant 6a/6b re-proof on the shipped trees:** the grep-proof (zero
  `SMRFixPack` in the new repo's executable code) re-run; the patch-point
  disjointness re-enumerated post-move.
* **Baseline honesty:** the new measured tallies and gate reads replace the
  old ones EVERYWHERE a future session would read them (STATE both repos,
  WORKFLOW references, checklist) — the old `77/0/10/0`-era numbers survive
  only in archive/history. doccheck `--emit-counts` re-emitted both repos.
* Whole-log sweep per WORKFLOW: unexplained lines verbatim with age; F99
  `TrackElement.lua:805` and C45 `invalid pos` watches; cheat markers vs
  disclosures; a missing archived log is an automatic finding.
* Save close-out: staged saves "deleted, listing verified" BY NAME (EF-051
  HOLD unchanged unless the owner has announced the untick — then route the
  post-untick cleanup as a named task); `CP15PT15` original byte-verified.

## Job 2 — the no-retraining acceptance test (rule 8, owner requirement 3)

With THIS repo's docs closed, answer from the NEW repo alone: build state?
policies (fix/doc/probe hygiene)? each module's record and where its history
lives? how to run the suite and read a gate? what is banned? provenance of
every ported artifact? **Each answer cites the new-repo file that gave it.**
Any answer that needed this repo → fix the scaffolding NOW, then re-run the
test. The test's transcript goes in the new repo's records.

## Job 3 — the ledger

Sitting-class misses vs the standing stacks (recurred = repair WORKFLOW
surgically; NEW = record); owner-time honesty (predicted zero — actual, and
whose); economics one line. CHAIN_METHOD one row ONLY if this chain taught
the method something new (a cross-repo split is a new chain shape — judge
honestly whether it earned a row).

## Job 4 — integrate and close

Both repos: entries carry verdicts; checklist item 15 gets its final state;
STATE both repos (this one: split DONE + NEXT = D13 chain; new one: its own
honest state + what is owed); **ACTIVATE the dormant WORKFLOW clause
"BOTH MODS LOADED is the rig's NORMAL condition" here (strike its dormancy
note, stamp cell (a)'s measured baseline into it) and install its twin in the
new repo's WORKFLOW** (README rule 12 — the owner keeps both mods loaded from
here on; STATE gate-read expectations in both repos say so); SESSION_LOG
record newest-first HERE (cite the pre-deletion sha; the new repo's log
records its own birth); delete every remaining file in this folder in the
closing commit. doccheck GREEN ×2, push what has a remote. **The owner report ENDS with the next kickoff: the D13
chain — derive the exposed set over BOTH post-split trees (it is not
authored; say what authoring takes).** Also carry to the owner: the display
name + description decision (launch prep), the GitHub-remote question, the
one-minute Mod Options re-tick, and the opt-in default ON/OFF recommendation
from the design (if the owner has not already ruled it).

## Stop conditions

- A matrix verdict fails audit and the logs cannot settle it → correct
  visibly, re-route to the owner, keep closing.
- The chain ran partial → audit what ran, inventory the remainder as TAKEABLE
  work items, still empty the folder.

## ⛔ What you may not claim

- Not "standalone" without cell (b)'s archived-log grep re-run by you.
- Not "save-compatible" beyond cell (d)'s name-by-name readings.
- Not "the fix pack is unaffected" without cell (c)'s recounted tally.
- Not "gone" for any staged save while the EF-051 hold stands.
- Not "the owner can work in it cold" without Job 2's cited transcript.

---

## Notes from upstream (prompt 4 — the matrix, 2026-08-12)

**EVERY CELL RAN. NINE LAUNCHES, ZERO OWNER MINUTES, ZERO `[LUA ERROR]`.** Nine
archived logs, `docs/archive/sp*_Mars.exe-20260812-*.log`. Two predictions
missed; both mechanisms were chased to ground before anything was filed, and
neither is a port defect. One close-out failure is MINE and is reported below in
full — it cost the owner a file.

### ⛔⛔ FIRST: the preconditions prompt 3 handed me were BOTH already stale

**(i) The owner enabled the mod and re-ticked everything at 18:30, before I
started.** Prompt 3 asked them to enable it and ⛔ NOT to re-tick; checklist item
15 said the minute was owed *only after this leg reported clean*. They did the
whole thing at once — their log is
`Mars.exe-20260812-18.30.09-6a22b86d.log`, and it is a **gift**: it is the ONLY
recording that will ever exist of the fresh-account-default state, because
ticking the boxes wrote the account key permanently.

* `:277-285` — the mod loads at fresh defaults: **7 × the exact predicted string**
  `<id>: inactive (opt-in module, off by default — enable it in Options → Mod
  Options)` + `DroneStatDials: applied` = the predicted **`1/8`**.
* `:295-304` — they then tick the seven; `Loaded mod items for:` grows to all
  three mods and all seven log `applied`. **`8/8`**.
* ⇒ **cell (a1)'s GATE half is banked from the owner's own hands**, and it is
  worth more than my (a1) run, which could only DEACTIVATE in-session.
* ⚠️ And they set **both dials off base** — `DroneSpeedDial=5x`,
  `DroneCarryDial=+2`, read live in four separate launches. **This is what
  falsified the design's cell-(d) dial prediction. See below.**

**(ii) "Owner NOT needed at the keyboard" DOES hold for the whole matrix — I
found a way, and it is new.** Prompt 3 said cells (a)/(b)/(c) are three
Mod-Manager configurations costing three owner visits. They are not: **taking
the JUNCTION out of the Mods folder is a real uninstall that never touches
account storage.** Route re-derived from Src, measured twice, and written up as
⭐ **`EF-055`**. `GetModsToLoad` filters a missing id into a LOCAL list with a
non-modal `ModMessage`; the only routine that would `TurnModOff` +
`SaveAccountStorage` + block on a modal is `WaitErrorLoadingMods`, reached ONLY
from `OnMsg.PreGameMenuOpen`, and `Msg("PreGameMenuOpen")` exists in exactly one
place in the whole Src — inside the `OpenPreGameMainMenu` that Surviving Mars
Relaunched **overrides at `Lua/init.lua:1` without it**. Dead code.
**MEASURED, not just derived:** after the fix pack's junction came out and went
back, the restore launch read `74/74 + 8/8`, the same mod load order, and the
dials still at `5x`/`+2`. ⇒ **The owner's three visits cost zero.**
⚠️ **Audit this hardest** — it is the one place I substituted a mechanism the
design did not name, and every cell (b)/(c) reading rests on it.

### The matrix, measured

⭐ **The comparison world is fixed:** every suite cell loaded `SPSTAGE`, a byte
copy of `PT35FIXTURE` — which is what `U2STAGE` was, so the displaced
`77/0/10/0` baseline (u2run3 `:983`) and these tallies describe the same colony.

| cell | predicted | **measured** | log |
|---|---|---|---|
| **(a2)** both mods, toggles ON | `74/74` + `8/8`; 78/0/10/0 of 88 | ⭐ **EXACT** | `spa2_…18.44.24` |
| **(a1)** toggles off | `74/74` + `1/8`; 72/0/16/0 | ⭐ **EXACT** | `spa1_…18.55.49` |
| **(c)** fix pack alone | `74/74` + registry ABSENT; 70/0/18/0 | ⭐ **EXACT** | `spc_…18.57.05` |
| **(b)** opt-in alone | opt `8/8` + fix ABSENT; the 8 opt probes as in (a2), no other PASS | ⚠️ **two deviations, both chased** | `spb_…18.58.24` (run 1), `spb2_…19.01.40` (run 2) |
| **(d)** save witness | dials ABSENT; fields present | ⚠️ **dial premise falsified; witness 1 too thin** | `spd_…18.45.47`, `spd2_…18.50.43` |
| **(e)** ⭐ NEW — active save contract | — | ⭐ **0 of 3 fields broke** | `spe_…18.53.42` |
| restore control | standing config back | ⭐ **EXACT** | `sprestore_…19.02.50` |

⭐⭐ **THE STRONGEST NUMBER IN THIS LEG, and it is not a tally.** I diffed all 88
(a2) rows against u2run3's 87, `probe status` by `probe status`. **The ONLY
difference in the entire suite is `OptionsMenu PASS` → `OptionsMenuOptIn PASS` +
`OptionsMenuFixPack PASS`.** Every one of the other 86 rows carries a
byte-identical verdict, and the 10 SKIP names are the same 10. The port changed
nothing, and that is a falsifiable claim that was given every chance to fail.

⛔ **The new standing baselines** (README rule 12 — cell (a2) IS the rig's normal
config from here): **`fix pack present: 74/74` · `opt-in pack present: 8/8` ·
`78 PASS / 0 FAIL / 10 SKIP / 0 ERROR` of 88**, SKIPs BY NAME:
`CaveInsNoDisasters MilestoneCrash TrainsToVoid BrokenTrackSalvage
TrackSalvageWipe LakeEntombment GhostFarmOxygen LowStorageWarning
AnomalyCaveInMap TechDescriptionBuilding`.
⭐ **EF-054's open question is CLOSED by observation:** the rig's load order is
`1:SMR_CommunityFixPackTestKit 2:SMR_CommunityFixPack 3:SMR_CommunityOptInPack`
in all four both-mods launches — **the opt-in mod loads LAST, so its wrappers sit
OUTERMOST.** That is what makes deviation 1 below reachable at all.

### ⚠️ Deviation 1 — cell (b) `LanderReturnFuel` ERRORed, naming the opt-in mod

Verbatim: `Mod/SMR_CommunityOptInPack/Code/Opt_ClassicRockets.lua:89: attempt to
call a nil value (method 'IsPlayerControlled')`.

**Mechanism, chased before filing.** `Opt_ClassicRockets` wraps
`UniversalRocketBase:GetFuelResourceRequest` and its guard reads
`(amount or 0) <= 0 and IsActive(...) and not self.arrival_loc and
self:IsPlayerControlled()`. With the fix pack PRESENT, `Fix_LanderReturnFuel`
returns a non-zero amount and the FIRST conjunct short-circuits. With the fix
pack ABSENT, vanilla returns 0, the conjunction runs on, and
`self:IsPlayerControlled()` is reached **for the first time in this project's
history** — because "opt-in without the fix pack" only became a reachable
configuration today.

⛔ **NOT a mod defect, and the control is in Src:** `IsPlayerControlled` IS
declared on the class (`Lua/UniversalRocket.lua:2140`) and reads nothing but
`self.RocketType`; every real rocket has it. The probe's fixture is a **plain
table with no metatable** that borrows class methods by name
(`GetDepartureLocType = R.GetDepartureLocType`) and had never needed this one.
⇒ **a TestKit gap the split's own cell (b) found.** REPAIRED in the same idiom
(`IsPlayerControlled = R.IsPlayerControlled` on both fixtures,
`20_Probes_Wave2.lua`), parse-swept, and cell (b) **re-run**: the ERROR became a
FAIL, which is the correct verdict with the pack absent. ⚠️ The repair is inert
in every other configuration (the conjunction never reaches it), so (a2)/(a1)/(c)
did not need re-running — **audit that claim.**

### ⚠️ Deviation 2 — one probe PASSes in cell (b) that the design said none should

`FactionFundingCheck` PASSes with the fix pack absent. Its own message says why:
`returned 0 (non-discriminating: engine tolerates pairs(nil) — not evidence)`.
⇒ a **self-documented, pre-existing probe-design gap**, not a port defect and not
new today. Final (b): **9 PASS / 69 FAIL / 10 SKIP / 0 ERROR** — the 8 opt-in
probes exactly as in (a2), plus this one. **Not repaired**: it is a probe-design
question with an owner-visible cost, and repairing it mid-matrix would have
broken comparability. Yours to rule.

### ⚠️ Deviation 3 — the cell (d) dial prediction was falsified BY ITS PREMISE

Design §6.2 predicted the two D09 modifiers **ABSENT** after load, because
"the mod id changed, so the dials read BASE". **The dials do not read base** —
the owner set them to `5x`/`+2` at 18:30. Run 1 could not tell a correct
application from stale residue, so I added a dial-position read and the
modifier's own fields, and re-ran:

* `label_modifiers["Drone"]["SMRFixPack_DroneSpeedDial"]` → `prop=move_speed
  percent=400` = 5x. `["Consts"]["SMRFixPack_DroneCarryDial"]` → `amount=2` = +2.
* ⇒ **presence is the module reconciling to the CURRENT dial positions, exactly
  as `Opt_DroneStatDials.lua:42-44` documents.** The design's PREDICTION was
  wrong; its stated MECHANISM was right. And presence is the **stronger** reading:
  it shows the ported module writing the persisted ids under their original bytes.
* Cell (e) proved it moves both ways: forced to `3x` → `percent=200`, restored.

### ⛔ Cell (d) run 1 fired the design's own "thin witness" clause — and the repair turned out to be a cell the design did not have

`CP15PT15` carries **ONE dome and 116 buildings** and read **0 / 0 / 0** on the
three field rows. Per design §6.2 I staged two more — byte copies of `CP60RT` and
`Autosave Sol 311`, the owner's real ~300-sol campaign:

| row | `CP15PT15` | `CP60RT` | `Autosave Sol 311` | `PT35FIXTURE` (cell e, before any write) |
|---|---|---|---|---|
| `SMRFixPack_closed_to_new_residents` | 0 of 1 dome | **4 of 10** | **4 of 10** | **4 of 11**, one `= true` |
| `SMRFixPack_no_homeless` | 0 of 1 | 0 of 10 | 0 of 10 | **2 of 11, both `= true`** |
| `SMRFixPack_ack_notworking` | 0 of 116 bldg | 0 of 540 | 0 of 540 | **1 of 618** (`MDSLaser#9057=true`) |
| CONTROL `SMRFixPack_F48_StationConnectors` | `true` | `true` | `true` | `true` |

⭐ **The best passive witness was the suite world all along** — `PT35FIXTURE`
carries **all three** fields, written by the OLD single-mod world, and the PORTED
modules read every one of them back under its exact original bytes. Both campaign
witnesses agree with each other on the same four dome handles. Round trips: 0
field readings changed anywhere; the only `INVDIFF` rows are total-object counts
moving by 1–2, which is the sim running at speed 1.

### ⭐ Cell (e) — the cell I added, and the one that actually CLOSES invariant 6c

A passive witness can only read what a previous world happened to leave; if the
owner never used a policy, no save can be staged to fix that. So cell (e) WRITES
the contract the way the player's click does (`obj[FLAG] = true` — the modules'
only writer, e.g. `Opt_AcknowledgedWarnings.lua:105`), moves both dials through
the module's REAL Apply path, saves, reloads, and compares **handle sets**, not
counts. **FORCED:** the field writes and the dial positions. **MEASURED:** that
the exact bytes survive on the same objects.

```
SMRFixPack_ack_notworking          before 4 [2851,5342,6300,9057] -> after 4 [2851,5342,6300,9057]  IDENTICAL
SMRFixPack_closed_to_new_residents before 11 [1243,1367,1506,2285,2653,2962,5276,6396,8299,8631,8984] -> after 11 [same]  IDENTICAL
SMRFixPack_no_homeless             before 11 [same 11] -> after 11 [same]  IDENTICAL
0 of 3 field(s) broke the save contract
```

### ⛔⛔ THE CLOSE-OUT FAILURE — IT IS MINE AND IT COST THE OWNER A FILE

**Two of the owner's HELD autosaves are gone. One I restored byte-exact; one I
cannot.** Written up as ⭐ **`EF-056`**, and it is a NEW harness-defect class.

Loading a byte COPY of a real campaign **still runs that campaign's autosave**,
and `Autosave()` (`Savegame.lua:1484-1528`) writes a new one and then runs
`for i = (AutosaveCount or 1), #autosaves do DeleteGame(autosaves[i]) end` — a
loop starting **AT** the count, so at `AutosaveCount = 1` it deletes every
pre-existing autosave. Directory, BY NAME:

| | 18:33, before | 19:04, close-out |
|---|---|---|
| `Autosave Sol 306.savegame.sav` | present, 55,419,123 B | ⛔ **ABSENT — NOT RECOVERABLE** |
| `Autosave Sol 311.savegame.sav` | present, 54,885,560 B | ✅ **RESTORED byte-exact**, MD5 `D5BCCF2CB758D5E5EA0706D671602AF5`, original mtime |
| `Autosave Sol 311(2).savegame.sav` | absent | present, mtime **18:52:43** — inside the cell-(d) process |

`Sol 311` came back only because I happened to have staged a byte copy of it as a
witness; `Sol 306` was never copied. ⇒ **WORKFLOW's "use a designated COPY"
protects the campaign FILE and not the save DIRECTORY.** Routed to the owner on
the checklist. Steam Cloud is ON (`EF-051` HOLD), so `Sol 306` may return at a
future launch — that is a thing to CHECK, never to claim.

### Close-out state, all of it verifiable

* **Protected originals, MD5 re-read after the whole matrix:** `CP15PT15`
  `D2887D754C44134141B6CCC4C9020446` (matches prompt 3), `CP60RT`
  `7467573DB43EF0D61ED36FE50A131EE6`, `PT35FIXTURE`
  `D721329D1EE18604B3D6C89401F74738` — **all byte-untouched.**
* **Staged saves: "deleted, listing verified" BY NAME** (EF-051 HOLD) —
  `SPSTAGE SPWIT SPWIT2 SPWITB SPWITC SPWITRT SPWITBRT SPWITCRT SPCONRT`, and a
  post-deletion `SP*` listing returns nothing. 79 `.sav` remain.
* **DISARM GATE: GREEN · PROBE SWEEP: clean** (all three `Code/` trees).
  ⚠️ The three parked instruments (`97_SPCommon.lua.txt`, `98_SPRun.lua.txt`,
  `SP_ARM.ps1.txt`) are LEFT IN THIS FOLDER on purpose so you can audit them;
  **you delete them when you empty the folder.**
* **doccheck GREEN**, counts unchanged (`74` registered / `75` files / `88`
  probes / `102 F + 12 D + 46 C`). `EF-055` + `EF-056` added, INDEX regenerated.
* ⚠️ **The TestKit carries one change from this leg** (the `LanderReturnFuel`
  fixture). An `account.dat` byte backup taken before the first junction removal
  is in the session scratchpad; it was never needed.

### What the audit must settle

1. **`EF-055` is the load-bearing claim of this leg.** If the junction route is
   wrong, cells (b) and (c) are wrong. Re-derive it; do not inherit it.
2. **My "the fixture repair is inert elsewhere" claim** — I did not re-run
   (a2)/(a1)/(c) after it. Check the reasoning or re-run one.
3. **`FactionFundingCheck`** — a probe that cannot fail. Rule on it.
4. **Cell (a1) is an in-session APPROXIMATION** (deactivated, not never-activated;
   hooks installed, `on_activate` side effects already run). Its gate half is
   independently banked from the owner's 18:30 log; its TALLY half is mine. Say
   whether the tally is quotable.
5. **`Autosave Sol 306`** — my loss, owner-routed. Confirm the routing is honest
   and check whether Steam Cloud returned it.
6. **Owner-time actually consumed by this leg: ZERO minutes.** The 18:30 minute
   was spent before I started, on prompt 3's ask. Machine time: 9 launches,
   ~19 minutes wall clock, 18:44 → 19:03.
