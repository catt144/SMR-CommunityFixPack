# Chain prompt 2 — the sitting (owner attended, ~40–60 min)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list the owner can read to know when to step in. The owner drives the mouse
and types every console line (the rig has no input path into a running game);
you hand lines ONE AT A TIME, pre-flighted, and keep the sent/checked/
outstanding ledger. An owner override is a course change — state the plan's
position once, then follow (WORKFLOW).

**⛔ PT-00 first** (stale-probe sweep, CLEAN or declared), then arm via
`CP60_ARM.ps1` (the ARM GATE refuses an unarmed launch), then launch.

## The leg, in priority order (decider first; a truncated sitting still banks ①–③)

**⓪ Gate + fixture.** `CP60.Load("CP60STAGE.savegame.sav")` → the run-top pack
gate (**STOPS if the pack is not loaded** — any re-enable is handed back to
the owner explicitly). Fixture confirm by READS: map, sol (~302 lineage),
`81/81` module count, CLOCK line. Re-arm any wanted loggers (restart cleared
them). ⚠️ The first load has ALREADY landed the P8 first-load heal lines in
the log buffer at zero owner cost — note the time window; the authoritative
absence/presence read is from the ARCHIVED log after exit (EF-047).

**① P1–P3.** `CP60.Fixes()` — registered/active counts, the five new modules
and seven converted modules' statuses, Note-relayed against prep's annotated
predictions. Read the detail string of anything not `active` before
concluding.

**② P4–P5.** `*r`-prefixed `CP60.Suite()` — the runnable new probes' verdicts
plus the no-regression check on the two at-risk probes prep named. Quote the
header line and per-probe verdicts; do not chase a total (the archive's own
rule).

**③ P8/P9 round trip.** `CP60.SaveNamed("CP60RT")` → `CP60.Load
("CP60RT.savegame.sav")` → P9 read (`CP60.P9()` — the key must be absent after
one load-and-save) → P8 idempotence expectation: none of the three save-state
heal lines repeats on this second load (mid-session = provisional presence
read; the audit settles absence from the archived file). R4 satisfied by
construction — this IS the round trip.

**④ The owner plays, 15–20 minutes, ORGANIC.** Mixed speeds, at least one
of their own saves if they feel like it. Watching for P6 (zero `[LUA ERROR]`
naming the five new files or seven converted modules) and P7 (no visible
behaviour change from the conversions — night shifts, gene forging,
shuttle-hub availability, landscaping sites, upgrade modifiers, sequence
latents, rocket refuelling all feel vanilla). ⚠️ Rule 13: F92/F95 legitimately
move morale/production on this save — do not let anyone read those as drift,
and say so out loud if the owner remarks on either.
**Riders — ONLY if the gate reads their precondition true, never forced:**
F21 (a working train line → the two reads from the entry), F34(d) (owner
stages a landscape mark over a loading rocket — hands + eyes), C42 (passages
demonstrably trafficked → the within-session read BEFORE any further
save/load), F90 (a surface storm arrives on an elevator colony → the
notification watch). Each rider names FORCED vs ORGANIC per reading.

**⑤ Owner verdicts.** At every measure moment, put the question, and relay
the owner's words through `CP60.Note` **the moment they are spoken**
(corun-pt15 rule 3 — a `tested` grant needs the verbatim IN the log). Expected
verdict moments: the suite outcome vs predictions; the play window's "nothing
felt different" (P7 — that sentence, theirs, is the reading); any rider taken.

**⑥ Close-out.** Quit to desktop (flushes the log). Archive the log
(`cmp`-verify + MD5, `git add -f`). Whole-log first pass: 0 `[LUA ERROR]` /
F99 `:805` / C45 `invalid pos`; every unexplained line VERBATIM with its age;
cheat markers counted + owner's reason verbatim if any were used. Save-dir
listing **BY NAME** against expected survivors; delete `CP60STAGE` +
`CP60RT` in the recording commit and record **"deleted, listing verified" —
NEVER "gone" (rule 12: Steam Cloud is ON; they may return at the next launch
and that is EF-051's mechanism, not a failure)**. Byte-verify the FOUR
protected files (`PT-15`, `TEST2H TRAIN`, `PT35FIXTURE`, `USA Sol 302`).
Update entries incrementally (per-prediction readings; F90/F91/F94/F96 +
conversion evidence moves only to what was read; status flips front-matter
AND heading tag, regenerate index). Owner-time honesty: promised vs actual,
deviations separated. doccheck GREEN, commit (`PROBE SWEEP:` line), push.
Append `## Notes from upstream` to `03_FABLE_AUDIT.md` — run conditions as
read, per-prediction verdict table with log line numbers, owner verbatims
(flag any that exist only in the transcript), misses, riders taken/skipped
with the gate reads that decided them. Delete this file in the same commit.

## Stop conditions

- Pack gate fails → STOP the run; hand the re-enable back; bank nothing.
- Fixture confirm fails on the staged copy → try the `USA Sol 298` fallback
  (stage it live, MD5 first); both failing → bank the gate reads, route.
- Any `[LUA ERROR]` naming pack/TestKit code → stop that leg, record
  verbatim, continue independent legs.
- The owner has to leave → ①–③ are the bank; inventory ④'s remainder as
  TAKEABLE riders and close honestly.

## ⛔ What you may not claim

- No `tested` grant without the owner's verbatim verdict relayed through
  `CP60.Note` on that reading — and name what was forced anyway.
- P6/P7 hold only for the paths this sitting executed — say "this session's
  paths", never "the conversions are verified" unqualified.
- Absence claims (no heal repeat, no error) are PROVISIONAL until the audit
  reads the archived file (EF-047).
- Nothing about F90/F93/F96 live halves from quiet weather.
- No "gone" for any deleted save while Steam Cloud is ON.
