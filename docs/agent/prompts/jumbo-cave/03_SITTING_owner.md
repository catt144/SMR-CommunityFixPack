# D·03 — the attended sitting · ⚠️ THE OWNER IS AT THE KEYBOARD

**This is the only prompt in the chain that costs the owner anything.**
Read `README.md` first, then `STATE.md`, then this, then
`## Notes from upstream` — 02 fills in the save name and the real steps there.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ **Do not start if 02 has not filled in §2.** An un-staged sitting wastes the
one resource this whole set is trying to protect.

## 1 · 🗒 Live todo list from your first action — and keep the ledger

`WORKFLOW` co-run rules (owner rule 2026-08-05): **the session keeps the
sent/checked/outstanding ledger so the owner does not have to.** State the plan's
position once when the owner deviates, then stop — no per-message
back-on-track reminders.

## 2 · The sitting — a PRIORITY QUEUE, not a schedule

*(02 fills this in. The ordering rule: put the decider first, so a truncated
sitting still banks it.)*

**Save:** *(02 writes the exact name here)*
**Owner cost:** one playthrough segment — *(02 estimates, honestly, and budgets
console-driving explicitly: the rig has no input path into a running game, so
every console line is the owner's hands)*

**The decider, first:** the owner builds the Jumbo Cave Reinforcements and lets
drones work the Waste Rock. Everything else is optional.

## 3 · What is being watched

The `DroneApproach` detector, armed by chain A and proven live by 02. It fires
when a drone fails to reach a rock, and captures **what occupies the
neighbouring hexes at that moment** — terrain or other rocks. That capture is
the ⚖️ discriminator and it cannot be reconstructed afterwards.

**Three outcomes, all useful** (README has the table): stranded by terrain ⇒
trigger demonstrated; stranded by rock crowding ⇒ consequence proven, trigger
still open; nothing strands ⇒ evidence the geometry does not do this.

## 4 · Rules for the sitting

1. ⭐⭐ **Relay every owner verbatim through the log-note primitive the moment it
   is spoken** (`WORKFLOW` co-runs, corun-pt15 rule 3). A quote that lives only
   in the session transcript **cannot be re-read by the audit, ever**. This has
   already cost this project the provenance of a status grant.
2. **The owner may reorder the queue live, and that is a feature.** Witness
   discipline applies to whatever runs, planned or not. Owner-directed deviation
   is never scored against the estimate — only they may rule their own time out
   of scope.
3. **Judge by the LOG, not the screen** — flush first. A silent console at the
   main menu executes without echoing (corun-pt60).
4. **Re-confirm the fixture at sitting time.** It has evaporated between prep and
   sitting before.
5. If the wedge happens: **do not fix it, do not demolish anything.** A
   demolition bumps the unreachables version (`Building.lua:523`) and destroys
   the state you just caught. Capture, then stop.

## 5 · Scope fence
**IN:** the sitting, the readings, the owner's verbatims, the log.
**OUT:** ⛔ any fix code · ⛔ any status promotion (that is 04's to weigh) · ⛔
adjudicating the discriminator mid-sitting — capture it and let the audit rule.

## 6 · Stop conditions
- The staged save does not load, or the tech/site is not actually available →
  **stop, do not burn owner time improvising.** Hand back to 02's successor.
- The detector produces nothing in a reasonable window → that is a **result**,
  not a failure. Record the exposure (how long, how many rocks, how many
  approaches) so the null has a denominator.
- The owner wants to stop → stop. Bank what ran.

## 7 · ⛔ What may not be claimed
- ⛔ **`tested-attended`** for `C25`. Nothing here tests a fix; there is no fix.
  The strongest available word is *reproduced* or *not reproduced*, with the
  discriminator's verdict deferred to 04.
- ⛔ **"The trigger is real"** from a stranding whose neighbours were rocks.
  That is the confound the discriminator exists to catch — do not launder it.
- ⛔ **A frequency claim.** One colony at elevated density is not a rate.
- ⛔ Any claim the owner did not actually see, attributed as though they did.

## 8 · Close-out
One commit: readings recorded on `C25` with provenance per row · **every owner
verbatim in the archived log, not just the transcript** · log archived
`git add -f` · outbox to `04_AUDIT` including the exposure denominator · the
checklist line struck now the sitting has run · manifest row struck · `git rm`
this file · doccheck GREEN · grave named · push.

## Notes from upstream
