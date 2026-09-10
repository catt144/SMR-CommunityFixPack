# 03 — the seam: class (g), where the owner's thesis predicts the yield

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: **Fable** (recommendation; the owner assigns — README §1) · owner needed: no ·
after 02; **independent of 04** (the hunt) — the two may run at once, they share no rows.

> ⚖️ *"They are famous for not correctly judging how old features will interact
> with new ones."* This link reads every row 02 tagged `dlc-adjacent` and every
> row 03 handed over — **the base-game changes made to accommodate the DLC,
> which ship to EVERYONE, DLC owner or not** (`DLC_DEEP_CHECK` §1.1). The DLC's
> own Lua is mostly new classes; the breakage lands HERE, in old code that now
> has to know about food, meals, farms, laws and a sponsor it never had. Your
> rows are BOTH the `dlc-adjacent` Lua rows and the `dlc-adjacent` preset rows
> (02 tags `PRESETS.tsv` too) — the food registries are yours at field level.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (§2, §3, §4)
· `STATE.md` · `TRIAGE.md` §1–§4 (your row lists are §3 "03") · `INVENTORY.tagged.tsv`
and `PRESETS.tagged.tsv` rows tagged `dlc-adjacent` · `CALLERS.tsv` rows in your set · `DLC_DEEP_CHECK.md`
§1–§2 (the seam list; ⛔ its "mostly additive" premise is a CLAIM that chain
attacks — you neither rely on it nor rule on it) · `facts/INDEX.md` · your
inbox. Pin check.

## 1 · 🗒 Live todo list, from your first action

## 2 · The two questions, asked of every row

1. **The owner path.** With the DLC present, does the old system still do what
   it did? A changed `Colonist` consumption body, a `FoodServiceBuilding`
   branch, a `Resource` table walk that now meets `Meal` — read the 1.0.7 body,
   read the 1.1.0 body, name the old behaviour, name what the new feature
   inserted, then ask what the OLD code assumed that the insertion breaks:
   a table it iterated with `ipairs` that now has holes; a count it cached; a
   label it filtered by class name; a `const.` it read that moved.
2. **⭐ The non-owner path.** `IsDlcAvailable("norman")` appears **3 times** in
   the base tree and `("thomas")` **once** (`DLC_DEEP_CHECK` §1.2, MEASURED
   2026-09-08 — re-derive the count first). Base Lua references DLC content in
   12 files. For every reference in your rows: is the DLC name a genuine
   dependency (nil class, nil preset, nil resource when the DLC is absent) or a
   name collision with base content (`Lua/Buildings/FungalFarm.lua` exists in
   BASE; `FungalFarmBase` is the DLC's)? ⛔ **Enumerate both directions** — the
   absence rule (README §2). A base-game function that indexes a DLC preset
   unguarded is a finding for every player WITHOUT the DLC; that is the class
   the developers are least likely to have tested and the severity sorter
   every finding here must answer.

## 3 · Method

- **Sort:** (b′) `F117-SHAPE` rows first (a base caller keeping an old contract
  the DLC work changed), then (a) body-changed rows in `Colonist`, `Dome`,
  `Building`, `FoodServiceBuilding`, `Resources`, `UpgradeUnlocks`,
  `ConstructionSite`, then (i) guard rows, then (f) new call sites, then the
  preset rows by registry (`CropPreset`, `Meal`, `Resource`, `LawDef`,
  `PolicyDef`, `Tech`, `Cargo`) — field-level, the CONSUMER named by
  `file:line` per row, the way 04 §3.E states it.
- **Fan out chasing, not judging** (README §4): one agent per candidate to
  enumerate callers/inheritors and the non-owner path; it returns a paragraph
  with citations in BOTH trees; you rule. ⛔ The seam judgement is yours — a
  seam is a relation between two systems and an agent that saw one row cannot
  see it.
- **Falsify before filing:** for anything with a synchronous, side-effect-free
  body, a `tools/desk_*.py`-style two-tree run (README §3) that shows the old
  behaviour on 1.0.7 and the new on 1.1.0 with the DLC-absent stub — that is an
  executing non-owner-path control, and it is cheap.
- **Recipe separately from diagnosis** (README §3). Name the trigger, not the
  code path; name the recipe's vacuity condition.
- **The surface sweep applies here too** (README §3, `PASSING`): a body you or
  an agent opened that meets a `FIX_POLICY` §4 tell is filed, diff-caused or not.

## 4 · Deliverables

- `C` entries for complete findings (README §3), each answering *"does it
  affect players who do NOT own the DLC?"* in its severity line.
- `TRIAGE.md` → **"For dlccheck"**: every seam you read, its verdict, and the
  rows you could NOT settle from the base side because the answer is inside
  `DLC/norman` (TAKEABLE WHEN the DLC chain reads that class). ⛔ This section
  is the contract with `DLC_DEEP_CHECK.md`'s chain: what it need not redo and
  what it must.
- `TRIAGE.md` → "03" coverage: rows read / not reached, with the reason.

## 5 · Scope fence

**In:** the `dlc-adjacent` set (Lua + presets), both paths, filing. **Out:**
any row not tagged (04 owns them; a seam you discover in an untagged row is a
one-line note to 04, with the tag added to the ledger and recorded as triage
drift for 99); reading `DLC/norman/**` beyond the single
function a base row calls into; ruling on the DLC chain's premise.

## 6 · Stop conditions

The `dlc-adjacent` set exceeds ~400 rows (split by registry:
`03b_SEAM_PRESETS.md`) · the `IsDlcAvailable` re-derivation differs
from 3/1 (record it, it is a finding about the brief, continue) · a finding's
falsifier needs a running game (route to the checklist as a rider; do not
guess).

## 7 · What may NOT be claimed

That the non-owner path is safe for a row whose DLC reference you did not
trace to nil-or-not. That a name match is a dependency. That the DLC "is
mostly additive" or is not. `tested`, ever.

## 8 · Close-out

Outbox to 04 (untagged seams found, by system, if 04 is still open), to 99
(every ruling with its route, the not-settled list, drift). Strike your row.
Explicit-path `git add`: `TRIAGE.md`, `bugs/C##.md` + `bugs/INDEX.md`, README, 04, 99;
`git rm` this file. doccheck GREEN, commit `-F`, push.

## Notes from upstream

*(authoring session, 2026-09-09)* Base-tree DLC references were counted in 12
files on 2026-09-08 including `Building.lua`, `ConstructionSite.lua`,
`FoodServiceBuilding.lua`, `Resources.lua`, `UpgradeUnlocks.lua`
(`DLC_DEEP_CHECK` §1.2 — INHERITED here, re-derive). `smr-bugfixpack-0f`'s
F117 lesson (README §2 (b′)) came from `ChooseDome` in `_GameUtils.lua`, a
dome-choice function the DLC work touched — the colonist/dome seam is where a
vanilla (b′) is most likely.
