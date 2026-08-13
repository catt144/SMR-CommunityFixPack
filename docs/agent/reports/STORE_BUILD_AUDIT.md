# The store build's audit ledger — six sweeps, every finding adjudicated

**2026-08-13, by `agent/prompts/public-docs/03_BUILD_STORE.md` (consumed).**
Deliverables audited: `STORE_FIXPACK.md` · `STORE_OPTIN.md` ·
`STORE_METADATA_STRINGS.md`.

⭐ **Written for `04_FABLE_AUDIT.md`'s job 1**, which re-runs two of these sweeps
as a control and compares yields. Per sweep: what was searched, what came back,
and a verdict on every finding — *confirmed → fixed* · *confirmed → deliberate,
and why* · *refuted, and what the sweep missed*. **A sweep recorded only as
"clean" cannot be audited, so the negative half is written out too.**

**Method.** Phase 1 wrote both documents serially, one voice, no fan-out. Phase 2
ran six subagents concurrently, each holding exactly one rule and the finished
draft. Phase 3 arbitrated: **every finding was re-derived from the entry, the
fact or the source line before a word changed** — and every refusal was
re-derived too.

**Yield: 6 sweeps, 43 distinct findings, 27 confirmed-and-fixed, 5
confirmed-and-deliberate, 8 refuted, 3 routed elsewhere.** Two of the confirmed
findings would have shipped a false instruction to a player.

---

## The two that matter most

### ⛔ 1. The dial uninstall recipe did not reach its destination (sweep 4)

**As drafted:** *"Set both dials back to base, load once, and then uninstall."*
**What the code does:** setting the dials to base makes `ReapplyDials` strip the
modifiers **from the running colony only**
(`SMR-OptInPack/Code/Opt_DroneStatDials.lua:110-149`; measured live in `D09`'s
PT-56 step 3 — exact restore, no relaunch). **The savegame on disk is not
rewritten until the player saves.** A player following the sentence literally
ends with exactly the boosted save the paragraph exists to prevent.

