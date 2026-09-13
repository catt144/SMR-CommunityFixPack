# smrtk payload P2 — the per-object section in the infopanel

Payload P2 of link 03A (`smrtk`). README rules 1–22 are yours, **21 especially: you write, you never commit.**
Independent of P1/P3–P5.

## Job — `Code/73_SMRTK_Infopanel.lua`: a "Tool Kit" section where vanilla's Cheats section sits, untainted

1. **The injection technique is decided — inherit it.** 03A's spike (`reports/SMRTK_UI_HOOKS.md` §1, pasted into
   your inbox) names the route that (a) needs no Mod Editor, (b) does not set `config.BuildingInfopanelCheats`
   (rule 10), (c) does not wrap a vanilla function while idle (rule 9). Build on it, or on its declared fallback.
   Not a third route on your own — not because the spike is authority, but because five of you run in parallel and
   cannot negotiate; a better route you see goes in your SUGGESTIONS section and the coordinator may re-spike on it
   (README § "What is FIXED"). Re-read the cited lines before building (rule 12); if they do not say what the
   spike says, STOP and report — that is a DRIFT finding.
2. **Buttons, all via `SMRTK.Action` with `needs = "selected"`, all leaf calls** (`EF-095` bodies): Fill, Empty, Delete
   (label it "Delete (vanish)"), Destroy (label it "Destroy (blow up)"), Clean & Fix, Malfunction, Add Prefab, Add Dust,
   Add Maintenance, Spawn Worker / Visitor / Child / Colonist / Drone / Shuttle as the class supports (probe with
   `PropObjHasMember` exactly as `InvokeObjCheat` does), Upgrade 1–6, **Dump** (P4's object dump — call its registry id;
   stub "not built" if it is not registered at load), **Pin A/B/C** (P3's pins — same).
3. The section renders only when `SelectedObj` supports at least one action; the vanilla Cheats section is left
   exactly as it is (with the panel on, the owner should simply never need to open the Mod Manager).

## Scope fence

IN: `73_SMRTK_Infopanel.lua` + its `metadata.lua` line. OUT: any change to the vanilla section, any World action.

## Stop conditions

The spike's route does not hold on re-read · the infopanel rebuild path would need a wrapped vanilla function.
Report; the fallback is a "Selected" tab on the floating panel (say so in your for-07 section) — do not build the
fallback here.

## What may NOT be claimed

That the section appears in play (08). That Delete/Destroy semantics match play (08 reads one of each).

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. Parse-check your file; rule 6's and rule 7's greps, counts quoted. Return a
**numbered-claims report** to 03A: built · verified how (command + output) · stopped · OWNER-ROUTED · for-07 · DRIFT. Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox and `SMRTK_UI_HOOKS.md` §1 here before launch)
