# smrtk 03b — the per-object section in the infopanel

Link 03b of `smrtk`. README rules 1–20 are yours. After 02 PASS; independent of 03/04/05/06.

## Job — `Code/73_SMRTK_Infopanel.lua`: a "Tool Kit" section where vanilla's Cheats section sits, untainted

1. **The injection technique is the risk — solve it first, on the desk.** Read how `sectionCheats`
   (`Data/XDef/sectionCheats.lua`, `Lua/XDef/sectionCheats.generated.lua`) is composed into the infopanel and how
   `InfopanelObj` builds sections (`Lua/X/Infopanel.lua`). Choose the least invasive route that (a) needs no Mod Editor,
   (b) does not set `config.BuildingInfopanelCheats` (rule 10), (c) does not wrap a vanilla function while idle (rule 9
   — a section spawned from a message or a template-list append is fine; a replaced `Open` is not). Write the chosen
   route and the two rejected ones into 99's inbox with the line numbers.
2. **Buttons, all via `SMRTK.Action` with `needs = "selected"`, all leaf calls** (`EF-095` bodies): Fill, Empty, Delete
   (label it "Delete (vanish)"), Destroy (label it "Destroy (blow up)"), Clean & Fix, Malfunction, Add Prefab, Add Dust,
   Add Maintenance, Spawn Worker / Visitor / Child / Colonist / Drone / Shuttle as the class supports (probe with
   `PropObjHasMember` exactly as `InvokeObjCheat` does), Upgrade 1–6, **Dump** (05's object dump — call its registry id;
   stub "not built" until 05 lands), **Pin A/B/C** (04's pins — same).
3. The section renders only when `SelectedObj` supports at least one action; the vanilla Cheats section is left
   exactly as it is (with the panel on, the owner should simply never need to open the Mod Manager).

## Scope fence

IN: `73_SMRTK_Infopanel.lua` + its `metadata.lua` line. OUT: any change to the vanilla section, any World action.

## Stop conditions

No injection route satisfies (a)–(c) · the infopanel rebuild path would need a wrapped vanilla function. Report;
the fallback is a "Selected" tab on the floating panel (say so in 07's inbox) — do not build the fallback here.

## What may NOT be claimed

That the section appears in play (08). That Delete/Destroy semantics match play (08 reads one of each).

## Close-out

Rules 15–16. Commit per unit (injection · buttons). Outbox to 07 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (02 appends here)
