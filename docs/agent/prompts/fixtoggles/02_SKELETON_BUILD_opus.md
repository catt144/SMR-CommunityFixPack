# fixtoggles 02 — the walking skeleton (build)

Link 02 of `fixtoggles`. README binding rules 1–18 are yours. Staleness: `git log --oneline -10` + `git pull`; the spec
(`reports/FIXTOGGLES_SPEC.md`) is your design authority, and its §0 may have re-cut this prompt — act on the spec.

## Job — the smallest end-to-end proof, built desk-side, with predictions written down first

1. **Predictions first.** Before any code, write `reports/FIXTOGGLES_SKELETON_PREDICTIONS.md`: for every step 03 will run,
   the exact log lines / reads you expect and a **3× abort threshold** for time or retries (`CHAIN_METHOD` §5 D). 03 is a
   kill gate; the predictions are what it scores against.
2. **Core** (`Code/00_Core.lua`) per spec §2: registry fields, the ONE store with deviation-only schema, the reconciler
   for every module, the gate helper, the "not yet switchable" refusal for unconverted modules, the switch log lines.
   Keep every existing behaviour for unconverted modules byte-for-byte (they must still apply exactly as today).
3. **Exactly ONE module converted end to end** — the one the spec picks (a wrapper with a player-visible effect is the
   ideal first subject). Its header states the real switch semantics both directions.
4. **The surface stub** per spec §6 and ck148(a) as ruled at that moment (if unruled: build the spec's recommended
   route and say so in 03's inbox): it must list every registered module (unconverted ones visibly not switchable),
   switch the converted one, persist, and be reachable by mouse AND gamepad by construction (spec §1e). Own look is
   07's job; the stub may be plain.
5. **`items.lua` / `metadata.lua`** only as the chosen route requires (option items + `default_options` for the Mod
   Options route — `name` == Register id == `default_options` key; H-10). ⛔ Never `version` (H-02).
6. **Desk harness** `tools/desk_toggles.py`, registered in `tools/deskbench.py`: cold boot AND enable-path reload,
   gate on/off on the converted module, persistence round trip, deviation-only storage (change a default, an untouched
   player follows it; a touched player keeps theirs), unconverted modules unaffected. **Every assertion gets a
   falsifier seen RED** before you trust its GREEN (load the real core under its real file name + line offset;
   memory `desk-harness-engine-shims` has the shims).
7. **Write 03's script** into `03_SKELETON_SITTING_owner.md`'s inbox: fenced copy-paste console lines (one command per
   line), where each runs (menu vs colony), the echo contract (the LOG, not the screen), the first-screen witness per
   step, and the fixture 03 needs (a 1.1.0 colony; `EF-079` — the 1.0.7 fixture library cannot load).

## Scope fence

IN: `Code/00_Core.lua`, the ONE module, the surface stub, `items.lua`/`metadata.lua` as required, `tools/desk_toggles.py`
+ `deskbench.py`, the predictions doc, 03's inbox. OUT: every other module (04–06b), the finished panel (07), player
text (08), version work (rule 10).

## Stop conditions

The core change would alter an unconverted module's behaviour · a blacklisted name is needed · the harness cannot
express the enable path · the surface route the spec chose fails on the desk. Report; don't force.

## What may NOT be claimed

That anything works in the game (03 decides). That the gamepad path works (only 03's hands can say). A GREEN whose
falsifier you did not see RED.

## Close-out

Green gates (rule 14), `Mars.exe` closed (rule 15). Commit per unit (core · module · surface · harness · predictions);
outbox to 03 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (link 01 appends here)
