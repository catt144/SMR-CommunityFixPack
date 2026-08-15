# Release assembly — the uninstall story and the disposition, per product

**Assembled 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`,
Job 2.** ⛔ **Every element below was re-derived from its own source. Nothing was
quoted from `STATE.md`**, per the prompt's own instruction and chain rule 3.

⚠️ **This is a report; reports are not authority.** Its player-text block is
reference text — the version every shipping surface must agree with. The two
store cards' short removal sections and the site's *"How do I get it out?"* are
already-audited surfaces and are **not** replaced by it.

---

## 1. What ③ inherited, and what re-derivation found

| inherited item | its source | state at re-derivation, 2026-08-14 |
|---|---|---|
| D13's uninstall text | `D13.md` → *"The uninstall procedure — player-facing DRAFT"* | ⛔ **DRAFT tier, and it does not survive the route-check its own header demands.** Three defects, §2 |
| the engine-notice sentence | `D13_EXPOSED_SET.md` §10.9(4), **corrected by measurement** (`D13_VERIFICATION.md` §4.5) | ✅ holds, unchanged. Both packs and the rescue tool produce the identical engine line; it self-clears on the next save |
| the version-skew statement | spec §10.6 | ✅ holds. Detection is impossible by construction — the one version-stamped name is dropped by the engine on the first load without the pack — so it is answered by disclosure |
| the §10.5 dialog texts | spec §10.5 **as corrected 2026-08-14 by Job 0** | ⭐ **RESOLVED, and the resolution changes what may be quoted**: the frozen design text is superseded as a quotable source; the BUILT text is authoritative. ⛔ No surface in this release quotes either — see §5 |
| the 27-site disposition table | `D13_EXPOSED_SET.md` §2a + §2b, §7 | ✅ **membership re-counted at the tables themselves: 12 + 15 = 27**, matching the third derivation the audit ran. ⛔ Agent-side only — §4 |
| F102's disclaimer + its uninstall revert | `F102.md` | ✅ disclaimer stands (cure still unverified); ⭐ the **uninstall revert is MEASURED**, promoted from SOURCE 2026-08-14 — §6 |
| the suite numbers | `archive/rs_r0_Mars.exe-20260813-11.42.08.log`, read directly | ✅ **`78 PASS, 0 FAIL, 16 SKIP, 0 ERROR`**, 78 + 16 = **94** — §7 |

---

## 2. ⛔ The route-check D13 demanded — and the frozen draft fails it three ways (a fourth, (d), found by the terminal audit)

D13's draft carries its own instruction: *"step ③ owns final wording and MUST
route-check every 'you can/do X' line per the walked-not-derived rule."* Walked,
not derived:

### (a) The draft never tells the player to restart the game — and that is the one step the whole thing turns on

The draft's step 3 is *"Uninstall the mod(s)."* full stop. ⛔ **A Mod-Manager
disable that is not followed by a full process restart leaves a state nobody had
named**: the code and every registration still live while the mod's persisted
permanent is already gone. That is D13's own headline finding (`corun-batch-2`
leg T, recorded on the entry) and it is a standing gate in this project. A player
who follows the draft literally measures the mixed state and concludes the
uninstall did not work — or worse, saves in it.

⭐ **The already-audited site page has this right** and the draft does not:
`content/faq.md` → *"Turn it off in the Mod Manager, or remove it from Paradox
Mods. **Restart the game fully.** Until you do, it is still running."*
⇒ **the site's ordering is the correct one and the assembled text below takes it.**

### (b) The draft's only remedy for the one harmful residue is a tool that may never exist

The draft ends: *"If that applies to you — or you removed the pack without step 2
— install **Save Rescue**, load the save once…"* ⛔ **Save Rescue's publication is
an unmade owner decision** (checklist 17, "build ≠ publish"), so as written the
draft's single answer to the drone-dial problem route-checks to **nothing** on
every platform today.

⭐ **And it omits the free remedy that always exists**: set both dials back to
base, press Apply, save. That costs the player thirty seconds, needs no
download, works on every platform, and is what both the opt-in card and the site
already tell people. ⇒ **the assembled text leads with the free remedy and
demotes the tool to a fallback for people who are already too late** — which is
also the only honest framing, since that is the exact population the tool was
built for.

### (c) Step 2's "update it to the latest version" is inert at launch and unexplained

*"With the mod still installed: update it to the latest version, load your
colony, let the load finish, save, exit."* The mechanism is real — a current pack
build deletes older builds' leftover names as it finds them, which is why loading
once under the newest version before removing it leaves less behind (the two
legacy rows in the rescue tool's own table exist precisely for saves that *never*
did this: `SMRFixPack_fixed_loop`, `SMRFixPack_rocket_fuel_key`, both marked
*"the current pack deletes it itself"*).

⛔ **But at initial release there is no earlier version to update from**, so a
launch-day player reading step 2 is being told to do something that cannot
apply, in the middle of a procedure where every other step matters. Written as
an unconditional instruction it teaches the reader that some of these steps are
decoration. ⇒ **the assembled text keeps the step, makes it conditional, and says
what it is for.**

### (d) Found by the terminal audit, 2026-08-14 (prompt 2): the rescue flow never says SAVE — and the notice sentence promises a screen event the game does not show

⛔ **The draft's rescue instruction — "load the save once, read what it removed,
and delete it again" — loses its own work if followed literally.** The clean
pass edits the **loaded** colony; only the player's next save writes the cleaned
state into the file. Load → read → quit-without-saving → delete leaves the dial
boost in the file forever, with the tool gone. The corrected sentence (with
**save** in the sequence) is now in `RELEASE_DESCRIPTION_OPTIN.md` FILL-IN 2 and
throughout the rescue card and its `metadata.lua`; this file's fill-in section
inherits the fix by pointing there. ⚠️ The shipped report dialog has the same
omission — a code string, priced with item 28's re-witness, noted there.

⚖️ **And the §1 row above that says the engine-notice sentence "holds, unchanged"
inherited an unverified extrapolation.** The §4.5 measurement is a **log** line
(`ModLog`, `Mod.lua:1199`); the only on-screen missing-mods warning
(`GetMissingMods`, `SavegameMetadata.lua:97-99`) **excludes mods marked
`optional` — all three of ours**. So §3's "One notice you will see" paragraph
describes a notice no player of these mods will see. It sits verbatim on both
audited cards and the site FAQ, so it is **routed as checklist item 29** and the
§3 text below is left matching the cards until the owner rules — one decision,
every surface changes together.

### What the route-check did NOT find

ℹ️ The dial recipe on the opt-in card reads *"set both dials back to base and
press Apply, then save the game"*, while the site adds the precondition *"with
your colony loaded … done from the main menu it clears nothing."* ⛔ **This is not
a card defect and is not filed as one.** *"Save the game"* is only performable
with a colony loaded, so the card's recipe implies its own precondition; the
site's version is more explicit because a page has room to be. Recorded so a
later reader does not re-find it and file it twice.

---

## 3. The reconciled uninstall story — reference text, per product

⛔ Player language gate (rule 4) applies to everything between the rules.

═══════════════════════════ PLAYER TEXT — BEGIN ═══════════════════════════

### Removing the Community Fix Pack

1. **Back up your saves first.** Always, for any mod change — this is not
   specific to us.
2. **If you have been using an older version of the pack**, and only then: with
   the mod still installed, update it, load your colony, let the load finish,
   save, and exit. A newer build clears out leftovers from older builds as it
   finds them, so this leaves less behind. On a first release there is no older
   version and nothing to do here.
3. **Turn it off in the mod manager, or remove it.**
4. **Restart the game fully.** Until you do, the mod is still running, whatever
   the mod manager shows you.

**What comes back:** the bugs it was holding back.
**What stays:** repairs it already made to your save. A bonus it cleaned up does
not come back; a track it re-numbered stays re-numbered.
**What is left in the file:** a small amount of bookkeeping — timestamps, stamps
and flags — that the unmodded game never reads. A couple of them clear themselves
the next time you save. **Two entries are left on purpose because they are
repairs, not leftovers:** the Large Wind Turbine bonus the game's own patch
migration dropped, and a one-shot mark that stops a track repair being done
twice. Deleting either would bring its bug back with no mod left to fix it.

### Removing the Opt-In Modules — do this one thing first

⚠️ **If either drone dial is off its base setting, deal with it before you
uninstall.** A non-base dial is stored in your save as an ordinary bonus of the
kind the game hands out itself, so with the mod gone your drones keep the boost
and nothing is left in the game to take it off.

**With your colony loaded:** set both dials back to base, press **Apply**, then
**save the game** — and then uninstall. Setting them to base clears the boost
from the colony you are playing; saving is what clears it from the file. Doing it
from the main menu clears nothing, because there is no colony to clear.

Then remove it exactly as above: turn it off in the mod manager, and **restart
the game fully**.

Everything else this mod leaves is inert: a "you have seen this warning" mark on
a building, and two dome policy flags. The unmodded game has no idea they exist.
What a module already did stays done — colonists a housing module moved do not
move back.

═══════════════════════════ PLAYER TEXT — END ═══════════════════════════

✅ **RULED 2026-08-14, both gates:** checklist **17** — Save Rescue is **not
published at launch**, held as a contingency for post-release reports; the
publish-gated "already uninstalled" section was therefore **deleted** per its
default (the honest text ends above, and the player is told nothing they cannot
act on). And checklist **29** — the "one notice you will see" paragraph was
**struck from every surface** (it promised a screen event the game never shows
for `optional_mod` mods; see §2(d)). If Save Rescue ever launches, the ready
paragraph is `RELEASE_DESCRIPTION_OPTIN.md`'s drafted FILL-IN 2 sentence, which
carries its own shipped-module control and the audit's save step.

---

## 4. The disposition table — referenced, never pasted (rule 4)

**Where it lives:** `D13_EXPOSED_SET.md` — §2a (capturable code, 12 sites), §2b
(persisted named data, 15 sites), §2c (the negative half), §5 (the curated
KEEP/REMOVE lists with a stated reason per row), §7 (the release-gate table
required by `FIX_POLICY.md` §3a).

**Membership re-counted at the tables themselves this session: 12 + 15 = 27.**
That is a third-derivation match, not an inherited number.

⛔ **No exposed-set count appears on any player surface in any form**, and none
does. The standing bar is `PUBLIC_DOCS_DESIGN.md` §8: *the player-facing statement
is the enumerated footprint in player words, which is a different artifact from
the derivation.* The player text in §3 above obeys it — it names what is left in
plain nouns and counts nothing.

⚠️ ③ therefore **references** the table and does not reproduce it. Anyone
tempted to paste it onto a store card or the site is pasting file paths, module
names and identifiers into player text, which is the hard gate.

---

## 5. The dialog texts — what Job 0 changed about what may be quoted

Job 0 re-derived spec §10.5 against the built `report_text()` and found **four**
divergences, of which two are substantive; the correction block and the evidence
are in `D13_EXPOSED_SET.md` §10.5 and `D13.md`. What ③ needs from it:

* ⛔ **The frozen design text is no longer a quotable source.** Anything that
  quotes it is quoting a string the build has never printed.
* ✅ **The built text is authoritative and is written out** in the same correction
  block, with the rules needed to reconstruct any case.
* ⭐ **Nothing in this release quotes either.** Both store cards, the site and the
  rescue description describe what the tool *does* and never reproduce its dialog.
  ⇒ **Checklist item 28 cannot invalidate any surface built by this chain**,
  whichever way the owner rules. That is deliberate, and it is why the item could
  be routed rather than blocking.

---

## 6. F102 — the disclaimer stands; the uninstall revert is now measured

Re-derived from `F102.md`, not from prose about it:

* ⛔ **The cure remains UNVERIFIED and ships disclaimered** — the owner's
  2026-08-12 ruling, recorded as *"the verification boundary, not a gap."* Two
  negative repros (the owner's own hardware; a Steam Deck) are consistent with
  the hypothesis but do not confirm the fix on the hardware that froze. **Only a
  witness-class report from an affected player moves that.**
* ⭐ **The uninstall claim is MEASURED as of 2026-08-14** and is no longer an
  argument: with both packs Mod-Manager-disabled (`archive/cs_a1_*`, gate line
  `pack=0/0`), the same deposit read back the vanilla sign entity with **zero**
  re-sign lines. The retarget reverts cleanly and the vanilla entity is still
  there.

**What that licenses on a player surface, exactly:** the general removal
statement in §3 — *repairs already made stay, and nothing of ours is left holding
your save together* — now has one more measured leg under it. ⛔ **It licenses no
new sentence about this fix**, because a player surface that singles out one fix's
uninstall behaviour is advertising a defect the disclaimer already covers. No
card mentions it and none should.

---

## 7. The suite numbers, re-derived at their source

⛔ Not from `STATE.md`. Read out of the archived log directly
(`docs/archive/rs_r0_Mars.exe-20260813-11.42.08.log`):

```
---- 78 PASS, 0 FAIL, 16 SKIP, 0 ERROR ----
```

78 + 16 = **94**, which matches `python tools/doccheck.py --emit-counts` at this
session's moment (`TestKit probes: 94`). Two independent instruments, same total.

⛔ **The 16 SKIPs by name, never as a total** (STATE's standing rule):
`CaveInsNoDisasters` · `MilestoneCrash` · `TrainsToVoid` · `BrokenTrackSalvage` ·
`TrackSalvageWipe` · `LakeEntombment` · `GhostFarmOxygen` · `LowStorageWarning` ·
`AnomalyCaveInMap` · `TechDescriptionBuilding` · and the six save-rescue probes
(`SaveRescueCleanPass`, `SaveRescueStandDown`, `SaveRescueIdempotent`,
`SaveRescueHealBounds`, `SaveRescueSelfClean`, `SaveRescueResidueTable`), which
skip with the stated reason *"save-rescue mod not installed (separate mod — not a
failure)"*.

⭐ **The only number that reaches a player is 94**, on the fix-pack card, as
*"an automated suite of 94 checks is run against the game with the pack and
without it."* ⚠️ **That sentence is exactly right and must not drift into
"94 passing"** — 78 pass and 16 skip in that cell, and a skip is not a pass. The
card does not say passing, and rule 6 is why.
*(⭐ 2026-08-15, `unattended-3` audit: the card's number is now **96** — two
probes added with that chain's two modules; the suite read `80/0/16/0` of 96,
SKIP set unchanged BY NAME from the list above. The must-not-drift rule is
unchanged.)*
