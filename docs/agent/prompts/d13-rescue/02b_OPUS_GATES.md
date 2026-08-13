# Chain prompt 2b (INSERTED, owner GO 2026-08-13 — checklist item 19) — the three orphan gates, in-pack

**Read `README.md` first — binding chain rules apply.** This prompt exists by
the rule-6f escalation route: prompt 1 found three mod-owned GT thread bodies
with no §3a orphan gate, routed them (never dispositioned them to the
cleaner), and the owner said GO. Staleness check (all three repos; this prompt
was authored at fix-pack `ea81faa`+, opt-pack `a90d128`, TestKit `62f03da`),
todo list, game closed throughout — everything here is parse-tier.

**Scope fence: fix pack only, three one-line gate insertions + comment/header
disclosure. NO other behavior change, NO new persisted state, NO interval or
timing change, NO probe edits unless a probe provably reads a touched line.**

## Job 1 — the three gates

Copy `Fix_MeteorStormWedge`'s PROVEN §3a gate form (first-statement gate
`:145`, re-armed after the Sleep `:156` — Tier-1 built and verified). Do not
invent a new form; cite the precedent in each insertion's comment.

| site | insertion point (verify against live source first) |
|---|---|
| `Fix_CrystalMysteryHang.lua:44-54` | gate re-checked each wake: first statement after the `Sleep` at `:47` (`if not SMRFixPack then return end` — the body sets no vanilla state, so a bare return complies with §3a's reset clause vacuously) |
| `Fix_ExtenderFlapChurn.lua:77-84` | gate after the `Sleep` at `:78`, BEFORE the hub rebuild |
| `Fix_TrackConnectorPingPong.lua:156-160` | gate as the created closure's first statement |

Reading a nil global is safe; the gate is false only when the mod is gone.
On the installed path all three gates are always-true and the modules behave
byte-identically — that claim is checkable by eye and you state it, you do
not "verify" it.

## Job 2 — disclosure (the reason these were 6f-routed at all)

1. The three modules' headers: state the GT thread body, its gate, and its
   bounded orphan behavior in the save-footprint/§3a lines (they are currently
   UNDISCLOSED — prompt 1's finding).
2. `Fix_MeteorStormWedge.lua:138-141`: rewrite the stale inline comment that
   still carries the disproven by-name persistence model, aligning it with the
   module's own corrected header (`:53-66`). Adjudication §3.4 ordered this in
   Tier 1 and only the header was done.
3. `Fix_MeteorStormWedge` header `:65` ("the pack's one mod-owned GT thread in
   Tier-1 scope"): reword so it stops reading as a completeness claim the
   other three falsify (e.g. "the one GATED at Tier 1; the other three gained
   their gates 2026-08-13").
4. ⛔ Do NOT touch `agent/facts/EF-023.md` — its stale count AND its "nothing
   in `Code/` states it any more" line are prompt 3's Job 3. But say in your
   outbox that after your item-2 edit that claim is TRUE AGAIN as of your
   commit, so prompt 3 annotates rather than re-falsifies.

## Close

Parse sweep every touched Lua file; doccheck GREEN; `python
tools/doccheck.py --emit-counts` unchanged (74/75/88 — you added no module,
file, or probe). Append your outbox to `03_OPUS_BUILD.md` `## Notes from
upstream`: the exact inserted lines with final line numbers, the disclosure
edits, the EF-023 comment-state note, and anything owed. Update `STATE.md`'s
NEXT pointer to `03_OPUS_BUILD.md` (its 17-19 gate is SATISFIED — answers on
the checklist 2026-08-13). Commit (house style, `git commit -F`), push,
delete this file in the same commit.

## ⛔ What you may not claim

- Not "orphan behavior verified" — nothing launches here; the gates are
  measurable in prompt 4's junction-pull legs if that prompt finds it cheap
  (note it as an optional leg in your outbox).
- Not "baseline unchanged" as a measurement — you assert it structurally
  (no probe touched, counts re-emitted) and say exactly that.
