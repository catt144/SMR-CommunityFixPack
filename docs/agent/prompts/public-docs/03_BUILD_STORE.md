# Chain prompt 3 — build the two store descriptions

**Read `README.md` first — binding chain rules apply, especially rule 4 (player
language), rule 6 (no unearned claim) and the exposure framing.** Staleness check
across all repos, live todo list updated per item.

⛔ **Read `## Notes from upstream — prompt 2` at the bottom of this file BEFORE
you open the design report.** It carries a BUILD verdict with six corrections,
three of which change what you are allowed to write.

---

## ⭐ CONCURRENCY IS BACK ON — the OWNER-ATTENDED SITTING outranks you

⚠️ **Amended 2026-08-13, ~30 minutes after this file was written.** The D13 chain
is gone (`agent/prompts/d13-rescue/` no longer exists, consumed `f08a3fc`) — but
the owner is starting **the combined sitting** (`agent/prompts/COMBINED_SITTING.md`,
plus folded-in passes from `agent/prompts/CAPTURE_SITTING.md`) while you run.

⛔ **THEIR SESSION HAS PRIORITY AND IT IS NOT CLOSE.** It is owner-attended, its
readings are perishable (two D13 dialogs write no log line — the owner's eyes are
the only instrument that can ever sample them), and it is what grants D13
`tested`. **You are writing prose that will still be there in an hour.** On any
clash — a file, a count, a checklist item, a rebase — **their version wins and
yours re-derives.**