⭐ **The frozen file had it right** — *"(and load/save once)"* — and the module
header offers two *alternatives* (*"set both dials to base, **or** load once with
the mod"*), which the draft silently welded into a three-step sequence. This is
the same failure shape as the console-veto line: a real mechanism, described in
a way that does not survive being walked.

⇒ **confirmed → fixed.** The page now says: set both dials to base, **then save**,
then uninstall — and says which step clears the colony and which clears the file.

### ⛔ 2. "What it writes is inert without it" covered the one item that is not (sweep 5)

`D13_EXPOSED_SET.md` §2b **D10** is on the **KEEP** list precisely because
*"⭐⭐ THE RESIDUE IS THE REPAIR"* — the restored Frictionless Composites bonus is
an ordinary modifier the **unmodded game reads and applies**, which is the entire
point of restoring it. The draft folded it inside an inertness claim.
⭐ The opt-in page, written the same afternoon, gets the identical construction
right: it carves the dial bonus out explicitly. **Same author, same hour, two
opposite treatments of the same object** — which is the argument for the audit
tier in one line.

⇒ **confirmed → fixed.** The item is now carved out and labelled *deliberately
not inert*, with the reason.

---

## Sweep 1 — rule 4 (player language) · agent: Explore · mechanical, high recall

**Searched:** both player blocks isolated by line range (fix pack 170 lines,
opt-in 231). Greps for paths (`.lua|.md|.py|Code/|docs/|agent/|tools/|C:` and
`file.ext:line`), identifiers (snake_case, camelCase, `()`, every backtick span),
ids (`[FDC]##`, `EF-###`, `PT-##`), and the house-word list. Line-by-line read
alongside, since (b) and (d) are not fully regex-reachable.

| finding | verdict |
|---|---|
| The `⛔ HOLE` for the dust-devil bullet was **four sentences of owner-addressed instruction** sitting in a bulleted list a player reads as product information | **confirmed → fixed** — all five HOLE markers reduced to one-line neutral pointers; the explanations moved to the notes |
| Four further HOLE brackets carried internal routing language ("release-time decision", "for-modders page") | **confirmed → fixed** with the same change |
| `%AppData%\Surviving Mars Relaunched\logs` | **refuted** — rule 4's own examples are *our tree and the game's source tree*. This is a folder on the player's machine holding player-owned data, and it is the entire actionable payload of the reporting section. **Deliberate keep** |
| `Ctrl+F1` | **refuted** — a shipped keybinding, i.e. player-facing UI text of the same kind as "Options → Mod Options". It trips an unanchored `F\d+` grep; that is a false positive, not a hit |
| "sitting", "fixed" (adjective), "suite", "verified", "measured" | **refuted by the sweep itself** and recorded — ordinary English, not house vocabulary |

**Negative half, explicitly:** zero hits inside either block for file paths,
function/class/module names, `F##`/`D##`/`C##`/`EF-`/`PT-` ids, or the words
*gate read · probe · co-run · disposition · exposed set · leg · layer 2 ·
residue*, and no use of `fixed`/`tested` as status vocabulary. Every citation in
both files sits outside the player-text rules, where it belongs.

## Sweep 2 — §4.5 vocabulary and the two forbidden moves · agent: Explore

**Searched:** §4.5 and §7 read first as authority. Case-insensitive grep of the
full forbidden list plus near-synonyms (*rock solid · flawless · foolproof ·
bulletproof · impossible to*), then a second pass on every instance of *safe ·
safety · compatible · harmless · never · always · completely · promise*, then a
line-by-line read for the two moves.

| finding | verdict |
|---|---|
| *"Anyone who lifts the limit with a generic 'multiple wonders' mod walks straight into it"* | **confirmed → fixed.** §7 rule 2 bars saying what another mod does not handle — "not softened, not implied by juxtaposition". Rewritten to argue from **our** scope: lifting the limit without repairing the binding is not worth doing |
| *"harmless, but permanent"* of the dial residue | **confirmed → fixed, and it was refuted by our own record**: `D13_EXPOSED_SET.md` §2 calls D15 *"the only genuinely HARMFUL residue in either pack"*. The word was inherited from the frozen file and contradicted the derivation that exists to govern it |
| *"restores the game's own behaviour instantly and completely"* | **confirmed → fixed** — softened. Source-verified only, and this module's playtest is frozen (PT-52) |
| *"in our own stress tests colony-scale repair time was dominated by trip count and distance"* | **confirmed → fixed** — see sweep 3 #7; the measurement attribution was untraced *and* the distance half had been withdrawn |
| *"loads perfectly well"*, *"put right"*, *"are cleaned up"* | **confirmed → fixed** (intensifier cut; the save-repair qualifier hoisted into the section intro) |
| *"The policy never suffocates anyone"* / *"Nobody is ever put outside"* | **split verdict.** The first is **confirmed → fixed** (rewritten as a statement about how the module is built). The second is **confirmed → deliberate**: it is a scope statement about what the module does, and it is the reassurance the whole paragraph exists to give |
| *"Your existing save is fine"* | **confirmed → deliberate** — the enumerated footprint follows it in the same breath, which is the strongest mitigation available |
| The six remaining absolutes ("your orders always win", "never nags again", …) | **refuted** — scope statements about what a module touches, not reliability claims. Recorded as a set, per the sweep's own request |

**Negative half:** the literal forbidden-word grep produced **one** hit across
both files, and it was in a notes table outside the player text. All three uses
of *safe* are correctly qualified. *"Compatible with all mods"* is not merely
absent — the page states the negative outright. **No internal status vocabulary
anywhere**, no fixed-vs-tested split, no count of fixes. And §4.5's flagged
community-standard sentence did not ship.

## Sweep 3 — evidence tracing · agent: general-purpose · the expensive one

**Searched:** 13 fix-pack entries and 10 opt-in entries opened and read (not
just their index rows), `D13_EXPOSED_SET.md` §2a/§2b/§2c/§5/§10.9, `FIX_POLICY`
§2/§5/§7/§8, `EF-014`, both `STATE.md`, the TestKit's probe-file inventory, and
a live `--emit-counts` re-emission. It also audited **the drafts' own trace
tables** rather than trusting them.

| finding | verdict |
|---|---|
| **#1** *"Your manual residence and dome assignments always win"* | **confirmed → fixed.** `D07.md:199-212`: the in-dome pass checks forced residence, the **cross-dome pass checks forced dome only** — a pinned Senior can still be emigrated. Owner-ruled that way 2026-08-11. The page now states both halves |
| **#3** the free-work door omitted | **confirmed → fixed.** `D12` — a flagged dome neither pushes out nor refuses while it holds a job someone could take. The page said jobseekers move; it now says when they do not |
| **#4** second-sun panels on a mid-session enable | **confirmed → fixed.** `D04` PT-55 measured it, and the entry says in terms that it is *"worth saying in player-facing text"*. Now said |
| **#5** the drone speed dial's arithmetic | **confirmed → fixed.** PT-56 measured 2x as `1728 → 3168`, i.e. **+1× base**, not +2×. The draft said "adds that multiple". Rewritten as *the label is the total* |
| **#7** the withdrawn distance reading | **confirmed → fixed.** `D06` B2 measured hauling at 3h03m of a 3h27m leg; the **distance** reading from the same leg was explicitly withdrawn. The page now claims hauling only |
| **#10 / #11** the footprint list asserted as exhaustive | **confirmed → fixed.** D6 and D9 had no member in the list; §2a's capturable code was outside the citation entirely. Now: "everything it stores **by name**", plus one plain sentence that work caught mid-flight finishes on the game's own code and stops |
| **#13 / #14** trace-table gaps (Hotel wrinkle sourced only to the frozen file; achievements row missing from the opt-in table) | **confirmed → fixed** — eight trace rows added, the Hotel wrinkle re-sourced to `Opt_NoHomeless.lua:289-312` instead of the frozen file |
| **#12** the trains claim | **confirmed → fixed** (clause cut, so the table and the text now agree) |
| **#2 / #6 / #8 / #9** whole opt-in module blocks "UNEARNED" because `D12` is `speced`, `D06`/`D07` are `built`, `D01` is `opt-in` | ⛔ **REFUTED, and this is the sweep's one systematic error.** It applied the **fix pack's F-entry status vocabulary** to the opt-in mod's **design entries**, where those words mean something else: a D-entry's status tracks its *design/playtest* item, not whether the module ships. All eight modules are built, registered and audit-sustained (opt-in `STATE.md`, split chain 2026-08-12), and `PUBLIC_DOCS_DESIGN.md` §8 lists the opt-in copy as **safe to write now**. ⭐ **What the sweep missed:** the bar it was given is the bar for *claims about repairs*, not a licence requirement for *describing what a shipped module does* — which a player can check in thirty seconds on the Mod Options page. **What it got right underneath:** findings #1/#3/#4/#5/#7 are all inside those same blocks, and every one of them was a real behavioural over-claim. The status objection was wrong; the reading that produced it was worth every minute |
| **borderline** — *"only by a companion mod"* | **confirmed → deliberate.** Literally inaccurate (the console does veto a per-call fix mid-session, `F97` fully), and it is §9.1's reasoned ruling: the route works for an unpredictable minority and a player cannot tell which |
| **borderline** — "elevators" among the routed-away arrivals | **confirmed → fixed.** `D03` enumerates `ChooseDome`'s callers and elevators are not among them; changed to "rockets and landers" |
| **borderline** — "before a release goes out" | **confirmed → fixed.** `WORKFLOW.md:274` frames the A/B pair as pre-flight when one is owed, not as a per-release gate. The promise was dropped |

**Negative half, and it is the most valuable part of this sweep:** **all seven
"What it fixes" examples came back clean** — every one traced to a `tested`
entry, and every player sentence matched the entry **body** rather than its index
title. `F52` in particular is scoped *away* from its own still-open half. **All
five judgment-call bullets clean.** Every number clean, re-emitted live. The
frozen file's four known-false claims are all absent, and the one place it was
still the only cited source (the Hotel wrinkle) is now re-sourced to code.

## Sweep 4 — the route check · agent: general-purpose

**Searched:** located the game source (`…\Project Spark\ModTools\Src`, path
recovered from `WORKFLOW.md:82`) and opened 12 route sites — Mod Options
category and its platform gate, `HasOptions`/`ApplyModOptions`, the options
screen's gamepad actions, the Ctrl-F1 action and `IsBugReporterEnabled`, the mod
manager's unload/restart flow, the train construction button and its costs, the
Ctrl+click broadcast idiom, Hotel policy strings — plus both mods' `metadata.lua`
and `items.lua`, and `%AppData%` enumerated on disk.

| finding | verdict |
|---|---|
| The dial uninstall recipe | **confirmed → fixed** — see "the two that matter", above |
| Ctrl+click named on a page that promises every platform | **confirmed → fixed.** The module wires `OnAltActivate` with a `<ButtonY>` hint — the mechanism *is* controller-reachable and the store page was the only place that dropped it. Both sites now name the controller equivalent |
| *"a vanilla feature the game… does not go out of its way to tell you"* | **confirmed → fixed.** The button carries a rollover naming Metals and Electronics, and the Command Center row repeats it. Clause cut — the *route* itself is walkable on all three platforms and the claim about it stays |
| *"Toggles take effect immediately"* | **confirmed → fixed** — `ApplyModOptions` fires on **Apply**, and there is a Cancel path. Now "as soon as you press Apply" |
| *"as it does for any mod"* (restart) | **confirmed → fixed.** Our claim is conservative and true for our two mods; the generalisation is not ours to make. Narrowed |
| Ctrl+F1 on Steam Deck | **confirmed → fixed** — `IsBugReporterEnabled()` (`uiXBugReportDlg.lua:1-3`) excludes `Platform.steamdeck`. I re-derived this one myself before the sweep returned; both agreed |
| `%AppData%` under the Microsoft Store's redirection | **confirmed → fixed cheaply** — "usually in", which costs nothing and covers the case neither of us can verify |
| *"a companion mod that loads before this one"* | **confirmed → deliberate.** Unverifiable in the load-order half, and already recorded as design hole 3. The sentence states the condition and promises no method |

**Negative half, and it is the reassuring one:** **no Mod Options instruction
anywhere in the fix-pack text, and no developer-console instruction in either.**
Those are the project's two historical false claims and both are genuinely
absent. The sweep confirmed independently that a player running only the fix pack
sees no Mod Options category at all (`HasModsWithOptions()`; the fix pack's
`metadata.lua` has no `default_options`). Routes positively confirmed walkable on
all three platforms: the Mod Options path and its title string byte-for-byte,
replacement trains, Automated Mode / Edit Payload, the Hotel policy row, and the
mod manager itself.

## Sweep 5 — the standalone test · agent: general-purpose

**Searched:** both documents end to end, tier boundaries drawn and quoted, every
tier-0/tier-1 claim tested against every later paragraph in **both** files, and
each file's claims about the *other* mod tested against that mod's own page.

| finding | verdict |
|---|---|
| **F2** *"Every fix targets a defect… the code says one thing and does another"*, against tier 2's *"there is no coding error here"* | **confirmed → fixed.** Tier 2 contradicted tier 1 instead of adding to it. Tier 1 now carries the exception itself: two of the five are calls where the code is not wrong at all |
| **F3** the inertness umbrella | **confirmed → fixed** — see "the two that matter" |
| **F4** modules that relocate colonists are not reversible in the way the page implies | **confirmed → fixed** in three places: *what a module already did stays done* |
| **F7** the flat *"it does not rebalance the game"* header while the only balance-affecting disclosure is a blocked hole | **confirmed → fixed**, and carefully: the tier-1 bullet now says *one of them changes how the game feels* — which closes the standalone gap **without** pre-empting checklist 22b's scale word |
| **F8** the achievements rule sat outside the page's own "four things" fence | **confirmed → fixed** — moved up against design §6.1, which calls burying it *"the single most consequential omission"*. The two pages now agree on where it belongs |
| **F1 / F6** the split's premise stated as a clean binary that leaks in both directions | **confirmed → fixed** on both pages. This is the load-bearing claim of the whole two-mod product and neither page survived expansion |
| **F9** the reader who infers a judgment call can be switched off | **confirmed → fixed** — one clause in the judgment-calls intro: they cannot be switched off from the game's own menus on any platform |
| **F10** "one setting" vs two dials, and an ambiguous "it" | **confirmed → fixed** |
| **F11** what becomes of an already-built second sun | **confirmed → fixed**, and the fact existed: `Opt_MultipleSuns.lua`'s header — *existing suns are ordinary buildings and keep working either way* |
| **F5** the two heal claims in the category list | ⚖️ **partly refuted.** Each is scoped to the exact damage state and is deterministic for it per its entry (`F81`'s reconciliation, `F03`'s id-pattern sweep) — the sentences are accurate. **The placement half is fair**, and one clause in the section intro fixes it |
| **F12** tier-0 "safe to add" vs the backup advice | **refuted** — the advice is explicitly generic to *any* mod, and §4.5 allows the qualified form. **What the sweep missed:** that the hedge's own sentence disclaims being about us |

**Negative half:** three tiers passed. **Opt-in tier 0** is clean against all
eight module blocks. **Fix-pack tier 1, question 3** (do I need anything else) is
clean in both directions across both pages. And the **opt-in dial-residue
disclosure** was judged exemplary — flagged in tier 1, stated in full in the
module block, restated at removal.

## Sweep 6 — staleness · agent: Explore

**Searched:** re-emitted `--emit-counts` in **both** repos and quoted both
outputs verbatim; checked every number in both drafts against them; verified the
five post-split facts against **code** rather than documentation; checked every
path cited in the notes tables for existence.

| finding | verdict |
|---|---|
| `02_QA.md` cited five times — the file was consumed and deleted | **confirmed → fixed.** Chain rule 2 deletes a prompt when it is consumed, so every such citation is born dead. Re-pointed at `PUBLIC_DOCS_DESIGN.md`, which carries the same corrections inline and survives |
| *"covering this pack and its companion mods"* (plural) against *"there **is** a companion mod"* (singular) | **confirmed → fixed** by deleting the clause: the shared kit's scope is not a claim the page needs to make |
| the notes said "more dust devils on **most** settings" where 22b's approved phrase is *"on **some** map settings"* | **confirmed → fixed.** Small, and exactly the drift 22b exists to stop — in the same file that quotes the correct phrase twice |
| *"That list is the whole of it"* against §2b's eleven rows | **confirmed → fixed** (merged with sweep 3 #10) |
| the fix pack's live `metadata.lua` still carries the false console claim and the dead working title | **confirmed → routed**, not fixed: `metadata.lua` is code and outside this chain's fence. It is release-prep's, recorded in `STORE_METADATA_STRINGS.md` |
| `Opt_DroneOverhaul.lua`'s header still names the pre-split Mod Options path | **confirmed → routed** — other repo, code comment, no player impact |

**Negative half:** every number current — **94** re-emitted in both repos, eight
modules with seven off and one active-at-base, 74 modules, eleven blank rows,
the pinned version, `74/74` and `8/8` and `1/8`. Both `metadata.lua` files
checked for the Mod Options split: correct in both directions. The override
table name, the decided display name, and the module counts all verified
**against code**. Line-exact spot checks on `MOD_DESCRIPTION.md:225-249` and
`WORKFLOW.md:274` both held. Every cited entry id resolves in the right repo.

---

## What the sweeps did not cover, stated so it is not mistaken for coverage

* **No sweep read the two documents as a scroller on a phone.** Length and
  formatting for the actual store card were not audited; the design defers store
  formatting to release prep.
* **Nothing here is play-verified.** Every route is source-derived. The combined
  sitting measures one toggle flip and the console-listing question (design holes
  4 and 11), and prompt 4 should upgrade what it settles.
* **`STORE_METADATA_STRINGS.md` was audited only by sweep 6**, and only for
  staleness. Its two `description` strings have not been through sweeps 1–5.
* ⚠️ **The judgment-calls section's fifth bullet is NOT covered by any sweep.**
  It was a hole while the six ran; the owner closed 22b immediately afterwards
  (*"change any wordings to their accurate versions"*) and the bullet was pasted
  in the approved 2026-08-02 phrasing. **It has been checked by hand against
  rule 4 and §4.5 and re-derived from `F97.md:334-352`, and by nothing else.**
  ⇒ **Prompt 4 should treat that one bullet as unswept text**, and it is a fair
  target for the control in job 1.

## Where I overruled a sweep, in one place

Sweep 3's status objection (findings #2/#6/#8/#9) is the only wholesale refusal
in this ledger, and it deserves the scrutiny: **it would have deleted four of the
opt-in page's eight module blocks.** The refusal rests on `PUBLIC_DOCS_DESIGN.md`
§8's explicit ruling that the opt-in copy is safe to write now, on the opt-in
repo's own audit-sustained build record, and on the difference between claiming a
*repair* and describing a *shipped setting*. ⚠️ **If prompt 4 disagrees, the
blocks are what changes, not the sentences** — the behavioural corrections that
came out of those same blocks stand either way.
