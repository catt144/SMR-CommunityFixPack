# B·01 — re-derive, then build what survives · UNATTENDED

**Read `README.md` first — the first-of-kind warning and `EF-039` bind you.**
Then `STATE.md`, then `FIX_POLICY.md`, then this.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ **Gated on chain A** — the dust-devil item needs A's marker census. If
`smrcf-verify/` is unconsumed, either wait or build the two unconditional items
and leave the third to a self-split continuation.

## 1 · 🗒 Live todo list from your first action — one item per fix.

## 2 · Job 1 — re-derive all three routes BEFORE writing a line

`CHAIN_METHOD` §2.3, the rule this project paid for twice: **"do not re-derive
the design" never means "do not verify the route."** Every route failure this
week sat above individually-correct citations.

Re-derive at `ModTools\Src`, by symbol:
- `C51`: the raw literal at `TerraformingOverall.generated.lua`; the two XDef ids
  in `customUniversalRocket.generated.lua`; the enrolled ids in
  `LocalizationTexts.lua`. **And re-check enrolment against a shipped language
  pack** — `EF-063` gives the 30-second route with our own `tools/flpk_extract.py`.
- `C50`: the two `Effect_ModifyLabel` entries and the `effect` string in
  `Data/MissionSponsorPreset.lua`; that `DroneHubBase:GetMaxDrones` is still the
  only behavioural reader of `g_Consts.CommandCenterMaxDrones`.
- Marker gate: `DustDevils.lua` — the marker thread's gate, the natural
  scheduler's two, and the post-warning re-check that is missing.

⛔ **If a route has moved, the entry is authoritative and this brief is not.**
Update the entry, then decide.

## 3 · Job 2 — build

**Order: easiest and safest first**, so a truncated session still ships
something. Suggested: `C51` rocket half → marker gate (if cleared) → `C51`
heading half → `C50`.

Per module, non-negotiable (`FIX_POLICY` §3a): a self-check in `apply()` that
returns a **reason string and never errors**; restore-on-disable that does not
overwrite a later third-party wrapper; no saved object, timer or marker; a
TestKit probe; and the parse sweep before any commit that touches Lua.

**Shape guidance, not design authority** — you re-derive and may overrule with a
written reason:
- `C51` rocket half: post-`Init` on `customUniversalRocket`, `ResolveId(
  "idBackToEarth")`, set the two rollover fields from the **enrolled** ids.
- `C51` heading half: the `XText` has no `Id` and neither does its parent. If you
  cannot find a stable handle, **do not invent a brittle text match** — stop and
  route it (README stop condition).
- Marker gate: a Layer-3 patch on the gate, keeping vanilla's body. ⛔ **Do not
  own the marker-thread body.** Our own `Fix_DustDevilSpawnGate` header records
  why we declined exactly that for the natural scheduler, and the reasoning
  transfers.
- `C50`: `shipped_T .. Untranslated("…")` only. ⛔ **Never replace the shipped
  string.**

## 4 · Job 3 — write the sitting

Fill in `02_SITTING_owner.md` with the real steps: which language to switch to,
which two panels, what "correct" looks like, and the `C35` ride-along (chain A
armed its detector; the trigger is a lander with drones on the ramp + Edit
Payload → confirm). **Order it so a truncated sitting banks the decider first.**

## 5 · Scope fence
**IN:** the three items, their probes, the sitting script.
**OUT:** ⛔ `C52` (chain C) · ⛔ `C25` (chain D) · ⛔ `C49` — R4, does not ship ·
⛔ the three raw literals with **no** loc record (*COLONY DATA*, *Mod options are
not yet available.*, *No DLCs available.*) — they need a `ModItemLocTable` per
language and that is a separate, later decision.

## 6 · Stop conditions
- A route has moved → stop, update the entry, re-decide.
- The heading half needs a brittle match → ship the rocket half, route the rest.
- `C50`'s append shape reads worse than silence → **build nothing, route it.**
- Suite or gate reads wrong → STOP; do not bank readings about code that did not
  run.

## 7 · ⛔ What may not be claimed
- ⛔ **`tested-unattended` for any of this.** All three are screen events; that
  word is closed to screen events by the 2026-08-15 ruling. `fixed` is the
  ceiling until 02 runs.
- ⛔ **"Translations now appear."** You can prove the UI asks for the right id.
  Only a non-English screenshot proves what a player sees.
- ⛔ **"The marker gate is fixed"** without A's census behind it — without
  markers it is LATENT and a fix for it ships nothing.
- ⛔ A blanket verification claim over a table. Provenance per row; ROUTE tagged
  separately from citations.

## 8 · Close-out
One commit: modules + probes + entries updated (`C50`, `C51`, and the marker
entry if it exists) · `02_SITTING_owner.md` filled in · the sitting on the
**checklist** (R10 — an ask in an agent doc is not asked) · counts re-emitted by
`doccheck --emit-counts`, never hand-typed · manifest row struck · `git rm` this
file · doccheck GREEN · grave named · push.

## Notes from upstream
