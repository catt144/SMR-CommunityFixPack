# Chain 9 — D10: the workshops module build (+ the bundled F84 text decision)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gate: the D10/D12
unhold must be recorded (prompt 5). Authority: **the BUGS.md D10 entry is the
spec** — speced 2026-07-30, user-approved; do not re-design it.

## Jobs (todo list first)

1. **The bundled F84 decision — ask BEFORE building T1.** D10's T1 text
   repairs and F84's Universal-Tunnel description fix share the identical
   localization tradeoff (a localized `T` becomes an English-only
   `Untranslated` string) and the standing rule says they must not be
   answered twice differently (STATUS/F84 entry). Present both together:
   one owner answer covers T1's shape AND whether F84 ships with it.
2. **Build per the D10 entry**: T1 text repairs + T2 capacity dial
   (base/+50%/+100%, `max_workers` AND `consumption_amount` PAIRED), as an
   `Opt_` module per the entry's shape.
3. **Add PT-57** (~7 min, per the entry) to the checklist at build time —
   the owner runs it during the playtest campaign; this chain does NOT run
   attended tests.
4. **Probe + the module's own A/B leg** (stale-probe gate; predictions
   first). D10 touches colonist assignment — the reason it was held —
   so the leg's zero-FAIL bar is absolute.
5. STATUS/BUGS records; F84 entry updated with the decision either way.

## Scope fence

**In:** D10 exactly per its entry, the F84 co-decision, PT-57's checklist
row, the leg. **Out:** D12 (NEVER in the same session — the two both touch
colonist assignment and the standing rule says land them separately, each
with its own A/B); any workshop behavior beyond the entry's spec.

## Stop conditions

- The owner's F84/T1 answer changes T1's shape materially → re-check the
  entry's spec still holds before building; if it doesn't, stop and ask.
- Leg fails prediction → stop, report.

## What may not be claimed

`fixed` only after the leg; `tested` only after PT-57 PASSES (that flip
belongs to the playtest campaign, not this session — say so in the entry).

## On completion

Outbox → `10_d12_no_homeless_build_opus.md`. Delete this file, commit, push.

## Notes from upstream

(prompt 8 appends state + counts here)

### Routed here from chain prompt 6 (2026-08-01) — one claim to CHECK before you build

A Reddit thread read this day (`BUG_LIST_AUDIT.md` **§10.5**, source **[S36]**)
contains a player asserting that the devs *"squashed two of the most pressing
bugs with the 1.0, **homelessness and unemployment**"* — the exact subjects of
**D10 (workshops / unemployment)** and D12.

**Treat this as a prompt to verify, NOT as a reason to descope.** It is
third-hand, vague about which 1.0.x, and comes from a satisfied player, not a
patch note. ⛔ The thread is **hotfix-1.0.3-era, four generations before our
pinned 1.0.7.396349**, so it says nothing about the build we ship against
either way.

**What it costs you is one Src read**, and this project's own rule says who
wins if they disagree: *"fixed in Relaunched" only from current Src, never from
patch-note or forum text alone.* If unemployment's cost really did become
visible in a 1.0.x pass, D10's premise changes and you want to know that before
building, not after. If it did not, you have spent five minutes and closed a
loose claim that would otherwise have surfaced during QA.
