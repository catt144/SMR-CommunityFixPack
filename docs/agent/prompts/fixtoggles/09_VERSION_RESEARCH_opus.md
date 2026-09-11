# fixtoggles 09 — versioning and 1.0.7: RESEARCH ONLY, for the owner's B-step decision

Link 09 of `fixtoggles`. README binding rules 1–18 are yours. **Independent of every other link** — fire it any time.
⛔ **You build nothing.** No `Code/`, no `items.lua`, no `FIX_POLICY` §2a edit. The owner: *"I want to focus on the
buttons first, and then we can swing back around to the versioning as a B step if we proceed with that."*

## Questions to answer, each with evidence (MEASURED / SOURCE file:line / INFERRED)

1. **The version model.** The owner likes a game-version selector (fredware's panel has one). The research found his
   is **display-only** and runs his 1.0.7 fixes on 1.1.0 (`reports/FIXTOGGLES_RESEARCH_2026-09-11.md` §2). Lay out the
   options — (a) detect the running game (`LuaRevision`/`BuildVersion`, `EF-078`, `EF-085`) with the per-module probes
   kept as the hard guard and the dropdown as a view filter; (b) a player-picked target; (c) probes only, no selector —
   against `FIX_POLICY` §2a (decision 118, *"DO NOT BUILD A GAME-VERSION DETECTOR"*, and its two reasons) and checklist
   133(4). Say which of §2a's reasons each option meets or breaks, and what the 09-08 incident would have looked like
   under each.
2. **The 1.0.7 re-import inventory** (retiring the frozen `v5-game-1.0.7` download, `bec2e06`): the 36 modules hotfix 2
   deleted (`git diff --stat v5-game-1.0.7 HEAD -- Code`), the 1.0.7 bodies of the five 1.1.0-only modules
   (LandscapeUnitFilter, PayloadTemplateRefill, RocketDroneChurn, TrainCargoDumping, VacuumWalks), ShelterReflex half
   (a), DroneTransportMinors half (b), the sanitizer's old F03 pass. For each: can it get a behaviour probe that
   DECLINES on 1.1.0 (`FIX_POLICY` §2a form), or only a shape test, or nothing?
3. **Conflicts:** F95's residue pass vs v5's AstrogeologistExtractors (they fight directly); any other pair.
4. **Testing cost:** Steam serves ONE branch at a time (owner 09-08); the 1.0.7 fixture library loads only on 1.0.7
   (`EF-079`); what attended sittings a B chain would need, priced honestly.
5. **Player surfaces:** the site's legacy page, the card's "STILL PLAYING ON 1.0.7?" section, what changes for a 1.0.7
   player and when.
6. **The recommended B-chain shape and size**, and what the buttons chain must leave in place so B needs no rework
   (a reserved registry field, the panel's header slot).

## Deliverable

`docs/agent/reports/FIXTOGGLES_VERSION_RESEARCH.md` + a plain-language decision for the owner appended to checklist 148
(or the next free number at that moment): proceed with B or not, which version model, with a recommendation.

## Scope fence

IN: reading both trees, the repo history, the reference mod, the report, the checklist append. OUT: everything else.

## Stop conditions

A question needs a game run to answer → say what run would settle it; do not guess.

## What may NOT be claimed

That any version route is safe (no game has run). That a deleted module "is still needed on 1.0.7" without its entry and
the 1.0.7 body read.

## Close-out

Commit the report + checklist append; outbox to 99 (and to the owner's B kickoff via 99); strike your row; `git rm` this
file; push.

## Notes from upstream

- From the authoring session: the module feasibility research (§3) marks the five 1.1.0-only bodies and the halves
  hotfix 2 removed. 06 may append 1.0.7-only considerations for SaintBlessing here.