1. ⛔ **Do NOT write `docs/agent/STATE.md` or `docs/PLAYTEST_CHECKLIST.md`.**
   The sitting writes both: it strikes 26b, records the PT-20 redo, and lands
   D13's `tested`. ⇒ **Put anything you owe those files in your outbox**
   (`04_BUILD_SITE.md`'s Notes from upstream) and let a later prompt land it.
   ⚠️ **Re-reading first is NOT protection and has failed twice in this tree:**
   `git add <path>` takes the **whole file**, so the other session staging its
   own legitimate edit carries yours into their commit under their message.
   That is how prompt 1's item-24 rewrite ended up inside D13's `6b75e11` —
   text intact, provenance wrong.
2. ⛔ **Never `git add -A` / `-u` / `.`** Stage by explicit path, every time.
   `git pull --rebase` immediately before each commit.
3. ⛔ **Not yours:** `agent/prompts/COMBINED_SITTING.md` ·
   `agent/prompts/CAPTURE_SITTING.md` · `agent/bugs/D13.md` ·
   `agent/facts/EF-023.md` · `agent/reports/D13_EXPOSED_SET.md`.
4. ⚖️ **Checklist 22b may come back while you work** (the dust-devil scale word —
   see Job 3). ⛔ **Do not strike it yourself even if the owner answers it in
   your session.** Record the answer in your outbox and use it; striking the
   line is a checklist write, which rule 1 forbids you.

⚠️ **If doccheck goes red for something you did not touch, it is probably the
sitting's in-flight edit:** `git status`, confirm whose it is, do not "fix" it.

⭐ **When the sitting is over** (the folder's briefs are deleted — that is their
done-condition), rules 1 and 4 lift and both files are normal again.

### ⭐ Three of your facts are about to become measured

The sitting settles things this chain currently holds as source-verified. **Do
not write around them and do not pre-empt them** — write the sentence the
evidence supports today, and flag it for prompt 4 to upgrade:

* **Hole 11** — whether `SMRFixPack.ListFixes()` puts anything ON SCREEN
  (Pass F is now a check, not a capture). ⛔ Until it answers, no surface says
  the console **shows** a list.
* **Hole 4's play half** — whether an opt-in toggle really applies without a
  restart (Pass C, one toggle flip).
* **D13's `tested`** — which is what finally lets the uninstall half of §4.2's
  fourth answer stop being a shape.

---

## ⭐⭐ HOW TO RUN THIS — write serially, audit in parallel, arbitrate everything

**Owner instruction 2026-08-13:** use subagents for the sweeps and act as their
auditor. ⭐ **Adopted, with one boundary**, because the split is not arbitrary:

### ⛔ Phase 1 — WRITE. One agent, no fan-out.

**Both descriptions are written by you, in one voice, start to finish.** Do not
hand sections to subagents. §4's whole design is that the three tiers *stand
alone but never contradict each other*, and the standalone test — *"if a reader
stops here and acts, is anything they now believe false?"* — is a property of the
whole document, not of any paragraph. Split the prose and you get seams a reader
feels and a tier-1 claim that tier-2 quietly widens. The frozen file is 748 lines
in one voice and that voice is the raw material.

### ⭐ Phase 2 — AUDIT. Fan out, one rule per agent, all on the finished draft.

⚠️ **This is where the value is, and the reason is on the record: an author
cannot see their own text.** The `F76` draft "sat in the file ready to publish
for a week — nothing about its prose flags it." §5.1's inverted rate claim was
written by a careful prompt, passed its own review, and was caught only by a
fresh reader with the entry open. **Three false claims have now reached a
player-facing draft in this project and not one was caught by its author.**

Launch these **concurrently**, each with the finished draft and its ONE rule:

| # | sweep | the rule it enforces | shape |
|---|---|---|---|
| 1 | **Rule 4** | no file path, function name, `F##`/`D##` id, or house word (`gate read`, `probe`, `co-run`, `disposition`) in anything a player reads | mechanical, high recall |
| 2 | **Vocabulary** | §4.5's forbidden list, plus the two forbidden *moves* — never quote our internal status words, never compare against another mod | mechanical |
| 3 | ⭐ **Evidence** | every factual sentence traced to its `agent/bugs/` entry or `agent/facts/` fact. ⛔ **The bar is `fixed` + suite + self-checks + the verified save-safety tier — nothing more** | expensive; must open the entry |
| 4 | ⭐ **Route** | every *"you can X"* names its route and confirms a retail player on **PC, Xbox and PlayStation** can walk it | has already caught two false claims |
| 5 | **Standalone** | per tier: *"if a reader stops here and acts, is anything they now believe false?"* | needs the whole draft |
| 6 | **Staleness** | counts re-derived at write time, not copied; post-split facts (Mod Options lives in the opt-in mod; the override table is `SMROptInPack_*`; the display name is decided) | mechanical |

⚠️ **Sweeps 3 and 4 are the ones that find real defects and the ones most likely
to hand you a confident wrong answer.** Give them the evidence bar and the
entries, and expect false positives.

### ⛔ Phase 3 — ARBITRATE. You are the auditor, and auditing means re-deriving.

⛔⛔ **Do not act on a subagent's finding because it sounds right.** Open the
entry, the fact or the source line yourself and confirm it before you change a
word — and equally, **do not dismiss one because it is inconvenient**. This is
the house rule that produced every good result in this project's chain history,
and it is the rule the `F97` error slipped past when a *recorded* claim was
trusted instead of re-derived.

**For each finding, record one of three verdicts:** *confirmed → fixed* ·
*confirmed → deliberate, and why* · *refuted, and what the sweep missed*.
⛔ **A sweep that returns nothing is a result and gets recorded as one** — silence
is not the same as clean, and an empty report usually means the rule was wrong.

⚠️ **Honest expectation: this does not make the job much faster.** The writing is
the bulk and it stays serial. **What it buys is that the adversarial read happens
now, inside prompt 3, instead of in prompt 5 after two more prompts have built on
the error.** That is worth more than the hours.

---

## Job 0 — read what you are building from

`agent/reports/PUBLIC_DOCS_DESIGN.md` **whole** — it is the design and it now
carries prompt 2's corrections inline, marked and dated. Then
`docs/archive/MOD_DESCRIPTION.md` (FROZEN, 748 lines, the raw material and the
tone reference) · `README.md` (this folder) · `docs/agent/STATE.md` ·
`docs/PLAYTEST_CHECKLIST.md` items 21–25 and **22b** (new, yours to close).

⛔ **Re-derive every count with `python tools/doccheck.py --emit-counts` in both
mod repos at the moment you write it.** The probe number moved twice while this
chain was being written.

---

## Job 1 — the fix pack's store description

Build it to §4's three tiers, in §4.2's order: the four install-gating answers
**before** any feature list, category names instead of a count (§4.4), the
allowed/forbidden vocabulary of §4.5 enforced word by word.

* **Split, do not edit, the frozen file** (§3). It documents a one-mod product
  and every *Mod Options → Community Fix Pack* path in it is now false.
* ⛔ **Carry neither `F76` draft block across in any form** (§5.6). They sit at
  `MOD_DESCRIPTION.md:225-249` in the right voice, ready to publish, describing
  a bug that does not exist.
* Rewrite the per-fix disable paragraph (`:487-493`) per §9.1 **as corrected** —
  companion-mod route only. ⚠️ Prompt 2 found the correction was itself too
  strong; read it before you write the replacement.
* ⛔ **Do not place the uninstall-cleanliness sentence** (§8) — Reading A vs B is
  an owner call at launch.

## Job 2 — the opt-in pack's store description

~50% exists: the eight module blocks are written and good. What is missing is the
whole top — what this mod is, why it is separate, and that **neither mod needs
the other** (measured both directions, 2026-08-12).

⭐ Use the decided display name: **"Community Fix Pack: Opt-In Modules"**.

## Job 3 — the judgment-calls section, and checklist 22b

§9's five bullets are owner-approved and ship. ⛔ **The fifth bullet's scale word
is factually wrong** and prompt 2 routed the correction as **checklist 22b**
rather than applying it inside an approved sentence. **Do not ship either
wording until 22b is struck.** Everything else in §9 is ready.

## Job 4 — `short_description` ×2

One sentence each, matching tier 0. Currently placeholders in both `metadata.lua`
files. ⚠️ `metadata.lua` is code — check the scope fence before editing, or route
the strings for a release-prep pass.

## Close

* Append **Notes from upstream** to `04_BUILD_SITE.md` (create it — the manifest
  in `README.md` describes it).
* Update `docs/PLAYTEST_CHECKLIST.md` if 22b comes back.
* `python tools/doccheck.py` GREEN. Commit with `-F`, push, **delete this file in
  the same commit.**

## ⛔ What you may not do

- Publish anything, anywhere, or create an external account.
- Write the fix list or any site page — that is prompt 4.
- Lift the `MOD_DESCRIPTION.md` freeze, or overturn STATE's release sequencing.
- Write a claim the frozen evidence bar does not support.
- Put an exposed-set count on any player surface, in any form.

---

# Notes from upstream — prompt 2 (`02_QA.md`, consumed 2026-08-13)

# ✅ VERDICT: **BUILD**

**The architecture survives the attack and prompts 3 and 4 should proceed.** The
load-bearing move — *the surface set is decided by the searcher, not by the FAQ*
— is right, and the packaging finding it partly rested on re-derives cleanly from
source. **Two sections need rework before their text ships, and both are narrow:**

* ⛔ **§5.1 (the `F97` dust-devil blurb) — its fourth beat is factually
  backwards.** Refuted below. This is the design's own showcase specimen.
* ⛔ **§9's fifth bullet — the same error, inside an owner-approved sentence.**
  Routed as checklist **22b**, not re-litigated.

Everything else — §1, §2, §3, §4, §5.2–5.6, §6, §7, §8, §8B, §10, §11 — **stands
as written**, with the corrections and additions below folded in.

---

## 1 · What was re-derived, and what it said

| claim | source walked | verdict |
|---|---|---|
| §2 — the site would have shipped inside the uploaded mod package | `GedModEditor.lua:678-742` read whole | ✅ **CONFIRMED, and stronger than stated** |
| §2 — `CreatePackageForUpload` is the only packer on the upload path | `:749`, `:764`, `:793` + `ParadoxMods.lua:423` + `SteamMods.lua:41` | ✅ **CONFIRMED for BOTH stores** |
| §2 — the recursion enumerates the whole mod folder | `AsyncListFiles(content_path, nil, "recursive")`, doc at `AsyncOp.lua:89-97` | ✅ confirmed (nil mask = `"*"`) |
| §12 hole 7 — `MatchWildcard` has no Lua body | grepped all of `Src` | ✅ **CONFIRMED** — one call site, no definition, no exported-doc stub |
| §6.2 — the achievements claim | `Achievement.lua:61-63`, `:77` read in context | ✅ **CONFIRMED, scope included** |
| §9.1 — the per-fix veto is read at mod load | `00_Core.lua:384-388` + all five modules | ⚠️ **CONFIRMED, but the conclusion drawn from it is too strong** |
| §0 — the three staleness corrections | git + the site repo | ✅ all three accurate; one is now **closed** |
| §5.1 — the `F97` blurb's fourth beat | `F97`'s own per-preset rate table | ⛔ **REFUTED** |
| checklist 25 — every assessment byte-unchanged | `git log -p` on `BUG_LIST_AUDIT.md` | ✅ **CONFIRMED** — the diff is exactly the two authorised edits plus an explanatory note |

### ⛔⛔ The refutation that matters most — §5.1, and it reached the owner

§5.1's blurb ends *"On the heaviest dust-devil settings you will see noticeably
more devils… The default setting is unaffected."* **Both halves are wrong, and
both are wrong in the player's favour.** From `F97`'s own rate table:

| preset | chance | change |
|---|---|---|
| `Low` | 50 | **+50%** |
| `High` | 75 | **+50%** |
| `VeryHigh` | 100 | **0% — the only untouched preset** |
| `VeryHigh_1` | 75 | +25% |
| `VeryHigh_2` | 75 | **+125%** |
| `VeryHigh_3` | 50 | +5% |

The **heaviest** shipped preset is the one that does not change. The biggest
changes are at the light and middle of the range. And "the default setting is
unaffected" fails under both readings — the untouched preset is the heaviest one,
and the class property defaults (`spawn_chance` 30, `count` 2..4) move **+170%**.

⚠️ **Three things make this worth the space it takes here.**

1. **It was inherited, not invented.** `CHAIN_QA_REPORT.md` §4 says *"the default
   preset is untouched"*. Prompt 1 believed a recorded fact — which chain rule 3
   says is a claim. (`memory: recorded facts are claims too`.)
2. **It drifted from the approved wording in the same move.** The relabel package
   approved *"on **some map settings**"*. "Some map settings" is correct;
   "the heaviest" is not.
3. ⛔ **The same sentence is in §9's fifth bullet, which the owner approved on
   2026-08-13.** So an approved sentence carries a factual error — the second
   time in one week that a routed decision came back approved with something
   false inside it (the first was the console veto). **Routed as checklist 22b.**

### ⚠️ §9.1 corrected — the console CAN disable a fix, for a minority of fixes

§9.1's *"the developer console cannot disable a fix"* is too broad. Reading all
five judgment-call modules:

| module | mid-session veto |
|---|---|
| `Fix_DustDevilSpawnGate` (`F97`) | ⭐ **FULL** — re-reads the veto table on every call (`:332-334`) |
| `Fix_DustSicknessBiorobots` (`F40`) | partial — the retroactive cure only |
| `F55` · `F73` · `F70` | ⛔ none |

So it is the other **three**, not four, and `F97` — the one judgment call a
player is most likely to want off — is fully console-vetoable mid-session.
⛔ **This does not revive the cut line, and the instruction to prompt 3 is
unchanged.** The reason sharpens rather than weakens: **the route works for an
unpredictable minority and a player has no way to tell which**, since
`ListFixes()` prints status, not vetoability. An instruction that silently works
for some fixes and not others is worse than no instruction.

⭐ **The owner's original challenge stands fully vindicated either way.** The cut
line promised *"they can each be switched off individually on PC"*, and *each* is
what fails.

---

## 2 · The route sweep — every "you can X" in the frozen file

Applying §9.1's standing instruction as a sweep. **Four claims, four verdicts:**

| claim | route | verdict |
|---|---|---|
| `:477` *"you can build replacement trains at any station for Metals + Electronics"* | "Construct Train" button on the station infopanel (`customStation.lua:16-18`) **and** the Command Center transportation row (`:459-461`), both with `<ButtonA>` gamepad hints; the game's own rollover names Metals + Electronics | ✅ **WALKABLE ON ALL THREE PLATFORMS** — and the resources are right |
| …*"a vanilla feature the game never tells you about"* | the button carries a rollover naming the cost | ⚠️ **OVERSTATED** — it is under-signposted, not hidden. Cut or soften; it invites *"yes it does, it's right there"* |
| `:487-493` the per-fix console switch | see above | ⛔ **FALSE as a general claim** |
| `:37-39` *"Set the dials back to base before uninstalling"* | Mod Options — but the dials moved to the **opt-in mod** at the split | ⛔ **UNWALKABLE AS WRITTEN.** The fix pack has no Mod Options page at all. The action is still correct; the place named is not |
| `:501` *"Toggles take effect immediately — no restart needed"* | opt-in `00_Core.lua:400-445`; 7 modules consult `IsActive` per call, `Opt_MultipleSuns` uses `on_activate`/`on_deactivate` | ✅ **TRUE — hole 4 CLOSED** (source-verified; the capture sitting now measures it) |
| `:502-503` *"`SMRFixPack_Optional = { … }` still works"* | the table is now `SMROptInPack_Optional` in the other mod | ⛔ **STALE IDENTIFIER** |

⚠️ **`MOD_DESCRIPTION.md` now has four known-bad claims** (F76 explainer, console
veto, the dials' location, the stale override table) plus one overstatement.
**§9.1's instruction to treat every remaining claim in it as unverified is not
rhetorical — it keeps paying.**

⭐ **And one more, found in `ListFixes()` itself:** its output goes to the mod
log, not to the visible console, and nothing in the game's Lua bridges the two.
So *"console: `SMRFixPack.ListFixes()` **shows** them"* may be false as well.
It cannot be settled from source — both ends are engine functions with no Lua
body — so **`CAPTURE_SITTING.md`'s Pass F was rewritten as a one-minute check**
that settles it and drops its own shot if the answer is no. New hole 11.

---

## 3 · Job 4 — the specimens, tested by drafting five more

**Five entries prompt 1 did not use, two of them `fixed*`, one `wontfix`:**

| entry | outcome | needed the 4th beat? |
|---|---|---|
| `F15` (`fixed*`) — wisp research paid double | drafted | ✅ **yes** — the fix *reduces* the player's research, and half the defect is deliberately unshipped |
| `F59` (`fixed*`) — freed housing never woke the homeless | drafted | ✅ **yes** — the reservation half is deliberately not hooked |
| `F47` (`tested`) — track salvage refunded one hex's worth | drafted | ⛔ no — three beats, clean |
| `F18` (`fixed`) — Independence tech gave 10% not 20% | drafted | ✅ yes — the retroactive save fix needs its "only when it can identify the damage" qualifier, and putting that inside "After the fix" is exactly the hedge §5 warns about |
| `F42` (`wontfix`) — buildings placeable on dust devils | ⛔ **NO ENTRY — correctly** | n/a |

⭐ **The format survives.** But **3 of 4 needed the fourth beat**, on a sample
deliberately loaded with hard cases — so *"does 'Worth knowing' become a dumping
ground?"* is a live risk, and §5 currently gives prompt 4 no rule for when to use
it. ⇒ **Recommended addition, one line:** *the fourth beat is for something that
changes what the player should DO or EXPECT — never for extra detail about the
defect.* Under that rule `F47` and `F18` stay three-beat and the count falls.

⭐ **`F42` is a second `F76` in waiting**, and it validates §5.6 as written. Its
body contains a persuasive, publishable-sounding account of a real observation
that was then declined — the same shape as the `F76` draft, sitting in a
different file. §5.6's rule (*"never contains defects we investigated"*) is
tight enough to catch it, and the frozen file's own banner is a second
independent guard. **Nothing to change.**

### ⭐ The `F55` sweep — and it is good news for prompt 4's method

**The question §5.3 raised: how many of the 81 shipping F-entries have a title
that describes more than the module delivers?** Swept all 81.

⇒ **Nine, and every one of them is machine-detectable.** The marker is an
**asterisk on the status tag**: 8 entries carry `fixed*` in front matter (`F15`,
`F29`, `F34`, `F49`, `F55`, `F57`, `F58`, `F59`) and **`F52` carries `tested*` in
its heading tag while its front matter says plain `tested`** — so a sweep on
front matter alone misses it. Six of the nine have index titles that genuinely
over-promise; the rest are honest titles with an unshipped nicety behind them.

⇒ **What this means for prompt 4:** the design's rule (*write every blurb from
the entry body, never the index title*) is **kept** — but the risk is now
*scoped* rather than uniform. The nine asterisked entries need a careful body
read; the other 72 can be drafted from the body at normal speed without fearing a
hidden second half. ⛔ **`F52` must be added by hand to any list built from front
matter.**

### The two blurbs most likely to be wrong in the player's favour

* **§5.2 (`F102`) — ✅ holds.** Checked line by line against the entry: the
  "clean, unused sign" is the orphaned remaster entity; "nothing about the
  deposit changes" matches *"gameplay is class-keyed, both entities ship in
  vanilla, save carries nothing of ours"*; and the refusal to claim a cure is
  exactly the entry's *"CURE UNVERIFIED on affected hardware; ships
  disclaimered"*. ⚠️ **One word:** *"Reported on Linux with NVIDIA graphics"* —
  the entry says NVIDIA was **inferred** from the reporter's own DLSS setting,
  not stated. Say "reported on Linux" or mark the inference.
* **§5.1 (`F97`) — first three beats ✅ hold, fourth beat ⛔ refuted** (above).

---

## 4 · Job 1 — the architecture, attacked

**It holds.** Two findings, one of them worth acting on.

⭐ **The reader the split misses: the player whose game is broken and who
suspects us.** They arrive hostile and time-poor and want three things — *is it
you · how do I get you out · where do I report it*. §1's table has no row for
them, §3's 13-item inventory has no surface for them, and the one answer the
design does have for them (§6.1's *"How do I turn one fix off?"*) is the answer
§9.1 just refuted. ⛔ **Not designed here — adding surfaces is out of prompt 2's
scope.** Routed to the owner as **checklist 22c**, sized at ~1 agent hour, and
flagged for prompt 4.

⚖️ **§1's evaluator cell is half-wrong, and in the direction that costs us.** The
table gives the site "owns them" and the repo *"receipts and nothing else —
never linked as documentation"*. The "never linked as documentation" half is
right. But this project's evaluator — a modder, a forum replier — **goes to the
repo regardless of what we link**, and the README's own 2026-08-13 correction
says the public working notes are a *stronger* trust signal than a polished page.
⇒ **The site's job for the evaluator is to be a good index INTO the receipts,
not a substitute for them.** This is the design's clearest **under-claim**: the
receipts are the single most unusual asset the project has, and §1 files them as
a footnote.

⚖️ **The reframe is sound; one of its supports is not knowable.** *"The big
creators split docs off because the platform forces it"* is an inference about
other people's motives — a catalogue-shaped mod or plain SEO would produce the
same GitBook. ⛔ **The conclusion is unaffected**, because it rests on **our**
shape (81 defects is a database, and a database needs a query), not on theirs.
⇒ Keep the reframe, state the peer half as an inference.

✅ **"The store card owes the searcher one link and nothing else" — right**, and
§4.4's category-names move is what makes it survivable. A card that answers *is
my kind of problem in scope* has done the searcher's install-gating job; the rest
is the site's.

---

## 5 · Job 5 — exposure and player-hostility: **CLEAN**

* ✅ **No exposed-set count anywhere** in anything the design proposes to
  publish — checked the specimens, the save-safety skeleton, §4, §6 and §9.
* ✅ **Nothing generates player pages from `docs/`.** Both guards survived the
  site's move to its own repo, verified in `C:\Dev\SMR-CommunityMods`:
  `docs_dir: content` is intact and the workflow's exposure gate still fails the
  build on a changed `docs_dir`, a `../` escape, or an added submodule.
* ✅ **Rule 4 clean** across everything proposed for publication — the specimens,
  the tier-0 sentence and §9's bullets carry no path, id or house word. The
  design report cites them freely, which is correct for an agent doc.
* ⚠️ **One rule-4 leak path found and closed:** `CAPTURE_SITTING.md`'s shot names
  (`F13-before`, `F102-signs`) are `F##` ids one copy-paste away from becoming
  captions. The brief now says so explicitly.
* ⚠️ **A rule-4 tension prompt 3 must resolve, not inherit:** the rewritten
  per-fix disable paragraph is addressed to *modders* and is useless without an
  identifier — which rule 4 bars from player text. ⇒ **Move it off the store card
  to a "for modders" corner of the site**, where naming an identifier is
  appropriate to the reader. Do not try to write it identifier-free.

**§8B's sitting** — `EF-056` is stated correctly and prominently (byte-copy every
autosave first, re-list by name at close). ✅ **The two-restart ordering works**:
the rig's normal state is both mods ON, so restart 1 goes to mods-OFF for the
"before" frames and restart 2 back to mods-ON for everything else. ⚠️ **Its
fixture check was short by three** — `F14`'s pair needs a dome with genuinely low
colonist stats, `F19` needs graph history, and `optin-nohomeless-on` needs
jobseekers. All three amended into the brief, with `F13` named as the pair to
fall back on. **No shot asks the owner to build colony state.**

---

## 6 · Job 6 — sizing and sequencing

✅ **The 8–12 h estimate for item 5 is credible.** Timing my own five drafts and
extrapolating honestly: ~4 min per plain entry × 72 + ~18 min per asterisked
entry × 9 ≈ **8 h**, plus categorisation, the search-title rewrite pass and
cross-checks ⇒ **8–10 h**. Slightly optimistic at the low end, and it assumes no
per-entry play verification — which the frozen ship line means there isn't.

✅ **Release sequencing respected.** MOD_DESCRIPTION stays item ③; this chain
makes ③ assembly rather than authoring. ✅ **The freeze is not lifted anywhere** —
§3 splits the file, §5.6 quarantines its bad blocks.

⚠️ **The D13 seam has one hole: the sentence about what the player SEES after
uninstalling.** `STATE.md` records that one **engine** savegame mod-reference
line survives an uninstall (both packs, self-clears on the next save) and routes
it explicitly *"→ uninstall text"* — i.e. a sentence prompt 3 owes. §8 never
mentions it, because §8 was written without reading `D13.md`. ⇒ **Prompt 3 must
write it and it is safe to write now:** the trace is the engine's own, not ours,
and it clears itself. Everything else in §8 is operational.

---

## 7 · Job 7 — the routed decisions

* **21 (topology)** ✅ acted on correctly. Site is its own repo, both copies gone
  from here, guards intact.
* **22 (judgment-calls wording)** ✅ acted on — ⛔ **but see 22b.**
* **23 (`ignore_files`)** ✅ recorded on `WORKFLOW.md`'s release steps.
  ⭐ **Re-derived per mod, which nobody had done for the third one:**

  | mod | unfiltered today |
  |---|---|
  | fix pack | `tools/` · `CLAUDE.md` · `LICENSE` · `.gitattributes` |
  | opt-in pack | the same four |
  | **save rescue** | **`LICENSE` only** — its `metadata.lua` already carries a `*CLAUDE.md` pattern the other two lack, and it has no `tools/` and no `.gitattributes` |

  ⭐ **`.github/` has left the building** — the fix pack has none since the site
  moved, so that half of the question is moot rather than unverified.
  ⚠️ **The rescue mod's extra pattern is the fix the other two want** — copy it
  rather than inventing one.
* **24 (preview art)** ✅ and the brief is audited and amended (§5 above).
* **25 (roster wording)** ✅ **verified byte-clean.** The diff is the heading, the
  two words, and an explanatory parenthetical. **No assessment was softened.**

### ⭐ The process question, answered

**Nothing was routed that prompt 1 should have decided.** All five were genuine
owner calls — three about other people (the roster, the art, the site's public
address) and two about tone.

⛔ **But something was DECIDED that should have been checked, twice, in the same
way.** The console-veto line and the dust-devil scale word both reached the owner
as *wording* with their evidence left behind, and both were factually wrong. The
owner caught the first from play instinct. **Nobody caught the second, because it
sounded like the phrasing that had already been approved.**

⇒ **The standing instruction to add to §9.1's, and the real finding of this
review:** *route a decision with the evidence attached, not just the wording.*
A bullet that says *"on the heaviest settings"* is unfalsifiable to the reader;
the same bullet with its rate table beside it is decided in ten seconds. That is
a cheap change and it is the only one that would have caught this.

---

## 8 · The corrections landed by prompt 2

* `PUBLIC_DOCS_DESIGN.md` — §5.1 refutation + table · §9 bullet-5 correction
  routed as 22b · §9.1 corrected with the per-module table · §12 holes 4 and 7
  closed, hole 9 widened, **hole 11 added**.
* `CAPTURE_SITTING.md` — fixture list corrected (3 shots added) · Pass C gains a
  free measurement that closes hole 4's play half · **Pass F rewritten as a check
  before it is a capture** · caption rule against `F##` shot names.
* `STATE.md` — the requested line landed, re-derived (⑤; **four repos plus the
  shared TestKit**; counts re-emitted).
* `PLAYTEST_CHECKLIST.md` — **22b** (the scale word, needs one owner line) and
  **22c** (the missing reader, needs a yes/no).
* `WORKFLOW.md` — item 23's release step now carries the per-mod list.
* Site repo `content/install.md` — the toggle-restart banner replaced with the
  derived answer; the mod-restart line left alone, because it is correct.

## 9 · Open holes handed to prompts 3 and 4

1. **The rescue artifact's name, link and publish status** — release-time owner
   call ("build ≠ publish").
2. **The uninstall-cleanliness sentence** — Reading A or B, owner, at launch.
3. **Load order** — still no measured answer. Prompt 4 derives one or says so.
5. **Per-fix "why isn't X fixed"** — needs each of the 11 `wontfix` entries read.
8. **Store links** — do not exist until upload.
10. **Preview art** — floor is queued, unbounded tail.
11. ⭐ **Does `ListFixes()` show anything on screen?** — one minute of the capture
    sitting. ⛔ Two of our sentences assume yes.

⭐ **Closed by prompt 2:** hole 4 (the restart question) and hole 7 (`.github/`,
now moot; one narrower wildcard question recorded with a one-command way to
settle it at packaging time).
