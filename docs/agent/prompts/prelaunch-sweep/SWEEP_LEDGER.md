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
