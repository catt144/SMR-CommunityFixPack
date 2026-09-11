# fixtoggles 06b — the data-undo four, then every linked button

Link 06b of `fixtoggles`. README binding rules 1–18 are yours. Runs after 04, 05 AND 06 (the link groups span their
modules). Staleness: `git log` + `git pull`.

## Part 1 — the data-undo modules

- **SilentHitMomentFX (C74, C77)** — wrappers gate normally; the anim-moment presets it registers (`:24-26`, `:286`)
  need an `on_deactivate` that removes exactly what it added and an idempotent re-add (the LoadGame tracker, `EF-087`).
- **DustSicknessBiorobots (F40)** — record the StoryBit filter objects it appends and remove exactly those on
  deactivate; reset the `DataPatch` runner's `patched` so re-enable re-runs (research `[I]` — verify in `00_Core.lua`).
- **SinkholeIndestructible (F96)** — write the class flag back on the same class (a class-field write works, `EF-058`).
- **CrystalMysteryHang (F06)** — `on_deactivate` stops the game-time repeater (`:72`); the ungated `MysteryEnd` handler
  (`:117`) gets the registry check `FIX_POLICY` §2 requires.

Each: shipped body read, disposition per spec §7, header, harness case for on/off/on and off→save→load→on, one commit.

## Part 2 — linked buttons

Implement spec §4 exactly: every TRUE dependency becomes a declared link the panel renders (the owner: *"we should make
sure thier button is linked"*); every non-dependency cluster is recorded as such with its proof, and NOT linked (a
spurious link takes a working fix away from a player). Harness: every declared link behaves as specced in both
directions; a player can never reach a state the spec calls invalid.

## Scope fence

IN: the four modules, link declarations (wherever the spec puts them), the harness. OUT: core semantics (route through
the README), the panel's rendering (07), text, version work.

## Stop conditions

An undo that cannot be made exact (it would remove something a player or another mod added) → route it.

## What may NOT be claimed

A link justified by a shared class alone. Anything in-game.

## Close-out

Green gates, `Mars.exe` closed. Outbox to 07 (the final link data), 08 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (links 01–06 append here)
