# smrtk 99 — the terminal adversarial audit

Link 99 of `smrtk`. Fable, fresh context; your job is to **disbelieve the chain**. README rules 1–20 are yours.
Run only on a folder holding this file and `README.md` (or in the reduced form below).

## Full form

1. **Inbox audit:** every upstream close-out's outbox landed where it said (successor + here + README row) in one commit.
2. **Owed-work sweep:** every routed item has an owner and a TAKEABLE-WHEN; nothing lives only in a session's memory.
3. **The taint invariant, re-derived, never inherited:**
   - `grep -n "NetSyncEvent\|LogCheatUsed" <every SMRTK file + 80_AgentSlots.lua>` → 0, **with the presence side**
     (the same grep on `Data/CheatDef.lua` → 13+) so the negative is a sample;
   - every registered action's `run` read line by line against `EF-095`/`EF-098`: leaf call or not;
   - 02's and 08's `CheatsUsed` reads located in the **archived logs** by line, and the scratch-save control's RED;
   - `CanUnlockAchievement` reason at 08's end, in the log.
4. **The tag invariant:** from 08's archived log, every line the toolkit wrote carries `[SMRTK] SMRTK_`; count the
   toolkit's actions in the log against the panel's fire counters (a total is not a set — reconcile).
5. **The idle invariant (rule 9):** with nothing armed, enumerate every vanilla function the toolkit has replaced
   (`SourceOf`-style, as the TestKit's `[install]` probes do) → 0; then arm each toggle, count, disarm, count 0 again.
6. **Falsifiers RED:** the session-id guard refusing a foreign slot; a stamp skipping an unbuildable hex by name;
   auto-disarm after a load; `SMRTK_TAINT` firing when you call a sync wrapper on purpose in a scratch save
   (then delete that save and record it).
7. **Docs vs built:** every button in PLAYTEST_HELP exists; every file in the README's layout table is in
   `metadata.lua`'s `code` list and vice versa; `perma/SMRTK_SLOTS.md` has a row.
8. **Verdict:** SHIP / SHIP WITH CHANGES / NO SHIP in `reports/SMRTK_AUDIT.md` and, in plain language, to ck175.
   "Ship" here means *the owner uses it*; the TestKit never uploads (`H-04` still binds the wording).
9. **Kickoff lines:** the first real sitting the panel serves (fire `perma/SMRTK_SLOTS.md` against it — the owed
   ck144(a) boot is the natural candidate; say whether it is), and none else unless queued.
10. Consume this file and the README's queue (the README stays as the record, its table fully struck); delete the
    folder's row in `prompts/README.md` **in the same commit** (PROMPT MAP gate); SESSION_LOG entry; STATE's NEXT line;
    record the executed model (R-G); push.

## Reduced form — if 02 KILLED the chain

Post-mortem appended to `agent/reports/CHAIN_METHOD.md` §3 (a row: failure · instance · countermeasure); the
respec-or-abandon decision routed to ck175 with a recommendation (the likely respec: which premise fell — if P1,
the toolkit cannot exist as designed; if P2–P4, it can, minus that feature); every unconsumed prompt `git rm`'d with
its grave (`git show <sha>:<path>`) named in the README; the five facts `EF-095`–`EF-099` **amended, not deleted**,
with what the game showed.

## What may NOT be claimed

Anything you did not re-derive or re-read yourself. "Release ready" (`H-04`). That the no-taint property holds on a
build other than the one 02/08 ran on.

## Notes from upstream

- (authoring session `smr-bugfixpack-8f`, 2026-09-13) Two premises were flagged unverified at authoring: native
  `ConsolePrint` → `ConsoleLine` (`EF-096`), and retail `Platform.cheats` (`EF-095`). Check 02 measured both rather
  than inherited them. The facts were written in one session from source reads at build 24995074 — if the game
  updated between authoring and 02, the fingerprint says MOVED and 01 must have re-derived; check that it did.
