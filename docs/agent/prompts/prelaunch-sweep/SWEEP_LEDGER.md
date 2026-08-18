# Sweep ledger — COVERAGE ONLY

⛔⛔ **VERDICTS DO NOT GO IN THIS FILE.** Findings go in `SWEEP_FINDINGS.md`,
which the next link ⛔ **may not read**. This file is what the next link ⛔
**must** read, and it is the only reason the chain can converge instead of
looping: five blind sweeps can each cover the comfortable 60% and never touch the
awkward 40%.

**Write your row BEFORE you start work** (claims the lens) and complete it at
close-out.

⭐ **The `NOT reached` column is the most valuable column in the chain.** It is
what the stopping rule reads, and it is what the terminal audit reports to the
owner as the honest product of the whole effort. An empty `NOT reached` cell is
almost always a lie — say what you could not see.

---

## Lenses (`00_CHAIN_SPEC.md` §3) — take the first one not yet claimed

`L1` structure & collision · `L2` lifecycle & idempotency · `L3` save & exit ·
`L4` player experience · `L5` failure & containment · `L6` promise vs behaviour ·
`L7` environment & namespace · `L8` adversarial / hostile modder

---

| link | lens | scope actually covered | depth | ⭐ NOT reached | config | commit |
|---|---|---|---|---|---|---|
| *(seed — not a link)* | — | `metadata.lua` upload guards; the shipped `.fpk` file list; `00_Core.lua` status/`order`/`update_suspect` paths | mechanical: preflight tool (20 guards) + real archive listing + every `status`/`update_suspect`/`order` site enumerated | ⛔ **everything else.** No module was read. Nothing was run in a game. No collision map. No save-footprint measurement. No packed-install test. No player-experience pass. | dev tree, unpacked, all three mods | `2f077e8`, `2e47e3a` |
| **1** | **L1 — structure & collision** | All 76 `Code/*.lua` for patch sites, **alias-resolved**: 197 rows / 134 symbols / **50 class-method targets** / 16 global replacements / 21 `OnMsg` registrations. All five exposure shapes of `02_LENS_NOTES.md` L1: class method · table slot · global assignment · preset field · own thread. Cross-checked against `ModTools\Src` (4,446 files, 3,708 `DefineClass`): **C1** every subclass in Src declaring a method we patch on a parent (8 hits, each adjudicated by reading the override); **C2** every method patched twice on one class/chain; **C3** shared class surfaces (16 pairs). `AutoResolveMethods` enumerated in full (58). | **mechanical for code symbols** — extractor-emitted, every row cites file:line, artifact `reports/L1_COLLISION_MAP.md`. **Medium for preset fields** — enumerated by reading the 13 preset-touching modules, ⛔ NOT extractor-backed. Engine routes (`OnMsg` additivity, `classes.lua:608` declare-wins, `Done` not auto-resolved) **re-derived at Src**, not inherited. | ⛔ **Nothing was run in a game** — every verdict is source-derived, and neither 2026-08-17 core fix has yet executed. ⛔ **`OnMsg` state interference**: additivity proven, but whether the 11 `LoadGame` / 7 `PostLoadGame` handlers read+write overlapping state is UNCHECKED. ⛔ **Preset-field map is not mechanical** — a write behind an indirection I did not read would not appear. ⛔ **Second-apply / `ReloadLua` behaviour** (L2). ⛔ **Aggregate save footprint, `90_SaveSanitizer` coverage, uninstall of all 75 at once** (L3). ⛔ **Anything a player sees or reads** (L4). ⛔ **Runtime failure containment in aggregate** (L5). ⛔ **Registry↔package↔card agreement, dead-coded targets, the veto route over all 75** (L6). ⛔ **Globals we leak, packed-vs-unpacked, what the TestKit's `_G` mutation hides** (L7). ⛔ **Any foreign mod** (L8). ⛔ **TestKit tree not included** (`Code/` only). ⛔ **Runtime cost of 75 modules together** — never measured by anything. ⛔ **Whether L1-F1's two preconditions can co-occur on one colonist** — needs a running game. | dev tree, unpacked, source-derived; no launch | *(this commit)* |

---

## Seed notes for link 1

The row above is **not a sweep** — it is the pre-chain work of 2026-08-17,
recorded here so the first link knows the small amount that is genuinely covered
and does not re-do it.

**Settled by measurement, do not re-derive unless you doubt it:**
- the shipped package is **80 files**, `docs/`/`tools/`/`CLAUDE.md`/`README.md`/
  `.git`/`.claude` all **zero** — read out of the real `.fpk`;
- `*` **does** cross `/` in `MatchWildcard`, which is what settles the
  `*/docs/*` question `WORKFLOW` §882-887 had owed since 08-13;
- `tools/upload_preflight.py` passes 20 guards, and was falsifier-tested by
  deleting the `image` field (it caught it, exit 1).

**Explicitly NOT settled, and first in line:**
- ⛔ neither 2026-08-17 core fix has been run in a game;
- ⛔ the mod has **never** been loaded packed — only unpacked via the junction;
- ⛔ every gate reading this project owns was taken with the TestKit loaded, and
  the TestKit **mutates `_G`**;
- ⛔ no aggregate anything: save footprint, runtime cost, collision map.
