# Chain B — `smrcf-text` · the simple combined chain

> ⛔⛔ **2026-08-20 — DO NOT RUN THIS CHAIN. `C50` AND `C51` ARE ALREADY BUILT
> AND SHIP IN 1.0.0.** The owner reversed the post-launch premise (checklist 58)
> and `closeout-1.0.0/` links 1–2 built both on 08-20 —
> `Code/Fix_LocalizedUIText.lua` and `Code/Fix_SpaceYDroneCapBullet.lua`, both
> registered in `items.lua` + `metadata.lua`, `upload_preflight` 0 FAIL. Running
> this chain's `01_BUILD_opus.md` would rebuild shipped modules. ⚠️ **Two of its
> readings were also overturned by that build and are wrong here:** `C50` has
> **three** live render sites, not two (`agent/bugs/C50.md`), and the replacement
> ids were re-verified across **all nine** packs, not just German
> (`agent/bugs/C51.md`). ⭐ **What is NOT consumed: the dust-devil marker gate**
> this chain carried as a rider — it is still owed and still gated on chain A.
> ⛔ The module counts below are era-stale (they read 76; the tree is at 77).

`C50` + `C51`, plus the dust-devil marker gate **if and only if chain A clears
it**. Map: `agent/prompts/SMRCF_CHAIN_SET.md`. ⛔ **Gated on chain A.**

## Manifest

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_BUILD_opus.md` | volume tier | no | re-derives all three routes, builds what survives |
| 02 | `02_SITTING_owner.md` | volume tier | **YES — ~15 min** | the language check + the `C35` ride-along |
| 03 | `03_AUDIT_fable.md` | top tier | no | adversarial backward QA; empties the folder |

## Why these three are one chain

They are the **simple** items in the set — each is a small, bounded patch — and
two of the three are the same subsystem (shipped localization). The owner's rule:
*"if the others are simple they can be combined chains."*

They also share **one attended check**, which is the real economy: switching the
game to a non-English language and looking at two panels covers `C51`, and the
sponsor screen covers `C50`, in the same sitting.

## The three items

**`C51` — three UI strings that can never be translated.** The terraforming
heading is a raw Lua literal with no id (`TerraformingOverall.generated.lua:56`)
while `T(914616772802, …)` ships translated — **verified in `Local\German.fpk` as
`TERRAFORMING-GESAMTFORTSCHRITT`**. The *Back to Earth* button uses two ids no
pack contains while `407456913268` / `316233855405` do.
⭐ **The repair shape is loss-free**: pointing a UI at an enrolled id yields the
shipped translation in every language, with no English literal in the path
(`EF-039` route mechanics, `EF-063` for how to verify enrolment in 30 seconds).
⚠️ The rocket button is the easy half (`Id = "idBackToEarth"`, resolve-and-set).
**The heading is the hard half — that `XText` has no `Id`, and neither does its
parent window.**

**`C50` — SpaceY's `+20 CommandCenterMaxDrones` has no description bullet.**
Whole-tree control: 16 sponsor presets, 6 carry modifiers, **5 of 6 describe
every one of theirs**. ⛔⛔ **The obvious remedy is a trap**: replacing the
shipped `T(880574954148, …)` with a new literal renders English for all eight
non-English languages (`EF-039`). The only loss-free shape is
`shipped_T .. Untranslated("…")` — which can **append** a bullet and cannot edit
the existing one. **Whether one appended English line beats nothing is a
judgement call and it is the owner's**, not this chain's.

**Dust-devil marker gate — CONDITIONAL.** The marker thread checks
`HasDustStorm` and omits `DustStormsDisabled`; the natural scheduler checks both,
twice, in the same file. ⛔ **Build only if chain A found real
`PrefabFeatureMarker`s with `FeatureType == "Dust Devils"`.** If A found none,
this is `C49` again — file it LATENT and build nothing.

## ⛔ First-of-kind warning, and it is the biggest risk in this chain

**This pack has never patched an XDef-generated UI class.** Zero `ResolveId`,
zero `XTemplate` work, zero UI-window wrapping across all 76 modules. `C51` would
be the first. Budget for that being harder than it looks, and note that
`FIX_POLICY` §348-351 puts UI and affordance behaviour in the one class where
*source reading gives confident answers with no validity* — expect to need eyes
during development, not just after.

## Binding chain rules

As `smrcf-verify/README.md` §"Binding chain rules" (staleness check ·
inbox/outbox · route-don't-drop · self-split · file your instruments' defects ·
`WORKFLOW` 1–7 · predictions before runs · archive logs with `git add -f`), plus:

10. **Every module obeys `FIX_POLICY` §3a** — save-safety pass, self-check in
    `apply()`, restore-on-disable, no saved object or marker.
11. **One fix per module** unless the owner rules otherwise; the combined chain
    is about sharing a *sitting*, not about merging modules.
12. ⛔ **`EF-039` binds every string this chain writes.** Re-read it before
    typing a `T(`. Its "control is queued" caveat was **stale and is struck** —
    the control ran 2026-08-02 and printed `userdata`.

## Stop conditions

- Chain A found zero dust-devil markers → drop that item, build the other two.
- `C51`'s heading half needs a fragile match-by-text walk and no stable handle
  exists → **ship the rocket half alone and route the heading** to the owner with
  the reason. Half a loss-free fix beats a brittle whole one.
- `C50`'s append-only shape looks worse than leaving it → **that is a real
  finding**, route it, build nothing.
