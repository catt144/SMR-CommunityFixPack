# Manual Playtest Checklist — Relaunched Fix Pack

**Who this is for:** the project owner, playing the real retail game **with a
live agent session alongside**. This file is the work list and nothing else:
what to test, how to set it up, what each test needs. Expectations,
predictions, pass/fail readings and console forensics are NOT written here —
the agent supplies them in the sitting, from each test's linked entry.
Reference material (ground rules, console facts, the verified command table,
Test Kit helpers, save fixtures) stays in [PLAYTEST_HELP.md](PLAYTEST_HELP.md);
completed tests move whole to
[PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) — 44 sections as of
2026-08-01, plus the 2026-08-03 pre-redesign snapshot.

> Redesigned 2026-08-03 (`docs/agent/prompts/PT_REDESIGN_PROMPT.md`, owner
> design authority of the same date): tests grouped **by system, not by PT
> number** — a sitting clears a group — and each test reduced to
> **Bug / Requirements / Setup / Good to have** (Requirements: the at-a-glance
> save/colony line, owner amendment at the checkpoint). PT codes are unchanged;
> numbering is identity, grouping is order. The full pre-redesign text,
> recorded results included, is in the archive under the "pre-redesign
> snapshot 2026-08-03" banner.

> ✅✅ **The 2026-08-11 "BOTH TICKS DONE" block (Mod-Manager re-enable + Steam
> Cloud untick) is CLOSED and moved WHOLE to `archive/PLAYTEST_ARCHIVE.md`.**
> The audit confirmed the second tick stuck: **two** post-untick launches
> restored nothing, every directory change reconciles by name (59 saves, all
> named, none of the 14 strays back), and the "never say gone" rule is formally
> retired. Nothing here is owed from you.

## Decisions waiting on you

### 2026-09-01 — ITEMS 88–90 OPEN: raised by the OPT-IN mod's contamination audit (its repo, `docs/agent/reports/CONTAMINATION_AUDIT_20260901.md`)

90. **Does your 2026-08-02 loc-table ruling extend to the opt-in mod?** You ruled
    (this repo's `FIX_POLICY` §6) that *the pack* WILL ship its own `ModItemLocTable`
    translations post-release — twelve days before the split, about THIS mod. The
    opt-in mod has 17 `Untranslated(` sites (rollover titles, policy rows, the
    stand-down dialog) and its `FUTURE_IDEAS.md` #4(b) hangs on the answer. Say
    "both", "fix pack only", or "decide at its launch".

89. **Opt-in `Code/`: allow a comment-only wording sweep?** Five comments still speak
    the donor's terms — "the pack" meaning the opt-in mod itself
    (`00_Core.lua:497`, `:536`, `:558`, `Opt_ResidencyControl.lua:63`) and one that
    points players' FAQ guidance at THIS repo's frozen `MOD_DESCRIPTION.md`
    (`Opt_NoHomeless.lua:319`). Zero behaviour change, parse sweep after; but it is a
    module-file edit, so it is yours. Say "sweep" or "leave as history".

88. **`FUTURE_IDEAS.md` #9 ("Per-fix player toggles for the FIX PACK") is parked in
    the OPT-IN repo with no ruling of its own.** Your 2026-08-14 move order covered
    "anything that's possible opt ins"; #9 is a fix-pack feature (a Mod Options page
    for THIS mod's fixes), routed there by analogy to #5. It also carries a stale
    release rider ("confirm `MOD_DESCRIPTION.md` no longer says 'in the console'")
    and cites a prompt that no longer exists (`COVERAGE_SWEEP_SMRCF.md`). Say "keep
    there", "move to this repo's `FUTURE_IDEAS.md`", or "delete".


### ✅ 2026-08-31 — ITEM 87 RULED THE SAME DAY: drones UNFROZEN

87. ✅ **RULED 2026-08-31 — "Un freeze drones" (verbatim).** Lifts the PT-52
    freeze and the module freeze on the opt-in mod's `Opt_DroneOverhaul` (D06)
    and `Opt_DroneStatDials` (D09): design and playtest work may resume under
    FIX_POLICY with an A/B per change. Recorded in the opt-in repo's `STATE.md`
    and `D06.md`; PT-52's status below updated. Still yours: the D06 design
    decision itself (`prompts/DRONE_PROJECT_PROMPT.md` §3 — three options), and
    whether `FUTURE_IDEAS.md` #7 (gleaner / pairing policy) is un-parked too — this
    ruling was read as NOT touching that post-launch parking.

### 2026-08-31 — ITEMS 83–86 OPEN: raised by the OPT-IN mod's readiness pass (its repo, `docs/agent/reports/READINESS_REVIEW_0831.md`)

86. **Ratify or reverse: `EF-###` ids are allocated by THIS repo.** After the split
    both repos minted their own numbers and collided (the opt-in repo's `EF-057`/`058`
    of 08-16 were different facts from ours). Resolved 08-31 by re-syncing its facts
    folder from ours @ `bec2e06`; the rule written into its `WORKFLOW.md`: a fact
    learned there is filed HERE first (or its next id reserved here), then mirrored
    there at the same id. Costs you nothing; say "reverse" if you want independent
    numbering with a prefix instead.

85. **Preview art for the opt-in mod (owner task).** `tools/upload_preflight.py`
    run against `C:\Dev\SMR-OptInPack` FAILS on exactly one clause: no `image` /
    `preview.png` — Paradox rejects before packing (`ParadoxMods.lua:39`). Same
    limits as ours (≤1 MB Steam / ≤2 MB PDX). Not urgent — that mod is not launching —
    but it is the only mechanical FAIL between it and an upload sitting.

84. **Opt-in: name three wrap pairs in `Require` blocks?** The F107 check (now run by
    its doccheck) found three capture+install sites with no Require pair:
    `Opt_DroneOverhaul` → `Drone.CleanUnreachables` + `TaskRequestHub.FindTask` (that
    module uses inline guards, no `Require` at all) and `Opt_MultipleSuns` →
    `SolarPanelBase.GameInit`. Each captured class DECLARES the method at Src
    (Drone.lua:879, _TaskRequest.lua:72, SolarPanel.lua:8), so `prev` is real and
    nothing is broken — they are allowlisted with those citations. The tidy fix is a
    code edit to frozen modules (`DroneOverhaul` carries PT-52's freeze) and needs an
    A/B. **Options:** (a) leave allowlisted until the next planned edit of each file;
    (b) do it at the opt-in launch session with its boot check. Recommend (a).

83. **TestKit edits for the opt-in mod's coverage (needs your go — it is the SHARED
    kit).** Survey findings (`READINESS_REVIEW_0831.md` §5): the kit has **no opt-in-only
    run mode** (a standalone leg prints ~85 fix-pack FAILs around 8 real verdicts);
    **D06 `DroneOverhaul` has no `RunAll` probe** (only the manual stress harness);
    `98_EnablePathLeg.lua:54` hardcodes `SMR_CommunityFixPack`, so the opt-in mod's
    normal first-run path has never been measured by that leg; `99_FixtureCarry.lua`
    channel 5 hardcodes `SMRFixPack_F35_` and cannot see D09's dial modifiers; only
    D12 has a vanilla-control clause (the 08-24 probe rule). **Proposed, in order of
    value:** (1) `RunAll` owner filter + a `fix pack absent = expected` mode;
    (2) `PACK_ID` parameter on the enable-path leg; (3) FixtureCarry D09 channel;
    (4) a D06 `RunAll` probe; (5) control clauses for D01–D04/D07/D09. Each needs a
    real launch to verify; none was made. Say which, or "all, next sitting".


### ✅ 2026-08-30 — ITEM 82 CLOSED: F110 live on both stores in v5, site deployed, delivered Steam pack verified. Nothing owed.

82. ✅ **SHIPPED — v5, both portals, 2026-08-30.** You packed and uploaded Paradox
    then Steam; you told me the store pages look good. The tree now reads `version 5`
    (up one from 4); `pdx_id`/`steam_id` unchanged and written back (Paradox rev
    `pdx_version` "4"). The release words are live: the card count moved
    **Eighty-one → Eighty-two repairs** on both store bodies, F110's change note is
    the version's changelog entry, and a headliner bullet ("A Jumbo Cave mystery
    could get stuck clearing waste rock and never complete") is on the card.

    ✅ **SITE DEPLOYED** — you ran Publish; newest run `ce3a3779` (== site HEAD),
    status success, **82** live fix-list entries. The store "Eighty-two" now matches
    the page it links to; count constraint closed.

    ✅ **Both questions answered 08-30.** **(1) Auto-fill did NOT deliver a clean
    page** — you pasted the `UPLOAD_WORKFLOW.md` §3 backup by hand. So after two
    upload cycles the auto-fill path has never once stood on its own: the §3 paste
    backups are the real delivery mechanism, **required and kept current**, not an
    optional fallback. You're treating the pasted plain text as a placeholder and
    will apply the headings/bold formatting later — cosmetic, no rush.
    **(2) No required-game-version field** was offered on either page — nothing to
    set, nothing owed.

    ✅ **DELIVERED PACK VERIFIED** (§0.5(f)) — your subscribed Steam copy downloaded
    to `steamapps/workshop/content/**3215050**/3787202810/ModContent.fpk` (Relaunched
    is app 3215050, not 464920). Read with `tools/pack_list.py`: **85 entries**
    (== `pack_predict`), **83 byte-identical** to the tree; the only 2 that differ are
    `metadata.lua` + `items.lua` (the forced-save comment strip, same as v4's 84/82).
    Extracted `metadata.lua` confirms `version 5`, count word **"Eighty-two repairs"**,
    the F110 change note, and `Fix_JumboCaveReinforcementWedge` in the code list.
    **md5 `a1cbaad6294382068250ef390037f239`, 401,188 B.** First delivered md5 this
    project has ever computed from a real portal artifact.

<details><summary>the attended-fix receipt (08-30, for the record)</summary>

    ✅ You decided to fix it, the module was written, and the attended A/B passed: on
    the re-loaded still-stuck `International Mars Mission Sol 84` the module's own
    control line fired —
    `[CommunityFixPack] JumboCaveReinforcementWedge: force-cleared 1 unreachable waste rock(s) …`
    — and the mystery auto-completed. Confound ruled out: your material cheat only
    supplied build resources (needed to *build*, not to *clear*) and you didn't
    finish-construct; the clearing is the fix's, by its own log line. `F110` flipped
    to `fixed`; log archived (`archive/f110_attended_…16.41.16.log`). One same-day
    hiccup handled: the first build required `Cities` at menu time and self-disabled
    (the dialog you saw) — Require trimmed, applied clean on the next boot.

</details>

<details><summary>original decision text (for the record)</summary>

**Confirmed, first time ever.** A Reddit reporter's save (you bought the
    Interplanetary Codex pass to load it) reproduced the month-old Jumbo Cave
    wedge on our exact build. Console read while stuck: a `JumboCaveReinforcementStructure`
    site down to its last waste rock, that rock a `WasteRockObstructor` the drones
    can't path to (in 2 drones' `unreachable_buildings`), site never clears, mystery
    soft-locks. Permanence witnessed (the unreachable flag reset on load, then
    rebuilt after ~1-2 min of run). Filed as **`F110`**; C25 is closed-promoted.

    **The decision is yours — three parts, and none is urgent:**
    - **Fix or leave?** It's a genuine soft-lock with no player recourse, which
      `FIX_POLICY` normally favours fixing — but it's niche (needs a Jumbo Cave
      *and* the geometry to strand a rock). **Rec: fix, in a future patch, not a
      hotfix.**
    - **Shape?** fredware's known repair is *reactive* (wrap the vanilla approach,
      act after a failure). A *proactive* shape would need the finer root cause
      first — WHY `Rocks_04` is unreachable (terrain vs a cleared pile vs an
      adjacent obstacle), which I did **not** measure. **Rec: characterise the
      geometry on the loaded save before choosing a shape.**
    - **Timing?** Post-launch = patch-note maintenance (your ruling); this rides a
      future patch, not its own cycle. No gate re-run for one added fix.

    ⇒ **Say the word and I'll (a) take the geometry read off the still-loaded save,
    then (b) bring you an A/B fix proposal.** Nothing is owed until you decide.

</details>

### ✅ 2026-08-29 — ITEM 81 DONE, you ran it 18:44Z and the site is fully deployed. ITEM 80 WITHDRAWN IN FULL, both halves. Nothing is owed on the site or either store.

81. ✅ **DONE — deployed `fcb2aa9`, status `success`, 2026-08-29T18:44:14Z.**
    Verified on three controls: the deployments API, the live index page (now
    reads *"six fixes are judgment calls"*), and `git log fcb2aa9..HEAD` in the
    site repo, which is **empty — every commit is now public.** Live fix list
    still 81 entries. Was: index.md said **five**, the FAQ said **six**, twice.

    The repo is already right: `fcb2aa9` corrects index.md, and it is the **only**
    commit not deployed. The two edits landed in *different* commits (`7f4bb78`
    did the FAQ, `fcb2aa9` did index.md), so deploying one and not the other left
    the public site disagreeing with itself while the repo looked consistent.

    ⇒ **one run of *Actions → Publish docs site*** on `SMR-CommunityMods` clears
    it. Low severity — nobody is misled about what the pack does — but it is the
    kind of thing a reader notices and it costs a minute.

80. ⛔ **WITHDRAWN IN FULL — both halves were wrong, and the fault was mine.**

    **(a) Steam.** I said the Steam listing had neither F105 nor F108. It had
    both. You refuted it with the Workshop change-notes page and by subscribing;
    the delivered archive settles it — 84 entries, 82 byte-identical to our tree,
    both fix modules present, packed `version` 4. I had argued from the version
    number, and `RELEASE_PORTAL_PREP.md` §0.5(c) describes a **first** upload in
    the sentence I was quoting. Recorded as `EF-068`.

    **(b) The count.** I said both stores claimed "Eighty-one repairs" while the
    site backed only 79, and called it a live falsifiable claim. **It is backed.**
    You deployed the site on 08-24 *and* 08-28; the live deployment is `7f4bb78`,
    status `success`, and it carries **81** fix-list entries. The live page itself
    renders 81. Two independent controls agree.

    **What I did wrong, both times: I read a record instead of taking a reading.**
    STATE said "deployed `a97b8b0` = 79 entries", true when written on 08-21, and
    I repeated it twice as current without checking. The deployments API answers
    it in one call and I only ran it while writing the audit prompt — which is
    precisely why that prompt now opens with it as §1.

    ⇒ **item 79 is DONE** (see below), and nothing is owed on either store.

### ✅ 2026-08-24 — ITEM 79 IS DONE. You ran it on 08-24 and again on 08-28; verified 2026-08-29 against the deployments API. The original text is kept below as the record.

79. ✅ **DONE — deployed `7f4bb78`, status `success`, 2026-08-28T22:25:18Z, carrying
    81 fix-list entries.** The gap this item was written against is closed. ⚠️ One
    later commit (`fcb2aa9`) is still undeployed — that is item 81, not this.

    <details><summary>The original item, kept for the record</summary>

    ⚠️ **Run *Actions → Publish docs site → Run workflow* on `SMR-CommunityMods`.**
    Everything is committed and pushed; **none of it is public.** The publish
    workflow is `workflow_dispatch`-only **on purpose** — publishing is your act,
    public-docs chain rule 5 — so the F105 entry has been sitting live-invisible
    since it was written.

    | | commit | fix-list entries |
    |---|---|---|
    | **what players see now** | `a97b8b0` (deployed 08-21) | **79** |
    | what the repo holds | `abe46c9` | **80** |

    Counted from the deployed commit locally, not off the web page.

    ⛔ **Why the order matters:** the store cards say **"Eighty repairs"**, and the
    only reason we allow a count on a store page at all is that the reader can
    check it on the page the card links to. Paste the cards first and the very
    first person who counts finds seventy-nine. **Deploy, then paste.**

    ✅ Nothing else about the site is owed — Pages is on, the store links are in
    the pages, the card carries the site links, and no FILL-IN markers remain.
    This is one button, and it costs you about a minute.

    </details>

### ⛔ 2026-08-24 — ITEM 78 IS WITHDRAWN. I asked you to decide something you had already done, on a tool reading that was wrong. Both reporters are answered. Nothing is owed.

78. ⛔ **WITHDRAWN — the finding was false and the fault was mine.** I reported
    that issue #1 was closed with **zero comments** and that Keelai had been left
    without any answer, and asked you to choose between reopening, commenting, or
    leaving it silent. **None of that was real.** You had already posted the reply
    and closed it, and Keelai had already thanked you.

    **What actually happened**, from the API, which I should have used first:

    | issue | what is on the thread | reporter's last word |
    |---|---|---|
    | **#1** F104 | Draft A posted 03:40Z; closed 06:01Z `completed` | *"Yeah i had a hunch that mod might be the problem but thanks for checking :)"* |
    | **#2** F105 | you asked for the save/store at 01:57Z, then posted a full explanation at 06:04Z | *"Nice and thanks :) ill try and include both save and log in the future"* |

    **The mistake, plainly:** I read the issue's web page instead of the API. It
    returned "no comments" three times — including once with a cache-busting URL
    — and I treated three agreeing reads as confirmation when they were the same
    broken method three times. The comment **count** was one field away in the
    issues list and would have caught it instantly. That control is now written
    into `agent/prompts/PUBLIC_SURFACE_SWEEP.md` §4 and the reply record, and
    `F104` carries the correction in its own entry rather than quietly reading
    right.

    ✅ **F104 is now `closed`** — its stated gate was a reply *plus* the
    reporter's confirmation, and both are on the thread.

    ⭐ **Two things genuinely came out of this, and they are the only parts worth
    your attention.** Your #2 reply was written hours *before* the rig legs ran,
    so four of its sentences are stronger than what we can now back. The reporter
    is satisfied and **nothing needs correcting on the thread** — but these must
    not migrate onto the fix list, a store card or `last_changes`, where there is
    no goodwill to spend and no thread to correct them in:

    * ⛔ *"it also **repairs saves** that already have a levelling job in the
      broken state"* — we don't repair; the site stays broken and the guard makes
      it harmless. The outcome you promised is right and leg D proves it (nothing
      to demolish); the mechanism isn't. Wording that holds: **"stops it happening
      on a save it's already happening in."**
    * ⚠️ *"**only three** technologies carry the effect"* — true of the label
      sweep; a second reader route (`OnMsg.ConstructionCostChanged`) was never
      ruled out. The guard covers both, so the fix claim is fine — it's the
      *"only"* that's wider than the evidence.
    * ⚠️ *"quietly to the log with **no warning box**"* — we measured `Mod
      Flagged` = 0 with the pack off, which supports it; nobody ever *watched* a
      screen to confirm the box is absent.
    * ⚠️ *"happens with **no mods installed at all**"* — derived at source, and
      every pack-off leg still had the rig's other junctions loaded.

    **Nothing here needs an answer from you.** If you want one thing when 1.0.x
    goes live, a one-line *"this is out now"* on #2 would close it warmly — pure
    courtesy, not a debt.

### ✅ 2026-08-24 — RULED AND APPLIED. The hazard is reworded; nothing blocks the update but your sitting.

75. ✅ **RULED 2026-08-24, in-session, and APPLIED the same hour.** Your words:
    *"if we have open bug reports and we are preparing a patch that should be
    assumed we are off a freeze."* ⭐ **That is a better rule than the one I
    drafted**, and it names what was actually wrong with `H-02`: it was written
    as a *state* ("frozen at 1.0.0") when it should have been about *who and
    how*. A freeze that survives into a patch cycle blocks the thing the pack
    exists to do.
    **`H-02` now reads:** the version is the **sitting's** to set, never an
    agent's and never by hand; open field reports plus a patch in preparation
    means a patch cycle and **no freeze is assumed**.
    ⛔ **What I kept, because it is mechanical rather than policy** — an agent
    never opens the Mod Editor (every save runs `version = version + 1`,
    `Mod.lua:967`, and `ValidateModBeforeUpload` force-saves a dirty mod), and an
    agent never hand-sets the version numbers, because the sitting bumps
    automatically and a hand-set value on top **double-bumps** and widens the
    portal gap item 71 says never to chase.
    ✅ Every other hand edit to `metadata.lua` — the `code` list, `last_changes`,
    descriptions — is ordinary agent work and always was.
    ⚠️ **One thing left before the sitting, and it is mine:** `last_changes` still
    says `"Initial release."` That string ships inside the mod and is the patch
    note players read. It is a text-only hand edit, no bump — say go and it is
    two minutes.

    <details><summary>The original item, kept for the record</summary>

    ⛔ **`H-02` forbids the 1.0.x update as written. It needs your ruling before
    any agent can prepare the upload.**
    The hazard reads *"`metadata.lua` is FROZEN at 1.0.0 — no version bump, no Mod
    Editor save."* It existed to protect the 1.0.0 upload from an accidental bump.
    **A real update requires exactly that bump**, so as written it blocks the thing
    it was never meant to block. An agent obeying STATE will refuse; an agent
    ignoring a hazard is worse. ⇒ **Rule it, don't leave it ambiguous.**
    ❓ **The call:** does `H-02` become *"frozen except at an owner-run upload
    sitting"*, or is it discharged like `H-04` was and replaced by a successor
    that guards the same accident? ⚖️ I'd take the first — the accident it
    prevents (a stray editor save silently bumping the version between sittings)
    is still real between updates.

    ℹ️ **Everything else about the deploy is already written down and needs no
    decision from you** — this item exists only because a hazard cannot be lifted
    by an agent. The sequence, the two-portal version mechanics, and the three
    checks still owed from the *first* upload are in
    [agent/reports/RELEASE_PORTAL_PREP.md](agent/reports/RELEASE_PORTAL_PREP.md)
    §0.5(c)(d)(f) and §1; the pack route is Mods Manager → Edit (`Ctrl-E`) →
    File → Pack Mod (⛔ the console is not a route).
    ⚠️ **Item 74 comes first** — it decides whether the module you are uploading
    is the repaired one.
    ✅ **Item 74 is now done (ruled (a), built — item 76), so 75 is the only
    thing between the tree and the upload.**

    ℹ️ **Drafted so this is a yes/no, not a writing task.** If you take the
    reword, `H-02` in [agent/STATE.md](agent/STATE.md) becomes, verbatim:
    > **H-02** `metadata.lua` is **FROZEN between sittings** — no version bump,
    > no Mod Editor save, ever, EXCEPT inside an owner-run upload sitting, where
    > the bump is the point (every editor save runs `version = version + 1`,
    > `Mod.lua:967`). ⛔ The accident this still prevents is a stray editor save
    > silently bumping the version while no upload is happening, which desyncs
    > the two portals further (checklist 71). An agent may never open the editor;
    > only the owner, at a sitting, and the sitting ends the exemption.
    ⛔ **An agent cannot apply this** — it is your ruling to make, which is the
    whole reason this item exists. Say the word and it lands in one edit.

    </details>

    ⚠️ **Unrelated, and it needs your hands too — the reporter's GitHub issue
    numbers were never captured.** F104 and F105 both cite "GitHub, Keelai" with
    no issue number, so neither entry can be found from the issue or vice versa,
    and F105's issue is titled something like *"Error when completing
    milestone"* while our entry is titled after the cause — the two do not match
    by search. Paste the two numbers/URLs and they go into the entries' front
    matter.

### ⭐⭐ 2026-08-24 — F105 IS FIXED ON YOUR WORD, AND BUILDING IT EXPOSED A NEW QUESTION. One receipt, one call.

**The receipt (item 72 — RULED by you, in-session: "This is a number 1 fix
priority").** `Fix_LandscapeCostRefresh` is built, registered, and boot-verified
the same session: `[CommunityFixPack] LandscapeCostRefresh: applied`, zero error
lines, menu-only leg, no save touched (log
`docs/archive/f105_Mars.exe-20260824-00.08.38.log`; PROBE SWEEP: clean). The
investigation also **corrected two things the filed entry believed**: the
Efficiency laws are NOT triggers (only three techs are — NeoConcrete,
DomeStreamlining, MarsNoveau), and `ClearWasteRockConstructionSite` (plain
rock-clearing jobs) crashes the same way, not just levelling.
→ [agent/bugs/F105.md](agent/bugs/F105.md) · report `agent/reports/F105_INVESTIGATION.md`
**Three things to know, none urgent:**
* ⚠️ **The live listings are now one module behind this tree** (78 modules vs
  the shipped 77). Whenever you want it live, it is the normal update sitting:
  editor save (bumps the version), pack, upload — both portals. Nothing else is
  queued behind it.
* `metadata.lua` gained ONE hand-written `code` row (the new module), version
  untouched — no editor save happened, so H-02 held.
* ⛔ Still never reproduced on the rig. The 10-minute repro (place a levelling
  site, research a dome-cost tech, watch `ConstructionSite.lua:673` stay
  silent) rides your next sitting if you want the attended upgrade.

### ⭐⭐⭐ 2026-08-24 — F105 IS REPRODUCED ON OUR OWN RIG, AND THE FIX WAS WATCHED TO STOP IT. Nothing is owed; this is a receipt.

77. ⭐⭐ **The one thing every F105 document said had never been done, is done —
    and you did it in about twenty minutes.** Until today the whole of F105 was
    read off the shipped Lua against a stranger's log. Now:
    * **Leg A, pack OFF — the defect fires. 14 raises of
      `ConstructionSite.lua:673`** (`docs/archive/f105_legA_Mars.exe-20260824-15.28.06.log`,
      lines 147-388). A real Flatten job, worked by real drones to
      `state = clean` with a live WasteRock request, **state verified at the
      console before firing rather than assumed**, then a cost tech researched.
    * **Leg B, pack ON — it does not.** Zero `:673` in the entire session
      (`f105_legB_Mars.exe-20260824-16.07.29.log`), with a landscape site active
      and **Mars Nouveau researched** — which you confirmed on the tech screen.
    ⭐ **Your mid-leg re-tick covered a third thing for free.** Enabling the pack
    on an already-running process is the `F87` **enable path** — presets loaded,
    classes not yet built — which `FIX_POLICY` §2 calls "every player's first
    run". The unattended harness leg was a cold boot; both paths are now covered
    for this module.
    ⭐ **A third pack-OFF leg (leg C) came in after the write-up and CORRECTED
    the write-up.** `f105_legC_*.log`: 12 raises, and `[CommunityFixPack]` appears
    **zero** times — the cleanest control of the three, no re-tick to explain.
    ⛔ **It also refuted something I had just told you.** I wrote that the console's
    `pcall` meant the raise "never reached the engine's uncaught handler". Wrong:
    every raise is logged **twice**, adjacent — 6 uncaught `[LUA ERROR]` plus 6
    console-caught in leg C, and 7 + 7 in leg A when I went back and counted.
    ⭐ **Which makes item 73 cheaper than I told you.** The thing that has never
    fired is not the uncaught path — it is `ReportModLuaError`. `Mod Flagged` is
    zero in all three legs simply because with the pack OFF there is no mod name
    in the stack to match. So seeing the real player popup needs **pack ON with
    this one module disabled** — no console trickery required, and the uncaught
    path is already measured firing.
    ⭐⭐ **And a fourth leg you designed, which is the one that matters to players.**
    You saved *after* the defect had fired (`Post 105-dirty`), ticked the pack on,
    fully exited, relaunched and loaded it — the exact position of someone who hits
    this bug and *then* installs the pack. **Applied, zero errors.**
    ⇒ **A player does not need a clean save.** They can hit F105, install the pack
    afterwards, and carry on in the same colony. That is measured evidence for the
    store page's "safe to add to a save you have already played" — for this defect.
    ⛔ I tried to caveat that the guard might not have been *called* during that
    load; **you were right that this is semantics against effect** and I dropped it.
    The wrap is a permanent shield on the reader, so called-or-not it is installed
    for every later call and no future trigger can raise while the pack is on.
    ⛔ Still not a repair: the site stays broken and the guard makes it harmless, so
    uninstalling brings the defect back — which is what the store text already says.
    ⭐ It also settles **item 72**'s shape question with a measurement instead of an
    argument: shape (b), initialising the writer, could never have helped that save,
    because the gatherer ran long before it existed. Only guarding the reader does.
    → [agent/bugs/F105.md](agent/bugs/F105.md), section "THE FIELD ROUTE, REPRODUCED"
    ℹ️ ⚠️ One loose thread I am not dropping: leg A's log line 107,
    `Unpersist missing permanent: Mod/SMR_CommunityFixPack`. It is what PROVED
    the pack was off — but it also says a save carries a persisted reference to
    our code, and `FIX_POLICY` §3a's posture is that it should not. Filed for a
    look after the upload; nothing about it blocks anything.

### ⭐ 2026-08-24 — F107 IS REPAIRED. One module, one wrap, doccheck green — and one thing to check I read you right.

76. ✅ **BUILT on your item-74 (a), same session — `Fix_LandscapeCostRefresh`
    now installs ONE chained wrap on `ConstructionSite` instead of three on the
    landscape leaves.** `prev` is the real function (`ConstructionSite` is the
    only class in the tree that declares `RefreshConstructionResources`,
    `ConstructionSite.lua:665`), so the delegation half is live code again.
    → [agent/bugs/F107.md](agent/bugs/F107.md) (`built`) · `Code/Fix_LandscapeCostRefresh.lua`
    * **The `Require` block already named the pair we now install on**, which is
      what `FIX_POLICY` §2 asks for — so the three F107 rows are **deleted** from
      `tools/harvest_wrap_targets.py`'s allowlist rather than kept. `WRAP CHECK:
      0 wrap site(s) outside Require, 5 allowlisted`. doccheck **GREEN**.
    * **The widening was re-verified at Src by this session, independently**, not
      taken on the audit's word: `GatherConstructionResources` creates
      `construction_resources` and `construction_costs_at_start` together
      (`:639-640`), both class defaults are `false` (`:13`, `:32`), so the only
      ordinary-site state where the widened guard fires is the ungathered one —
      where vanilla's own body raises at `:670`. Same verdict: it can only ever
      prevent an error. That derivation is now in the module header.
    * **The header's refuted F106 premise and the banned `classes.lua:986-988`
      citation are gone**, replaced by the measured file-load ordering; the
      `Track.lua:651` "only writer" precision is in too.
    ✅ **VERIFIED ON THE RIG 2026-08-24, unattended — F107 is `fixed`, not
    `built`.** You launched; the TestKit autorun harness did the rest (boot ->
    generate a map -> start a colony -> all 100 probes -> quit itself). Log
    `docs/archive/f107_Mars.exe-20260824-13.07.00.log`.
    * **Suite `76 PASS / 0 FAIL / 24 SKIP / 0 ERROR` of 100**, gate `78/78
      applied`, `[SMRAUTO] BEGIN..END` clean. The previous leg was `75/1/24/0`
      and that single FAIL was this probe.
    * ⭐ **Clause 1 stayed PASS on all three leaves** — that is the half that
      mattered. A repair that traded one defect for another would show clause 1
      broken, and nothing else in the suite checks it.
    * ⭐ **The dispatch sweep agreed independently of the probe**: the three
      leaves went from `UNREACHED=3 (own-copy 3)` — unreached because the module
      had overwritten them itself — to `UNREACHED=0`, reach 5 -> 8. Sweep total
      `clean=97` -> **`98`**. That is the inheritance mechanism measured without
      reference to the probe's verdict.
    * ⭐ **The widening you ruled in is no longer a reading.** Clause 3 ran on
      `ConstructionSite` itself: ungathered `ok=true` (where vanilla raises at
      `:670`), gathered `ok=true set_to=90 start_cost=50` (delegated identically
      to vanilla). Two static derivations had agreed on that; now it has run.
    * **Zero unexplained error lines.** The `Flight.lua:465/:479` asserts in the
      log are the known synthetic-map ones, present in the control leg too.
    ⛔ **Still NOT established, and no run so far touches it:** the field route —
    a levelling site on a real map plus a `*_Construction` cost tech. F105 has
    never been reproduced end to end. That is unchanged by this leg and rides
    your next organic sitting if you want it.
    ❓ **One thing still open: I read your "I'd take (a)" as the ruling and
    built it.** If that was a leaning rather than a decision, say so — it is one
    `git revert`, though the tree is now measured green on it.

74. ✅ **MEASURED AND ANSWERED 2026-08-24 — and the answer is the opposite of
    the question. It cost you nothing: the run was unattended.**
    **The good news first: nothing was broken by the mechanism I was worried
    about.** I filed F106 saying that most of our ~60 fixes might be silent
    no-ops, because the game copies inherited methods into each subclass before
    our code could patch them. **That was wrong, and it is now measured wrong.**
    Our fixes are applied *earlier* in the boot than I believed — before the game
    builds its classes, not after — so the game copies **our** patched version
    down into every subclass. `Fix_SmallLandscapeSites` (F33) is fine and always
    was; the sweep checked all **105** wrap targets and 97 of them reach every
    subclass. → [agent/bugs/F106.md](agent/bugs/F106.md) (closed, refuted) ·
    report [agent/reports/F106_DISPATCH_SWEEP.md](agent/reports/F106_DISPATCH_SWEEP.md)
    · log `agent`-side `docs/archive/f106_Mars.exe-20260824-02.32.27.log`
    · suite `75 PASS / 1 FAIL / 24 SKIP / 0 ERROR` of 100, gate `78/78 applied`.

    ⛔ **The bad news, and the only thing here that needs you: the same run found
    a real defect in the F105 module you ruled on yesterday.**
    `Fix_LandscapeCostRefresh` was written to "check, then hand off to the
    game's own code". Because of the same early-apply timing, the hand-off
    captured **nothing** — it holds a nil where the game's function should be. In
    practice: **the crash you asked me to fix IS fixed** (the check fires and
    returns, which is the whole repair), but the hand-off half is dead code that
    would throw an error *inside our own file* if anything ever reached it.
    Nothing shipped is affected — this module is not on the live listings yet —
    but it is **the one module the queued 1.0.x upload exists to deliver**.
    → [agent/bugs/F107.md](agent/bugs/F107.md) (measured, not derived)

    ❓ **Your call — one question, three options.**
    * **(a) Repair it before the upload** *(my recommendation)*. The repair is
      small and, ironically, it is the shape **you** were originally offered on
      item 72: **one wrap on `ConstructionSite`** instead of three on the leaf
      classes. It is now measured to reach all 13 relevant classes. One module
      touched, one boot log to confirm, then the upload goes as planned.
      ⚠️ It widens the guard to ordinary construction sites too — harmless by
      construction, but it is a behaviour surface and that is why I am asking
      rather than deciding. (Audit-checked 08-24: in the one state where the
      widened guard changes anything, the game's own code would have crashed —
      so the widening can only ever prevent an error, never cause one.)
    * **(b) Upload as-is, repair in the next patch.** Defensible: the reported
      crash really is fixed and the dead branch is unreachable on shipped data.
      The cost is that the pack carries a latent error in its own file, and
      `EF-065`(a) means any such error names **us** in the player's popup — the
      exact misattribution F104 and F105 were both about.
    * **(c) Repair it with the minimal change** — keep the three installs, just
      take the game's function from the class that actually declares it. Smallest
      diff, no behaviour-surface change, but it leaves the shape that caused the
      bug in place.
    ✅ **RULED (a) and BUILT 2026-08-24 — receipt is item 76 above.**
    ⛔ (Historic:) the chain that found it was forbidden from writing fix code,
    deliberately, so that the finding and the fix stayed separate decisions.

    ⚠️ **One thing this run canNOT tell you, and no run so far can.** The sweep
    lists which subclasses do not receive one of our patches; it does **not**
    say which of those subclasses ever actually exist in a game. So the "audit"
    half of this item is **not complete and is not closed** — what is closed is
    the alarm that the mechanism was breaking everything.
    For the record, the leftovers it did find are the *old* known question
    (`EF-066`): 8 targets where a subclass writes its own version of the method
    we patched, so it keeps the game's behaviour instead of ours. That is
    under-coverage, never new harm. The largest is
    `Fix_ShuttleHubOffAvailable`, whose wrap on `BaseBuilding` is overridden by
    `Building` and so misses ~578 building classes; also
    `Fix_GhostFarmOxygen`'s wrap misses residences, research labs, training
    buildings and water reclamation spires. **None of these is new, none is a
    regression, and none needs you now** — they are per-fix coverage questions
    for the opt-in-era maintenance window, exactly where `EF-066` always put
    them.

### ⭐⭐ 2026-08-23 — THE FIRST FIELD REPORTS ARRIVED. Two GitHub issues, one reporter, and the pack was named in both. Neither error was ours.

72. ✅ **RULED 2026-08-24, in-session ("number 1 fix priority") — BUILT AND
    BOOT-VERIFIED the same day; receipt in the 2026-08-24 section above.**
    ⚠️ Kept as filed for the record; note the recommendation's mechanism was
    "corrected" during the build — the single reader wrap was believed unable to
    reach the landscape classes (F106), so the fix installs per leaf class.
    ⛔ 08-24: that belief was measured WRONG (F106 refuted, item 74) — the
    single wrap you were originally offered would have worked, and the per-leaf
    shape it was traded for carries F107.
    **F105 — do we fix the landscaping crash, or leave it?**
    A real vanilla defect, no mod needed: a terrain-levelling site never
    initialises `construction_costs_at_start`, so researching any tech that
    carries a `*_Construction` cost modifier throws. Squarely in charter, and the
    reporter hit it. ⛔ **We have never reproduced it** — everything we know comes
    from reading the shipped Lua against their log.
    → [agent/bugs/F105.md](agent/bugs/F105.md)
    **Two shapes, both small.** (a) guard the reader — skip the refresh when
    `construction_costs_at_start` is not a table; covers every subclass with the
    same gap. (b) initialise the writer — narrower, only fixes what we enumerate.
    **Recommendation: (a).**
    ⛔ **Price it post-release, not with the gate** (your 08-20 ruling, item 57):
    an `items.lua` entry, one boot `applied` line, doccheck counts. Nothing else.
    **What I'd want before building it:** a rig repro. Place a levelling site,
    research a dome-cost tech, watch for `ConstructionSite.lua:673`. ~10 minutes.
    ❓ **Your call:** build it now, build it after a repro, or leave it filed.

73. **The bigger one — we get blamed for other mods' crashes, and it will keep
    happening.** The engine decides which mod to flag by asking "does this mod's
    folder name appear anywhere in the crash text" (`Mod.lua:3001-3013`, its own
    comment calls it a "rough estimation"). We wrap ~60 game functions, so any
    error thrown *underneath* one of them names us. **Two sightings in one day,
    neither our defect.** The mod that actually caused F104 can never be named,
    because its function had already returned when the error happened.
    → [agent/facts/EF-065.md](agent/facts/EF-065.md) · F104 · F105
    **Four options, cheapest first — these are not exclusive:**
    * **(0) Log breadcrumb.** One handler that logs "the throw site is not a pack
      file". Costs nothing, accuses nobody, saves the next reader a whole session
      of derivation. *I'd do this regardless.*
    * **(1) Shrink the blame surface.** Patch leaves, not ancestors.
      `Fix_MilestoneCrash` replaces `CompleteMilestone`, which sits above the
      entire milestone→research→every-construction-site fan-out — that is exactly
      why F105 named us. Patching `Milestone:GetScore` instead does the same
      repair with almost nothing running underneath. **I checked every other
      caller: zero ripple** (`Challenges.lua:58` guards `if cs then`, and `0` is
      truthy). It also deletes a 40-line verbatim copy of vanilla that could drift
      on a game patch. *Strictly better code; my first pick.*
    * **(2) Trampoline.** Route call-throughs via a separately-loaded chunk so our
      file genuinely isn't on the stack while vanilla runs. Needs two boot
      measurements first (is `load` reachable from mod code; does a custom chunk
      name reach the traceback). Only for hooks that don't rewrite arguments.
    * **(3) Own the wording.** Wrap the global `ReportModLuaError`, pass every
      other mod through untouched, and for our id alone show **our own** message
      when the throw site isn't ours: "the pack appears in a crash raised in
      `<file>`, which is not part of the pack — please send the log." **Not
      suppression** — the player is still told, and told something true.
    * ⛔ **Rejected, on the record:** `config.DisableErrorReporting` (silences
      *every* mod, including other authors'), and pre-setting `ReportedMods`
      (silences us wholesale, before any error exists). Both are the blanket
      suppression you said to avoid.
    ❓ **Your call:** which tiers, and whether (2)/(3) touching engine internals
    for self-defence is inside `FIX_POLICY` at all. That last part is a policy
    question, not an engineering one, which is why it is here.

    ℹ️ **Ruling already taken and applied (2026-08-23, yours):** we DO name the
    other mod when answering a reporter. Stating the cause plainly is not
    slander, and shielding an unmaintained mod is not our job. `FIX_POLICY` §8
    still binds for *store pages and load-order advice* — this ruling covers
    issue replies. Worth folding into §8 explicitly on its next edit.

    ⚠️ **doccheck, copied verbatim:** `STATE.md is 9505 bytes, warn threshold is
    9216 — copy this line VERBATIM into the owner report; the owner fires
    agent/prompts/STATE_EVICTION.md`

### ⭐⭐⭐ 2026-08-20 — IT IS PUBLISHED, ON BOTH PORTALS. The ids are committed. One number came out differently on each store, and that was mechanical, not a mistake.

71. ⭐⭐⭐ **Live.** Paradox Mods **156049** · Steam Workshop **3787202810**. Both
    ids are now in `metadata.lua` and committed — ⛔ **that is how every future
    update finds the listings instead of creating a second one.**

    ⚠️ **The two stores show different version numbers for identical code, and
    nothing went wrong.** Paradox saves *after* the upload returns, so it got the
    package built at `version 0` → **1.0.0**, exactly as you ruled. Steam saves
    *before* it packs, so its bump landed **inside** the archive → **1.0.2**.
    Running both in one sitting is what produced the gap; the sheet predicted it
    (§0.5(c)) and it is now on the record rather than a mystery for later.
    ⇒ **This retires item 37 Q2** — Steam's number was decided by circumstance.
    ⛔ **Do not re-upload to tidy it.** Another upload bumps again and makes the
    two further apart, not closer.

    ℹ️ Steam's file is **385,131 B** against our packed **391,567 B**. Also
    expected: that same forced save stripped every comment out of `metadata.lua`
    and `items.lua` before packing them. **The 78 code files are byte-identical
    on both portals** — only one integer and two files' comments differ.
    ⇒ The delivered-bytes check (§0.5(f)) now says so: md5 **against Paradox
    only**; Steam reconciles by entry list, not by hash.

    ✅ **Repaired here, and it is the writeback the sheet warned about:** the
    saves stripped ~140 lines of comments from those two files. `items.lua` had
    **zero** value changes and was restored whole; `metadata.lua` kept its six new
    fields and its `version 2` and got every comment back, with the split above
    written into the file where the next reader meets it.

    ⛔ **One tool defect found while doing it.** `upload_preflight` reported
    **20 checks before the upload and 18 after** — `SaveDef` omits properties at
    their default, so publishing deleted `version_minor`, and the guard printing
    *"PackVersion a player sees"* silently dropped both version lines. The tool
    went quiet about the version at the exact moment the version got complicated.
    Fixed: a missing minor now reads as `0`, mirroring the engine's own default
    (`Mod.lua:265`). It reads **20 checked · 0 FAIL** again, and prints
    `PackVersion 1.0.2`.

    ✅⭐ **YOU SUBSCRIBED, SO THE DELIVERED-BYTES CHECK RAN — the first time this
    project has ever verified what a player actually receives.** Every byte check
    before it stopped at the file we upload.

    **Steam: checked, and clean.** The downloaded copy is **385,131 B**, matching
    the page; **82 entries**; and against our tree **80 are byte-identical and
    exactly 2 differ — `metadata.lua` and `items.lua`**, the two files that save
    rewrote. ⇒ **All 78 code files a Steam player gets are byte-for-byte the ones
    you watched working.** I read `version` out of the archive itself: **`2`**, so
    Steam is confirmed **1.0.2** by measurement rather than reasoning.

    ⏳ **Paradox needs one more thing from you, and it is small.** Subscribing on
    the website downloads nothing — `PdxMods\` holds only an empty `temp_pdx`; the
    game fetches it at startup. ⇒ **Next time you launch, it lands on disk and I
    read its version the same way**, which closes the question below for good.

    ⛔⛔ **AND ONE THING I TOLD YOU ABOVE MAY BE WRONG — I am flagging it rather
    than leaving it.** I said Paradox holds 1.0.0. The Paradox browse card reads
    **376 KB**, which is Steam's 385,131 B in KiB — *not* our 391,567 B pack. If
    Paradox received the same stripped, bumped archive Steam did, then it is
    **not** 1.0.0 and the version story is one number, not two. The counter-
    evidence is real: `pdx_version` came back `"1"`, which is only reachable if
    Paradox saved *after* uploading a version-0 tree. ⇒ **One download settles
    it** — §0.5(f) already asks you to pull the published copy; when you do, I
    read the `version` inside its `metadata.lua` and correct the record either
    way. ⚠️ Until then, do not repeat "Paradox is 1.0.0" as settled, including
    anywhere on the store pages.

    ℹ️ **Also on that card, worth your eye, not mine to change:** the author
    renders as **`cat144`**, while `metadata.lua` says `catt144`. Portals
    usually show the *account* name rather than the metadata field, so this is
    probably just your Paradox account — but if it is a typo in the account, it
    is the kind of thing that is easier to fix on day one than later.

    ⇒ **Still owed on the live listings, all yours:** §0.5(d) the required game
    version **350453** on the Paradox page if it offers the field · §0.5(f) the
    download checksum · then the site: I put both store links in, you switch
    Pages on, and the site link goes back onto the two store pages (§1 steps
    2–4). ⭐ **Say the word and I'll do the store-links step now** — I have both
    ids; I only need the Paradox page URL in the form your browser shows it,
    because I will not construct a store URL from a pattern.

### ⭐⭐ 2026-08-20 — THE AUDIT IS DONE. VERDICT: SHIP. The repo's active work ends here; the upload sitting is yours whenever you want it.

66. ⭐⭐ **SHIP.** Both fixes go in 1.0.0; the tag is moved onto this ruling's
    commit and now stands on **your attended sitting** (plus your one-time
    release-gate ruling, item 57) — not on run B, which two new modules
    outdated. I found **no launch blocker**. What I tried to break, and what
    happened:

    | challenge | what I did | result |
    |---|---|---|
    | the C50 regression warning | re-read the module: `preset.effect` is only ever **read** (one line), never written; your row-4 reading — first bullet **(40,000)** intact on both screens — is the screen proof | ✅ holds |
    | evidence provenance | traced every `tested-attended` word to who/screen/language/log; C51's claim rests on the **German** readings, never the English pass | ✅ holds |
    | H-10 (ships absent) | compared `items.lua`, metadata's `code` list and disk **myself**: 78 = 78 = 78, identical order, both new modules present; `pack_predict` **82** | ✅ holds |
    | frozen things | `version` still `0` · `C52` still `parked` · no opt-in passage restored · no player surface names the other mod · **nothing published** (no portal line in any log) | ✅ holds |
    | the sitting's own wrong turn | re-derived the rocket-subclass story **from the engine's class builder at Src** — the report's marked correction is right, and the suite message *"a later mod has chained on top of ours"* is provably wrong about the cause (it's the engine composing `Init`; no later mod exists). Recorded as fact `EF-066` | ✅ report honest |

    ⚠️ **Named, not blockers:** the challenge landing-spot screen and the
    SpaceY in-game Goals panel remain unobserved (your item 59/63 skips); the
    English rocket-rollover reading predates the mid-sitting repair, so
    "English players see no change" on the final build rests on the measured
    language data, not a screen — the mechanism makes it byte-identical.

    ⭐ **The question this chain never asked (my C5):** the pack wraps ~60
    class methods, and **nobody has ever checked which of them have subclasses
    that override the wrapped method** — a subclass that does keeps vanilla,
    fix and all. C51's rocket half is the only place that question ever
    surfaced, and it cost that fix its whole working life until your tracer
    caught it. The safe part: a missed subclass means *the bug stays vanilla
    there*, never new harm. It's recorded in `EF-066` as opt-in-era
    maintenance, not a launch item.

    ⚖️ **Was five prompts for two text fixes worth it? Yes — narrowly, and
    not for the reason planned.** The builds alone didn't need a chain. But
    link 4's prep caught C50 printing a wrong number on a screen no record
    had ever named, and the sitting caught C51's rocket half having never
    worked at all. Both would have shipped broken under "just build and
    upload." The chain's cost was mostly the two build links; its value was
    the two catches. A future two-fix change should be a **two-link** chain:
    build, then attended-test-plus-audit in one.

    ⚠️ Housekeeping line, emitted after my edits and copied verbatim as it
    requires: **`warn STATE.md is 9941 bytes, warn threshold is 9216 — copy
    this line VERBATIM into the owner report; the owner fires
    agent/prompts/STATE_EVICTION.md`** — fire the eviction prompt whenever
    convenient; nothing about the upload waits on it.

67. ⭐⭐ **Your upload sitting, restated — nothing else stands between you and
    the release:**

    1. **Re-tick the mods** in the Mod Manager (the junction pull cost the
       enables; restart after ticking).
    2. ⛔ Before anything is pressed: **not dirty, and `1.0.0` on screen.**
       ⇒ see item **70** for the exact command and what each answer means —
       ⚠️ **`nil` is a PASS**, and the sheet used to imply it was not.
    3. Pack via **Mods Manager → Edit (`Ctrl-E`) → File → Pack Mod** — ⛔ no
       console route exists. Expect **82 files**; a different count means
       stop, not adjust. Record the md5/bytes in §0.5(f)'s blank row **at
       pack time**.
    4. ⛔ **Paradox Mods FIRST**, Steam second.
    5. Then the sheet's §0.5(d) — game version **350453** on the portal page;
       §0.5(e) — the id-writeback commit; §0.5(f) — md5 your downloaded pack
       **against the row you filled in at step 3**.

70. ⛔ **The dirty check, exactly — asked 2026-08-20, and the sheet's expected
    value was wrong in the same way the version digit was wrong on 08-19.**

    **The command, in the in-game console (Enter, in a loaded colony):**

    ```
    print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())
    ```

    **How to read the two values:**

    | value | meaning |
    |---|---|
    | first — `0` | ✅ **1.0.0**, which is what you ruled. ⛔ A `1` means the version already moved — **stop.** |
    | second — `nil` | ✅ **PASS.** Nothing has dirtied it, and the mod has not been opened in the Mod Editor this session. |
    | second — `false` | ✅ **PASS.** Opened and hashed, unchanged. |
    | second — `true` | ⛔ **STOP.** The upload would force a save and bump you to 1.0.1. |

    ⚠️ **Why `nil` had to be spelled out.** `IsDirty` is
    `return old_hash and (old_hash == 0 or old_hash ~= data.current_hash)`
    (`CommonLua/GedEditedObject.lua:93-98`, read at Src 08-20). If `old_hash` is
    unset — which it is until the mod is opened in the editor — the whole
    expression is **`nil`**, not `false`. The **only** archived reading this
    project has, act 1 on 08-19, is exactly that: `dirty: nil`
    (`archive/act1_Mars.exe-…15.18.19…:258`). ⛔ The sheet said *"must be
    `false`"*, so a correct `nil` would have read as a failure and stalled you —
    the same shape of error as the `1`/`0` inversion corrected on 08-19.
    ℹ️ Item 44's step 1 said *"the 08-19 console read returned `0 false`"*; no
    archived log contains that string, and the reading it cites shows `nil`.
    Corrected there too.

    ⭐ **The check that matters more, and it needs no console at all.** Whatever
    the console says, the real guard is the editor's own behaviour: **if the Mod
    Editor prompts *"The mod needs to be saved before uploading"*, STOP** — that
    prompt IS the forced save (`ValidateModBeforeUpload`,
    `GedModEditor.lua:836-844`), and it is the thing that would bump the version
    inside the package. The console read is the early warning; the prompt is the
    tripwire.

69. ⭐ **What to fire, and when — asked 2026-08-20 after the eviction.**

    ⛔ **For the upload itself: nothing.** No agent can publish, so there is no
    prompt to run. It is you, item **67**'s five steps, and
    `reports/RELEASE_PORTAL_PREP.md` §0.5 open beside you.

    ✅ **After the listing exists, fire
    `docs/agent/prompts/POST_UPLOAD_CLOSE.md`** — written 08-20 for exactly that
    moment. It exists because the writeback is not a copy-paste: the forced save
    that writes `pdx_id`/`steam_id` into `metadata.lua` also **regenerates that
    file from memory and strips every hand-written comment in it**, so the ids
    have to be committed *and* the prose restored in the same commit. It also
    ⛔ forbids the tempting mistake of "correcting" `version` back to 0 — after
    Paradox the tree sits at `1` by design, and normalising it would lie about
    what is published.

    ⚠️ **Nothing else is owed by that prompt** — it does the three sheet checks
    (§0.5(d) game version, (f) delivered bytes), closes STATE and the records,
    and hands off to the opt-in. It routes **37 Q2** (Steam's number) back to you
    rather than deciding it, because that call is only decidable once Paradox is
    done.

68. ⭐ **The opt-in effort starts on your word** — your stated next priority
    (*"shift resources and start working on the opt in"*). Its first session
    must read **that repo's own STATE** and its standing pre-upload
    obligation: `reports/PARKED_OPTIN_REFERENCES.md` (~46 parked passages
    that restore only when the opt-in pack launches). I have deliberately not
    scoped it further — that's its own repo's job.

### ✅✅ 2026-08-20 — YOUR SITTING IS DONE AND BOTH FIXES WORK. Nothing here is owed from you; this is the receipt.

63. ⭐⭐ **You saw both fixes working, in two languages.** Every reading passed:

    | what you looked at | what it said |
    |---|---|
    | SpaceY rollover + summary, English | the new bullet, **(40)** — the number I predicted before you launched |
    | SpaceY rollover + summary, German | **Maximale Anzahl an Drohnen, die ein Drohnen-Hub kontrollieren kann (40)** |
    | SpaceY's first bullet, both | **(40,000)** cargo intact — the regression that mattered most didn't happen |
    | terraforming heading, English | no visible change — exactly what the site page promises |
    | terraforming heading, German | **TERRAFORMING-GESAMTFORTSCHRITT** |
    | Back to Earth rollover, German | **Zurück zur Erde** |
    | the suite | **74 PASS · 0 FAIL · 24 SKIP · 0 ERROR** of 98 |

    ⭐⭐ **The single most valuable thing you did:** the German heading. In vanilla
    that text is a raw code string with no translation attached at all — there is
    no way it becomes German by itself. It is German *because of our fix*. That
    also closes a question this project has carried since **2 August**: nobody had
    ever watched one of these repairs render in another language. Now we have,
    twice.

    ⚠️ **The suite's 24 skips are all "another mod isn't loaded"** — 8 opt-in, 6
    save-rescue, 8 retail sandbox, 2 odds and ends. **0 failures, 0 errors.** Your
    store card's "98 checks" is now a measured number instead of a claim (item 60,
    closed).

    ⛔ **Two things nobody looked at, named rather than counted as passes:** the
    challenge landing-spot screen, and the in-game Mission Profile on a SpaceY
    colony. Both are the same code seen working elsewhere; neither is a launch
    item.

64. ⚖️ **Two code changes happened while you sat there, and you should know what
    they were.**

    - **`C50`** — the double-count you ruled on (item 61). Built, and confirmed by
      both the console and the suite: the in-game panel now shows vanilla.
    - **`C51`'s rocket half was a no-op as shipped-in-progress.** It had *never*
      worked, in any session. It searched for the Back to Earth button in the
      wrong place. It now uses the engine's own lookup, and you watched the result
      in German.

    ⛔⛔ **And one thing I got badly wrong, which you should hear plainly.** I
    talked myself into a theory that rocket subclasses don't inherit the fix,
    built a change for it, and when that change looked like it failed I
    **recommended cutting the rocket half from 1.0.0**. Your very next screenshot
    showed it working. A good fix was one message away from being deleted on my
    bad inference.

    ⭐ **What saved it was your question** — *"why can't you detect it when I press
    the button and trace it back?"* That tracer answered in one shot what three
    rounds of me reading source got wrong. Recorded in the report as the method
    lesson, because it is one.

65. ⚠️ **Two small things for the record, neither needing anything from you.**

    - **The `[LUA ERROR]` in your logs is mine, not the pack's.** My console
      tracer used a function the mod sandbox doesn't have. It was contained, and
      it's flagged in the report so the audit doesn't misread it.
    - **Your autosaves are intact** — `Sol 406` and `Sol 411`, byte-identical to
      the copies I took before the first launch, reconciled by name. `C47FARM`
      untouched.

    ⭐⭐ **Next: `docs/agent/prompts/closeout-1.0.0/05_AUDIT_fable.md` — the last
    link.** It reviews everything adversarially, moves the release tag, and rules
    ship-or-revert. **It does not need you.** After it, the upload sitting is
    yours whenever you want it.

### ⛔⛔ 2026-08-20 — the sitting's prep found a real defect in `C50` (RULED: fix it). Kept as the record of the call.

61. ⛔⛔ **The thing I found, and it needs your word before the sitting.** `C50`
    was recorded — twice now, and by me — as touching **pre-game screens only**.
    While writing your script I traced the panel it patches and **it is also an
    in-game screen**, and on that screen **the number it prints is wrong**.

    **What is actually true.** The pre-game mission summary panel is not built in
    one place. The game builds the same panel again for the **in-game Mission
    Profile dialog — the Goals button on your HUD**. Both go through the exact
    function `C50` wraps. So the bullet appears in a running game too, which
    nobody intended and nothing recorded.

    ⛔ **And in a running game the arithmetic double-counts.** The base Drone Hub
    capacity is **20**. SpaceY adds **+20**. Pre-game that gives the right answer,
    **40**. But once a colony exists, the game has *already* applied SpaceY's +20
    to the live value — so the fix reads 40, adds 20 again, and prints **60**.
    The real cap is 40. ⚠️ **The safety check inside the fix cannot catch this**:
    it only asks "is the number bigger than the baseline", and 60 is bigger than
    40, so it passes happily.

    ⚖️ **How much does it matter?** Honestly: **little, but it is wrong.** You
    only ever see it if you play **SpaceY** *and* open the Goals/Mission Profile
    panel mid-game. It changes no save, breaks nothing, and every pre-game screen
    — the three the sitting is actually about — shows the correct **40**.
    ⛔ But it is a wrong number that we introduced, on a screen a player can
    reach, and the site's fix page already promises this fix is a plain repair.

    ⭐⭐ **My recommendation: fix it, and it is about six lines.** Have the fix
    **stand down when a game is running** — the bullet then appears on the
    pre-game sponsor screens exactly as designed, and the in-game Goals panel
    goes back to showing vanilla. That matches what the module already says about
    itself ("it is pre-game UI text"), it is the smallest possible change, and
    the sitting can confirm it by opening the Goals panel and seeing no bullet.

    ⚖️ **Your options:**

    | | what happens |
    |---|---|
    | **A — fix it now (recommended)** | ~6 lines + a corrected header. Adds maybe 10 minutes before your sitting, and the sitting then checks it for free (open Goals, expect no bullet). |
    | **B — ship it as-is, file the defect** | `C50` ships with a wrong number on one in-game panel for SpaceY players. Recorded as a known defect for the opt-in effort. Costs you nothing today. |
    | **C — pull `C50` out of 1.0.0** | `C51` ships alone. ⛔ Its site fix-list entry has to come out too. I do **not** recommend this — the defect is small and the pre-game repair is sound. |

    ⚠️ **Note on the fence:** link 4's brief says code changes are out *unless the
    sitting finds a fix broken*. I found this **before** the sitting, from the
    source, not from a screen — so I am asking rather than just doing it.

    ⭐ **Nothing about this blocks you from starting.** If you pick **B**, the
    script below runs unchanged, right now.

62. ⭐ **Your script — about half an hour, one launch, two language settings.**
    Everything is prepared: predictions are written down and committed *before*
    the game opens (`docs/agent/reports/04_ATTENDED_SITTING.md`), and ⚠️ **both
    your autosaves are already byte-copied out of the save directory** (`Sol 406`
    and `Sol 411`, `EF-056`) — reconcile them by name when you are done.

    ✅ **Save: `C47FARM`** — your word, 2026-08-20. Two of the readings need it
    loaded, with a **Universal Rocket sitting idle on Mars** and the **planetary
    view** available.

    ⚖️ **Item 61 is RULED and BUILT.** You chose the fix; it is in, it parses,
    doccheck is GREEN and `upload_preflight` still reads 0 FAIL with 78 entries in
    order. Step ② below carries the one check that confirms it.

    **① English, pre-game — the two free `C50` looks.**
    New game → sponsor selection → **SpaceY**.
    - ✅ Expect the summary panel's SpaceY description to carry a **new fourth
      bullet: *"Maximum number of Drones a Drone Hub can control (40)"*.**
      ⭐ **The number should be 40.** (The brief's example said 100 — that was an
      illustration, not the real value.)
    - ✅ Now **hover SpaceY in the sponsor list** — the rollover is a second,
      independent look at the same repair. Same bullet, same 40.
    - ⛔ **Read the FIRST bullet both times too:** *"Dragon Rocket - has smaller
      cargo capacity **(a number)** but is faster and requires less fuel."* If
      that number is gone, or you see raw `<cargo>`, **stop and tell me** — that
      is the failure the whole design was built to avoid.
    - ⛔ If you see literal `<drone_cap_help>`, `<CommandCenterMaxDrones>`, a
      `{#4706}` token, or an empty `()` — **tell me exactly what the screen says,
      word for word.** Do not summarise it.

    **② English, in-game — the `C51` "nothing changed" reading.**
    Load the save → open the **planetary view** (the Mars/planet button) → then
    select your idle **Universal Rocket** and hover its **Back to Earth** button.
    - ✅ Expect **no visible difference at all**, on both. That *is* the reading —
      the site page promises English players see nothing change, and this is the
      step that checks exactly that.
    - ⚠️ **If the Back to Earth button is not on the rocket's panel**, the rocket
      is busy. It only shows on a Universal Rocket that is **idle with no
      destination set** (not loading, not launching, not an asteroid Lander).
      Cancel its flight and it comes back.
    - ⭐ **And the 20-second check on the defect you just ruled** (item 61 — it is
      built, parse-clean, and in). ⚠️ **Do not just look at the Goals panel** — I
      wrote that first and it was wrong: `c47farm` is not a SpaceY colony, so the
      panel would look identical whether or not the repair works. Paste this
      instead, anywhere in the loaded game:

      ```
      *r local sp = table.find_value(MissionParams.idMissionSponsor.items, "id", "SpaceY")
         ModLog(tostring(SMRFixPack.SpaceYDroneCapBullet.bullet_for(sp, "probe")))
         ModLog(SMRFixPack.SpaceYDroneCapBullet.stats.probe.reason)
      ```

      ✅ Expect **`nil`** and then a line saying *a game is running…*. Before the
      fix this printed a bullet with the wrong number in it. That is the whole
      proof, and it cannot disturb the three real screens.

    **③ Switch the game language to German. Restart if it asks.**

    **④ German, pre-game — the same two sponsor looks.**
    - ✅ Expect the bullet's sentence **in German**: *"Maximale Anzahl an Drohnen,
      die ein Drohnen-Hub kontrollieren kann (40)"*.

    **⑤ German, in-game — ⭐ the only step that can see `C51` at all.**
    Reload the same save → planetary view → rocket rollover.
    - ✅ Expect the heading as **`TERRAFORMING-GESAMTFORTSCHRITT`** and the rocket
      rollover title as **`Zurück zur Erde`**.
    - ⭐ **This is the first time in this project's history that anyone has watched
      a shipped translation id render in another language.** Whatever it shows,
      it closes a note that has been open since 2026-08-02 — so tell me even if
      it looks boring.

    **⑥ Switch back to English, restart, confirm the screens look normal again.**

    **⑦ Optional, your call (this is item 60):** `*r SMRTest.RunAll()` — a minute
    or two, and it turns the store card's "98 checks" into a measured number.
    ⭐ **Run it if the sitting went smoothly; skip it if you are out of patience.**
    Either way I record which.

    ⚖️ **The challenge landing-spot screen is the one I recommend skipping**
    (your item 59 ruling already allows this). It is the same code on a screen
    you would otherwise never open. If you skip it I record it **by name** as an
    unobserved site, not as a pass.

    ⭐ **When you are done: tell me what you saw in your own words** — I am not
    allowed to write down any screen reading you did not report to me, and I will
    not.

### ⚠️ 2026-08-20 — THE PAGES AND THE RELEASE SHEET ARE CAUGHT UP (link 3 done). One small thing wants your word, and the next link is the one that needs your hands.

60. ⭐ **What moved, in one breath.** The site's fix list now has entries for both
    new fixes; the md5 you were told to checksum your download against is gone and
    replaced with a blank you fill in when you pack; and the counts everywhere now
    read what the emitter says. **Nothing you have to do about any of that.**

    ⛔ **The one number I could not honestly finish.** The store card says *"an
    automated suite of N checks is run against the game with the pack and without
    it."* The suite grew from 96 to **98** when the two new fixes brought a check
    each, so the card now says 98 — **but nobody has run it at 98.** The last real
    A/B measurement is `80/0/16/0` of **96**, from 08-15, and link 4's script
    makes the suite step optional on purpose because you ruled the basic-testing
    bar (item 57).

    ⚖️ **Your call, and it is genuinely small:** at the sitting, `*r
    SMRTest.RunAll()` costs a minute or two and turns the card's 98 into something
    measured — or say the word and it stays a statement about the suite the pack
    ships with, which is what it literally says and is true either way. ⭐ **My
    recommendation: run it if the sitting is going smoothly, skip it if anything
    else is eating the half hour.** The two new fixes are checked by their own
    probes inside it, so it is not wasted either way.

    ⚠️ **A trap I found and defused while sweeping:** the four `smrcf-*` chain
    folders from 08-16 still told a future session to *build* `C50` and `C51`.
    They now carry a banner saying both shipped on 08-20 and that chain B must
    not be run. `C52`'s chain is banner-fenced as frozen too. Nothing was
    deleted — chain A and the jumbo-cave chain are untouched and still owed.

    ⭐⭐ **Next: `docs/agent/prompts/closeout-1.0.0/04_TEST.md` — this is the one
    that needs you, about half an hour, one launch.** Everything in the pack right
    now is built and **unobserved**; that sitting is the only eyes either fix ever
    gets before it ships.

### ⚠️ 2026-08-20 — C50 IS BUILT, AND IT TOUCHES THREE SCREENS RATHER THAN THE TWO ITS BRIEF NAMED. Your sitting in link 4 changes slightly.

59. ⚠️ **What I found, and the call I made without stopping you.** The brief for
    `C50` named two places SpaceY's description gets assembled and said to append
    at both. I re-derived that list before building — the brief told me to prove
    the caller counts myself — and **it was wrong in both directions**:

    | screen | what happens now |
    |---|---|
    | the pre-game **mission summary panel** | bullet added ✅ *(in the brief)* |
    | the **rollover when you hover a sponsor** in the picker | bullet added ✅ *(NOT in the brief — a live screen the record had never named)* |
    | the **challenge landing-spot screen** (3 shipped Challenges use SpaceY) | bullet added ✅ *(NOT in the brief either)* |
    | the "in-game mission profile" the brief listed | ⛔ **left alone — that function has zero callers anywhere in the game.** It is dead code; the in-game profile dialog does not show sponsor effects at all. |

    **My call:** build all three live screens, skip the dead one. Fixing one of
    three would have left the defect visible on the other two, and `FIX_POLICY`
    §4a bars shipping code for a function no shipped caller reaches (the F28
    lesson — we retired a fix over exactly that once). ⚖️ **If you would rather
    it stayed to the two the brief named, say so and I will cut it back** — the
    third site is one wrapper and comes out cleanly.

    ⚖️⚖️ **RULED 2026-08-20: KEEP all three sites** (owner: *"keep 59"*). ⇒ No code
    changes; the challenge landing-spot wrapper ships. ⭐ **Looking at it during the
    sitting stays optional** — §2a of the test brief says that if it is not opened,
    the report names it as an unobserved site rather than counting it as a pass.

    ⭐ **What changes for your ~30-minute sitting (link 4).** The bullet is now
    visible in **two places without starting a game**: the sponsor summary panel
    *and* the hover rollover on the sponsor list — so you get two independent
    looks for free while you are already on that screen. The third, the challenge
    landing spot, needs a SpaceY **Challenge** started; ⚖️ **that is the one I
    would skip unless you want it** — it is the same code on a screen you would
    otherwise have no reason to open, and the probe already checks the wrapper is
    installed there.

    ⛔ **Nothing about this moves the store card's "five judgment calls" count** —
    your 08-20 ruling that `C50` is a plain repair still stands and is untouched.

### ⭐⭐ 2026-08-20 — THE PLAN CHANGED ON YOUR RULING: C50+C51 ship IN 1.0.0, C52 is frozen, and the chain that closes this repo is written and waiting.

58. ⭐⭐ **Your ruling, and what is now sitting ready.** *"C52 is going frozen may
    revisit at a later date. C50-C51 we are going to close out and launch. With
    basic testing. One chain to do both, with a testing chain right before the
    fable audit… I don't want to upload and move right into 1.0.1 work. I would
    rather shift resources and start working on the opt in."*

    ✅ **`C52` is `parked` — frozen, reversible, and fenced.** No session may open
    it without a fresh word from you. ⚠️ One piece of it is *not* parked because it
    is not a code fix: the mod browser caches preview art on **id + version**, so
    if you ever replace the preview after publishing **without a version bump**,
    everyone who already saw it keeps the old picture forever. That lives on the
    upload sheet now.

    ⭐ **The chain is written: `agent/prompts/closeout-1.0.0/`, five links.**

    | # | link | needs you? | what it does |
    |---|---|---|---|
    | 1 | build `C51` | no | the three untranslatable strings |
    | 2 | build `C50` | no | the SpaceY bullet |
    | 3 | surfaces | no | the two fix-list entries, counts, the stale pack fingerprint |
    | 4 | ⭐ **the sitting** | **YES, ~30 min** | the only eyes either fix ever gets |
    | 5 | Fable audit | no | breaks it, moves the tag, rules ship-or-revert |

    **Kick off link 1 with:** `docs/agent/prompts/closeout-1.0.0/01_BUILD_C51.md`
    — each link ends by handing you the next line, and link 5 ends by handing you
    the opt-in.

    ⭐ **What your sitting in link 4 actually is:** one launch. Check both modules
    say `applied`; look at SpaceY's description on the sponsor screen (the new
    bullet, *and* the first bullet's cargo number, which is the one thing that
    could have broken); glance at the terraforming panel and the rocket's *Back to
    Earth* rollover, where you should see **no change at all**; then switch the
    game to German, look at the same three things, and switch back. ⭐ That German
    look is the only way `C51` is visible to anybody, and it is also the first time
    this project will have watched a translated string render in another language
    — a gap our own records have carried open since 2026-08-02.

    ⚠️ **Two consequences of building before launch, stated up front, neither a
    surprise:** the release tag will **move** in link 5 (it currently marks bytes
    measured in run B, and two new modules invalidate that), and the recorded pack
    fingerprint — the md5 you were told to checksum your download against — goes
    stale, so link 3 rewrites that check to use the md5 recorded when *you* pack.
    ⛔ Nothing about the upload route changes: still Paradox first, still
    `IsDirty()` false and 1.0.0 on screen before anything is pressed.

    ⇒ **After link 5 this repo is closed** — nothing queued, nothing owed, until a
    player report, a real problem, or a game patch. Which is the point.

### ⚖️⚖️ 2026-08-20 — YOU RULED THE POST-RELEASE TESTING MODEL, and corrected a cost I had been quoting wrong.

57. ⚖️ **STANDING RULING — the release gate was a one-time cost, not a per-change
    tax.** Your words: *"I do not plan to do a major lens sweep and b leg like we
    did for pre release unless we have to do a major overhaul of the mod again…
    My post release plans is basic checks from patch notes to see if we need to
    remove, or change fixes, and add new fixes if there are new bugs. We won't
    most likely run multi day tests ever again."*

    ⛔ **This corrects me, and future sessions should not repeat my error.** I
    priced a single UI-text module using `FIX_POLICY` §3a's per-module cost —
    save-safety pass, probe, suite re-measure, three store surfaces. Most of that
    was the **release gate amortised across 75 modules**, and it does not recur
    for one added fix on a shipped mod. Quoting it made a cheap change look
    expensive, which is the opposite of useful.

    ✅ **What a normal post-release change actually owes**, and it is short:
    * the `items.lua` entry for any new module (**H-10** — this is the one that
      would have shipped a fix that never loads; it is a ten-second check, and it
      is not ceremony);
    * one boot log showing the new module reports `applied`;
    * a language-switched look **only** for a fix that cannot be seen in English
      (`C51` is the sole example on the books);
    * `doccheck` counts re-emitted, never hand-typed.

    ⛔ **What does NOT recur:** run B, the eight-lens sweep, the terminal audit,
    the multi-day gate. Those bought a first impression, which happens once.
    ⇒ They come back only for what you named: **a major overhaul.**

    ℹ️ Your other observation, recorded because it is the pack's premise: *"if
    paradox tested as extensively as we do as the actual paid developer, there
    would be no need for us."* The bar being higher than the developer's was right
    for the launch; it is not right for every later line of text.

### ⭐ 2026-08-20 — C49 is RETIRED on your word, and I measured how hard C50/C51 actually are. Item 34's "now or after" is still yours.

56. ✅ **`C49` → `wontfix — unreachable`, done.** Your words: *"c49 wontfix -
    unreachable is right, get it off our list and retire it."* The entry keeps the
    reading and records the retirement, with the one falsifier that would bring it
    back named: non-vanilla code assigning `show_overlay = "soil_solid"` — a mod
    or the console, which is the only route there has ever been.

    ⭐ **And I stopped guessing at C50/C51 and went to the shipped language data.**
    You said these look simple and that fredware's modules should let us validate
    quickly. **Half right, and the half that isn't is the important one.** Every id
    below was looked up this session in the real `German.fpk`, extracted with our
    own tool:

    | id | who uses it | in the German pack? |
    |---|---|---|
    | `914616772802` | the terraforming heading's *unused* record | ✅ *TERRAFORMING-GESAMTFORTSCHRITT* |
    | `407456913268` / `316233855405` | *Back to Earth* title/text, unused records | ✅ *Zurück zur Erde* / full sentence |
    | `885571832096` / `807999655245` | the ids the button **actually** uses | ⛔ **absent — 0 hits, both** |
    | `880574954148` | SpaceY's shipped description | ✅ present and translated |
    | `981267450064` | **fredware's replacement SpaceY text** | ⛔ **absent — 0 hits** |

    * ✅ **`C51` is as simple as it looks, and it is loss-free.** Nothing is
      re-worded — three UI elements get pointed at ids whose translations already
      ship. I verified the two hook points at source myself: `TerraformingOverall`
      and `customUniversalRocket` are both real classes with an `Init`, and the
      rocket button carries `Id = "idBackToEarth"`, so that half needs no text
      matching at all. It writes nothing to a save. ⚠️ **Two catches, both small.**
      The terraforming heading has *no* Id, so the only handle is its literal
      English text — fine on a frozen game, fragile in principle. And **an English
      player sees no change whatsoever**, so proving it works means switching the
      game to another language for one look. Scope is exactly three strings; the
      *COLONY DATA* heading and two Options strings have no record in any pack and
      are a different, bigger job.
    * ⛔ **`C50` is the opposite: trivial defect, no free fix — and fredware's
      module is the one route we must NOT copy.** Their fix swaps the description
      for `T(981267450064, …)`, and that id is in **no** language pack, so under
      `EF-039` all eight non-English languages would render the English literal.
      Our entry predicted this; the lookup above confirms it. What is left: append
      an untranslated English sentence to the shipped translated text (safe, but
      one English line inside eight translated descriptions), or ship our own
      per-language table (`ModItemLocTable`, which overrides the shared table for
      vanilla and every other mod), or leave it. ⇒ **This one is a judgement call
      about which harm you accept, not a coding problem, and no amount of testing
      settles it.**
    * ⚠️ **`C52` — your memory is right, it is the risky one.** Three defects, and
      only one is cleanly ours: re-enabling the hyperlink path *may reinstate the
      fault the developers' comment was working around; the thumbnail cache is not
      fixable from a mod at all (it is upload discipline — bump the version when
      you swap art); and even the screenshot loop's diagnosis differs from theirs,
      because our own `EF-008`/`EF-064` refutes their stated mechanism.

    ⇒ **Still your call and unchanged in shape: `C51` is a genuinely small, safe
    module; `C50` needs a ruling from you before anyone writes a line; `C52` is
    1.0.1-or-later.** ⛔ All of them touch `Code/`, so building any of them before
    the upload breaks byte-identity with what run B packed and re-opens the gate.

    ⭐⭐ **UPDATE, same day — you asked me to go deeper on `C50`, and the deep
    reading changed the answer twice.** Full derivation in `agent/bugs/C50.md`
    ("REPAIR-ROUTE ANALYSIS"); the three things that matter to your decision:

    * ⛔ **The safe-looking fix I described this morning is NOT safe here.**
      Appending to the description turns it into a "concatenated" string, and the
      game's own text function *throws away the lookup table* when it sees one —
      so SpaceY's first bullet, which fills in its rocket's cargo number from that
      table, would lose the number it prints. **Breaking bullet 1 to complete
      bullet 3 is not a repair.** Both facts read at source this session.
    * ⭐ **But there is a route that survives, and it is better than "one English
      line".** Leave the sponsor text alone and add our bullet in the *screen* that
      shows it (two places show it). And the added bullet does **not** have to be
      English: the game already ships a translated sentence for exactly this —
      *"Maximum number of Drones a Drone Hub can control"* is a real record in all
      nine languages (I read the German). Even the number can come from the game's
      own table, so it stays right if a patch ever changes the base value. ⇒ **a
      fully translated bullet, no English anywhere, nothing rewritten.**
    * ⛔ **~~So the decision is not technical any more — it is editorial… that is a
      *judgment call* in our own sense of the word.~~ WRONG, AND YOU OVERTURNED IT
      THE SAME HOUR.** You said a genuine defect is by definition a bug, and our
      own published definition agrees with you: a judgment call is one that
      *"required deciding what the game meant"*, where *"there is no coding
      error"* or where *"we added a behaviour the game does not have"*. **Neither
      applies.** The 5-of-6 sponsor control settles what the game meant, and the
      `+20` is granted and working — the description contradicts the preset it
      lives in, which is your store card's own test. The pack also **already**
      ships a description repair (`Fix_TechDescriptionBuilding`, F25) that carries
      no judgment-call mark. ⇒ **`C50` is a plain repair, and the "five judgment
      calls" line on your store page does not move if it ships.** Correction
      recorded in `agent/bugs/C50.md`.

### ✅ 2026-08-20 — your two rulings are carried out. Nothing owed back; this is the receipt.

55. ✅ **Both sibling decisions are done, in the siblings' own repos, and neither
    touched the fix pack's shipping files.** Your words: *"You can mirror the two
    core fixes for the opt in. For the rescue mod I would just note it in its
    file system as a gate if we ever need to launch it."*

    * ✅ **Opt-in pack — the two core fixes are mirrored** (`SMR-OptInPack`
      `2cedf7d`). Both repairs landed in its own `00_Core.lua`, parse-swept and
      doccheck green, and the mirror was *checked* rather than assumed: with
      comments stripped and the namespace normalised, the three edited sites are
      now code-identical to ours. ⚠️ **Not verified in a running game there** —
      nothing was launched, and its STATE now carries the one boot check its
      launch session owes (that its eight modules register once each after a
      script reload). ⚠️ One honest split you should know: the double-name fix is
      the half that was actually *measured* on that mod (its `NoHomeless` is the
      module the dialog named twice); the false-alarm fix is **pre-emptive**
      there, because no module of its own currently uses the code path that
      leaves the stale mark. It is mirrored anyway — same design, and the next
      module to use that path would inherit the defect.
    * ✅ **Rescue mod — the gate is written where a launch session cannot miss
      it** (`SMR-CommunitySaveRescue` `9c912b3`, in its `CLAUDE.md`, the file
      every session reads first). It states the verified fact (no `items.lua`,
      2-entry code list), the mechanism as *our claim with its citations*, and —
      in the words that stop it being repeated as fact — that **the consequence
      is still not derived**: nobody has read what the game does when the file is
      *missing* rather than *incomplete*, and it may simply refuse to rebuild,
      which would be harmless. The gate's outcome is binary: a citation-backed
      showing that absence is harmless, or an `items.lua` written and re-verified
      after the forced save.
    * ℹ️ **A small gift to that future session, bought by my own detour:** the
      game source is under an install folder literally named **`Project Spark`**;
      the old `Surviving Mars` folder has a `ModTools` with *no* `Src` and is a
      decoy. `EF-014` said so and I walked into it anyway, so the exact path is
      now pasted into the gate. The derivation is minutes, not the twenty I
      quoted you, if you ever want it done early — say the word.

    ⇒ **Your remaining list is unchanged and short: re-tick the three mods, then
    upload — Paradox first.**

### ⭐⭐ 2026-08-19 — THE VERDICT REVIEW IS DONE: **UPHELD**. The upload now waits only on you.

54. ⭐⭐ **I tried to break the audit's upload verdict and could not.** A second,
    independent session ruled on it as your design required — not by trusting
    the audit, but by re-checking its evidence from the primary sources before
    reading its reasoning. What was re-verified first-hand: the shipped files
    are byte-identical from the release gate's commit (and from the release
    tag) to today; the built package re-hashes to the recorded fingerprint;
    your 10-of-10 gate's log-readable results all reproduce under a freshly
    written checker (including the packed-vs-unpacked comparison, redone
    because a tool once lied "identical" on empty input); and the two console
    reads you took in act 1 — the ones that proved both core fixes — were
    found in the live game logs and re-read. **Verdict: UPHELD. Upload when
    you are ready.** Full record: `SWEEP_FINDINGS.md` (VR-1…VR-6).

    **Three things worth ten seconds each, none needing a decision:**

    * ⭐ **Your act-1 console evidence was one log-rotation from being lost** —
      the two logs holding the `suspect: nil` / `order: 75` reads were never
      archived. They are now (`docs/archive/act1_*`), copied and checksummed.
    * ⚠️ **One honesty correction to the audit's wording, not its verdict.**
      Its "no player this ships to can reach the unswept remainder" line
      quietly assumes an English-PC-solo audience; the portal also serves
      console, non-English and multi-mod players. The verdict still holds —
      each unswept item was individually bounded (the code never branches on
      platform, our text falls back to English, the hardening queue all needs
      a hostile third mod) — but that is *why* it holds, and the record now
      says so.
    * ⭐ **One new post-upload step added to the upload sheet** (§0.5(f), takes
      a minute): after the listing is live, download your own mod once and
      checksum it. Everything the chain verified stops at the file we upload;
      nothing yet confirms players receive those same bytes.

    ⚠️ Also: mid-review, the game's account state showed fix pack + TestKit
    re-ticked (21:23 log) — no launch was taken and nothing was changed on the
    rig by this session.

53. ⭐ **The audit's verdict: upload the mod exactly as it stands.** A second,
    independent session (`99b_VERDICT_REVIEW_fable.md`) will try to break that
    verdict before you act on it — that review is the next session to run, and
    the upload waits for it, not for anything below.

    **What the audit did.** Ten independent verifier sessions each tried to
    *refute* the chain's findings rather than confirm them (your fan-out
    design). Most findings survived. Three did not: one recorded "gap" turns
    out not to exist (the game combines `Done` methods, so the track-station
    reclaim works after all — the error was in our favor); one measuring tool
    was flattering itself (its "24 full replacements" number is wrong — at
    least 4 of them actually chain politely; the tool is quarantined); and one
    code comment we accused of being backwards was right all along. The two
    core fixes that paused the upload survived a hostile re-read completely.
    The full record is `docs/agent/reports/99_TERMINAL_AUDIT.md`.

    **Said plainly, because the rules require it:** the sweep chain stopped at
    its cap with territory still unswept — console platforms, non-English,
    other people's mods, long sessions. That is *"we stopped counting"*, not
    *"it is clean"*. But none of the remainder can touch a player running this
    pack alone on the current game build, which is who 1.0.0 ships to, and the
    release gate you ran covers exactly that player. That is what the YES
    rests on.

    ❓ **The one call that is yours — the recorded hardening queue.** The
    sweep recorded a short list of code guards (all in `00_Core.lua` plus one
    module): they only matter if another mod, or a modder following our README
    wrongly, writes into our globals — a player alone can never trigger them.
    Applying them now would edit the exact file your 10-of-10 gate just
    validated. Three options:

    * ⭐ **Recommended: ship 1.0.0 as validated; do the whole queue as one
      1.0.1 hardening pass** verified by one unattended launch. The gate stays
      exactly what it measured; the queue's defects need a hostile third party
      that a fresh release does not have. (Your *"clean period"* ruling was
      about a defect players would see — none of these is.)
    * **Apply now + one unattended verification launch** — run B proved packed
      behaves identically to unpacked, so the unattended launch carries over;
      cheap, but the shipped file is no longer byte-for-byte the one the gate
      ran.
    * **Apply now + re-run the full two-act gate** — the strict option; costs
      you another sitting.

    ⚠️ One queue item was *wrongly marked settled* and the audit reopened it:
    the daily stale-reservation sweep has no per-item guard (the console test
    that cleared its two siblings never covered it — it's a plain loop, not a
    map walk). It's in the same queue, same third-party gating logic... except
    corruption, not a mod, is its trigger, which is why it's queued and not
    urgent: a throw there just leaves vanilla's own stale state in place.

    ⚠️ **One check-at-upload item added** (it's in the upload sheet §0.5): after
    the Paradox upload, check the portal listing has a "required game version"
    — the game never sends one, and players who turn on the mod browser's
    "only compatible" filter would otherwise never see the pack.

### ✅ 2026-08-19 — THE RELEASE CHECK IS DONE. You ran both acts; the gate scored **10 of 10**. Nothing below is owed from you — item 52 is kept as the record of what was run.

> ⭐⭐ **DONE 2026-08-19, attended, both acts.** Both core fixes proven (fix ②
> needed a real `Reloading done in 1358 ms`), archive rebuilt (**80 files, 80
> byte-identical to the tree**), and run B scored **10/10** — including the three
> nobody had ever tested: it loads **`packed`** (66 archived sessions all said
> `unpacked`), the **preview image renders** on the packed path, and **uninstall
> holds for all 75 at once**. ⭐ The 75 module names are **set-identical** packed
> vs unpacked, so packing changes nothing.
>
> ⚠️ **What act 1 got wrong and cost you two launches:** step 5's
> `DbgPackMod(...)` at the console **cannot work** — that function is not in `_G`
> on retail at all, and neither is `ReloadLua`. The blacklist story was never
> about the console. **The route is Mods Manager → Edit (Ctrl-E) → Mod Editor →
> File → Pack Mod**, a menu item with no button, which is why you couldn't find it.
>
> ⛔ **This is not "the upload will succeed."** Nobody logged in, nothing was
> transmitted, no listing exists. Next is the terminal audit, not an upload.
> ⛔ **Your mods are all unticked** — re-tick the fix pack and Test Kit before the
> next session's numbers mean anything.

52. ⛔ **The final release check needs your hands twice, and I can now say exactly
    why nobody has ever run it.**

    **What the check is.** Run B tests the mod the way a *player* receives it:
    squeezed into one archive file and installed like a download, with our test
    kit switched off. Every reading this project owns was taken the other way —
    the mod spread out as loose files through a developer shortcut, with the test
    kit loaded. Your ruling stands: the green test suite is information, **this**
    is the gate.

    **Why it stalled.** To test the archive I first have to *build* it. The
    game's build command, `DbgPackMod`, is on a list of things mod code is
    forbidden to call — so neither our mod nor our test kit can build it — and an
    unattended session cannot type into the console. **Building the archive is a
    console line, the console is you, and the entire gate sits behind it.**

    **And it is two sittings, not one.** The archive cannot exist until you make
    it; the install cannot exist until the archive does; the Mod-Manager tick and
    the "is the picture there" look cannot happen until the install does. I had
    planned this as one visit and that was simply wrong.

    ---

    **⭐ ACT 1 — about four minutes, at the keyboard. Nothing here uploads,
    publishes, or touches either store.**

    Load any save with a real colony (`C47FARM` is fine). Press Enter for the
    console. In this order:

    1. `print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())`
       — must print **`0  false`**.
       ⛔⛔ **CORRECTED 2026-08-19 — this line said `1  false`, and it was
       inverted on the exact thing it exists to catch.** `version` is the third
       digit only (`metadata.lua` holds `'version', 0`, which is what renders as
       1.0.**0**), and the 08-19 console read returned `0 false`. As written, a
       correct `0` would have stopped you for no reason — and a `1`, which **is**
       the 1.0.1 bump this step guards against, would have been read as fine and
       waved through to upload.
       ⇒ **`0` = 1.0.0, which is what you ruled. ⛔ A `1` means the version has
       already moved — stop.** And `IsDirty()` must be **not-`true`**: if it says
       `true`, stop too, because step 5 would force a save and bump it.
       ⛔⛔ **CORRECTED AGAIN 2026-08-20 — the second value was wrong here too.**
       This said *"must be `false`"* and cited a `0 false` console read; **no
       archived log contains that string.** The one reading on record is
       `dirty: nil` (`archive/act1_…15.18.19…:258`), and `nil` is the CORRECT
       clean answer whenever the mod has not been opened in the Mod Editor this
       session (`IsDirty` returns `old_hash and …`, and `old_hash` is unset —
       `CommonLua/GedEditedObject.lua:93-98`). ⇒ **`nil` and `false` both PASS;
       only `true` stops you.** Full reading table: item **70**.
    2. `print(SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order)`
       — expect **`nil  75`**. *(That `nil` is core fix ① proven.)*
    3. `local n = 0 local ok = pcall(function() AllMapsForEach(true, "Colonist", function(c) n = n + 1 if n == 2 then local t t.x = 1 end end) end) print("L5 MapForEach:", ok, n)`
       — three of our repairs walk every colonist and fix what they find. If one
       object goes wrong halfway, does the game skip it and carry on, or silently
       abandon the rest of the list? That loop lives in the game's C code and
       cannot be read. This breaks the **second** item on purpose.
       *`true` and a number above 2* → it carries on, non-issue. *`false 2`* →
       it abandons the rest, and three fixes want a small change next release.
       **Neither answer blocks launch; both are worth having.**
    4. `print("L5 errbox:", config.DisableErrorReporting, ReportedMods)`
       — whether the game's own *"Mod Flagged"* pop-up is even switched on here.
       Expect `nil false` (or `nil nil`).

    ⛔ **Now quit to the MAIN MENU before the next line, and this ordering is not
    fussiness.** Step 5 reloads every script in the game, and nobody has ever
    measured what a mid-game script reload does to a live colony — the two
    sessions in our records that ever did it were both at a menu. Steps 1–4 need
    a colony; step 5 must not have one.

    5. `DbgPackMod(Mods.SMR_CommunityFixPack, false)` — **this builds the
       archive** and forces the second script load. A few seconds. It does not
       upload anything and does not touch either store.
    6. `print(SMRFixPack.fixes.SaintBlessing.status, SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order, #SMRFixPack.UpdateSuspects())`
       — expect **`active  nil  75  0`**. *(The `75` is core fix ② proven — it
       used to become 150. The `0` is the box confirmed not to fire.)*
    7. Optional, ~30 s: `*r SMRTest.RunAll()` — a prediction nobody has tested:
       **2 false failures** after a reload. Either answer is worth having.

    **Then quit the game and paste me what 1–4, 6 and (if you ran it) 7 printed.**
    Anything other than the expected values is a launch-blocker and I want to see
    it before anything is uploaded.

    ⚠️ **Your autosaves are already copied** — both `Autosave Sol 406/411`,
    byte-verified, parked outside the save folder — so act 1 is safe to start
    whenever you like.

    ---

    **BETWEEN THE ACTS — my side, no time from you.** I check the archive holds
    exactly the 80 files it should and that packing altered none of them, then I
    install it the way a download installs and take the developer shortcut out.
    *(Both checks are already built and already proven against the archive you
    made on 08-17 — see the note at the bottom.)*

    **⭐ ACT 2 — about three minutes, and this one is looking, not typing.**

    1. Start the game → **Mods** → untick and re-tick **"Relaunched Fix Pack"** →
       ⛔ **and untick "Community Fix Pack — Test Kit" and leave it off** →
       close the dialog → **restart the game**. Unavoidable: taking the shortcut
       out costs the mod its enable and putting things back does not buy it back
       (item 45, and the same thing that bit the Opt-In pack in item 43).
       ⛔⛔ **THE TEST-KIT UNTICK WAS MISSING FROM THIS STEP UNTIL 2026-08-19 AND
       ITS ABSENCE WOULD HAVE VOIDED THE WHOLE GATE.** Run B *is* "test kit off"
       by definition (`00_CHAIN_SPEC.md` §6) — with the kit left on you get a
       packed run A, which is not the configuration a player receives and not the
       thing this gate exists to test. Steps 2 and 3 below both already say
       *"with the kit off"*, so the script assumed the untick it never asked for.
       ℹ️ The Opt-In pack needs no action — it is already off and stays off.
    2. **While you are on that screen, three looks, all free:**
       - **Is there a picture** beside the Relaunched Fix Pack entry? That image
         path was hand-written against the loose-files install and **has never
         been seen on the packed one**.
       - Does the version read **`1.00-000`**? ⚠️ **Corrected 2026-08-19 — this
         said "1.0.0", which that screen never prints.** The Mods Manager was
         seen tonight rendering `version 1.00-000`, because `GetVersionString`
         is `"%d.%02d-%03d"` (`Mod.lua:1176-1178`). `1.00-000` **is** 1.0.0 under
         that format and is the PASS; the plain `1.0.0` is a different surface.
         ⛔ A `1.00-001` means the version moved — stop.
       - **Anything of ours on screen that should not be** — a dialog, a
         notification? ⚠️ Expect the game's own *"Welcome to Mars, Commander!"*
         box when a game starts: that one is vanilla, our test kit has been
         hiding it for every unattended run, and with the kit off it is back.
         **It is not ours and not a failure.**
    3. Then load a **named** save (not an autosave), let a few sols pass, save
       under a **new** name, and load that back. That is the save round trip, and
       with the test kit off it cannot be scripted — it has to be you.
    4. Quit, tell me it is done, and I read the log and score the gate.

    ---

    ⛔ **What no part of this touches: Paradox or Steam.** The first call to
    either store's API *creates the listing* — there is no "everything but the
    last click" — so the rehearsal goes nowhere near one, by design.

    ℹ️ **What I did get done without you tonight**, so act 1 is the only thing
    standing between us and a scored gate: the pre-upload check passes all 20
    guards; the archive's expected contents are now predicted by a tool that
    reproduces your 08-17 archive exactly, 80 files out of 80; **packing was
    proven not to alter a single one of our files** (78 of 80 byte-identical to
    disk, and the 2 that differ are exactly the two files we have edited since);
    and **four of the gate's ten pass criteria were repaired before anyone scored
    them** — one asked for a number the game never prints, one had arithmetic
    that would have sent a runner hunting a module that does not exist.

### ⚠️ 2026-08-19 — two calls from the last sweep link. Neither blocks launch; one is a wording call, one is a "when", and my recommendation on the second is *not yet*.

50. ⚠️ **Two sentences we publish promise other mods more than the code delivers.
    Your call on the wording; nothing else changes.**

    **What we say.** The README's "For modders" section says the pack will
    *"chain rather than clobber"*, and the top of `Code/00_Core.lua` — which ships
    inside the mod, so a curious modder reads it — says fixes *"prefer
    wrapping/chaining originals over replacement, **so other mods that hook the
    same functions keep working**."*

    **What the code does.** I counted it, mechanically, for the first time: of the
    66 places the pack patches something, **42 chain** (they call the original, so
    another mod's version of that function still runs) and **24 replace it
    outright** (they don't, so it doesn't). That is 11 of the 16 global functions
    and 13 of the 50 class methods.

    ⛔ **This is not a rule being broken.** Our own house rules explicitly allow a
    full replacement when the bug sits mid-function and can't be hooked, and they
    already warn that those are *"the fixes most likely to clash with other
    mods."* Every replacement I sampled carries the header the rule demands,
    naming the game file and lines it was copied from. These are deliberate,
    documented decisions and **I am not proposing to change any of them.**

    ⭐ **What is new is the number.** The rule says "keep the list short" and
    nobody had ever counted the list. 24 is the count. Whether 24 is short is your
    judgement, not mine.

    ⇒ **The decision is only about the two sentences.** The first ("chain rather
    than clobber") describes a preference as if it were a practice. The second is
    the one that actually matters, because it promises an **outcome for other
    mods** — and that outcome is true at 42 sites and false at 24.
    **Recommendation:** soften the `00_Core.lua` sentence to say the pack chains
    *where it can* and copies a corrected body where the bug can't be hooked. It
    costs one line, it is true, and it is the sentence a modder quotes back at us
    if something clashes. ℹ️ Same visit could carry the veto-snippet wording note
    below.

    ⚠️ **A smaller one riding along, same file.** The README says to disable a fix
    by *"setting a fix's identifier in that global table."* Read literally that
    invites `SMRFixPack_Disabled = {"DustDevilSpawnGate"}` — a **list** — which is
    a perfectly valid table, throws nothing, logs nothing, and **does not disable
    anything.** The person walks away believing they turned a fix off. The example
    directly under that sentence is correct; the sentence above it is what misleads.
    One clarifying half-sentence fixes it.

51. ⚠️ **There is one test worth running that I could not run, and my
    recommendation is to run it AFTER launch, not before. Your call on the timing.**

    **The test.** Every claim this pack makes about getting along with other mods
    is derived from reading code. Nothing has ever been *watched* — no second mod
    has ever been in the process while we measured anything. The one second mod we
    can legitimately use is **our own opt-in pack**, which patches two of the same
    functions the fix pack patches. A single unattended run with both loaded would
    be the only time this project ever sees two independently-written patches
    stacked on one function.

    **Why I did not run it.** The opt-in pack is currently switched off in your
    account, and putting a mod's folder back does **not** switch it back on — that
    takes you ticking it in the Mod Manager and restarting. That is a cost only you
    can pay, and spending it unattended is the one thing our own hazard list says
    never to do.

    ⇒ ⛔ **Recommendation: don't do it yet.** The final release test ("run B")
    needs the opt-in **off**, and it is the gate. This compatibility test is
    information, not a gate — by your own ruling. Turning the opt-in on now means
    turning it off again before run B, for a result that cannot block the launch
    either way. **Cleanest order: run B first, launch, then this.**
    ℹ️ Nothing owed today. The tick itself is still owed whenever you next open the
    Mod Manager (that is item 43); this just says what it would buy.

### ⚠️ 2026-08-19 — the SAME defect class, in the third mod. Not today's problem; do not let it be forgotten.

48. ⚠️ **The Save Rescue mod has no `items.lua` at all**, against a 2-entry code
    list (`Code/00_Core.lua`, `Code/10_SaveRescue.lua`). Item 46 explains why that
    file matters: uploading forces the editor to save, and the save **rebuilds the
    list of code files to load from the items file alone — it never looks at the
    disk.** The fix pack had one item missing and would have shipped a fix that
    never loaded. The rescue mod has **no items file whatsoever**.

    ✅ **This does not touch tonight.** The rescue mod is the held-in-reserve
    contingency (item 17) and is not publishing. The opt-in pack was checked and is
    **correct** (9 for 9).

    ⛔ **But it must be settled before that mod ever uploads**, and the sweep
    chain's own rules forbid its sessions from touching sibling repos, so this
    would otherwise be lost. ⚠️ I have **not** derived what the game actually does
    when the file is absent — it may refuse to rebuild rather than rebuild empty,
    which would be harmless. **That question is the work**, and it is twenty
    minutes with the source, not a guess to be recorded as a fact.

    ⇒ **Folded into your item 37 Q1** (*"mirror the core fixes into the opt-in pack
    now, or leave them?"*): whatever you rule there, the same visit should carry
    this. **Recommendation unchanged — do the sibling work in one pass**, while the
    diagnosis is fresh, rather than making each mod's launch session rediscover it.
    ℹ️ Nothing owed beyond that ruling.

    ⚖️ **RULED 2026-08-20: record it as a gate in that mod's own repo, do not
    derive it now.** Written into `SMR-CommunitySaveRescue`'s `CLAUDE.md`
    (`9c912b3`) — the undecided consequence is carried openly as undecided, and
    the source path for whoever discharges it is pasted in. Receipt: **item 55**.

### ⚠️ 2026-08-19 — the launch test's own first question could not fail. Already fixed; nothing owed unless you disagree.

49. ⚠️ **The final launch test had a check that was incapable of failing, and I
    changed it.** ⇒ **Nothing to do** — this is the "what happened" note, and a
    single call is yours only if you dislike the change.

    **What happened, in plain words.** Before this mod goes out, there is a final
    test — "run B" — that loads the mod **the way a player receives it**: zipped
    into a single package file, rather than through the shortcut we develop
    against. It has ten pass criteria and the **first** one is *"the mod loads
    packed"*, because if that is wrong, the other nine measured the wrong thing.

    The way that first check was written, it was satisfied by *"the mod printed
    its usual lines in the log"* — which it does **either way**. So if the
    shortcut had been left in place by mistake, the test would have quietly
    measured our development copy, ticked the box, and every number after it
    would have been wrong while looking right.

    **What I changed.** The game itself writes down which way it loaded the mod,
    in one log line, in plain words: `packed` or `unpacked`. The check now reads
    that line. ⭐ **And I checked our own history: 66 recorded sessions carry that
    line, and all 66 say `unpacked`.** So "this mod has never once been loaded
    the way a player will load it" is no longer something we believe — it is
    something the logs say, in a line anyone can search for.

    I also wrote down a related trap in the test's instructions: if the shortcut
    **and** the packaged copy are both present, the game silently prefers the
    **shortcut**. So "remove the shortcut first" is not tidiness, it is the
    difference between a real test and a fake one.

    ℹ️ **The only thing that is yours:** if you would rather the first check stay
    loose, say so and I will put it back. Otherwise nothing is owed here.

### ⛔⛔ 2026-08-19 — the upload would have shipped one fix missing, on Steam. Already fixed; two small wording calls are yours.

46. ⛔⛔ **A fix would have vanished from the Steam release, and the check that
    was supposed to catch it said "pass".** ⇒ **Nothing to do — it is fixed and
    pushed.** This is the "what happened" you asked to always get.

    **What happened, in plain words.** The mod carries two lists of its own code
    files. One is the list the game reads to decide what to load; the other is
    the list the in-game Mod Editor keeps. They are supposed to be identical.
    When the automation-law fix was built on the 15th it went into the first list
    and nobody added it to the second. **The Mod Editor rebuilds the first list
    from the second every time it saves** — and *uploading* forces a save. On
    Steam that save happens **before** the mod is packed, so Steam would have
    received a mod that simply does not contain the automation-law fix. Paradox's
    very first upload would have escaped, because its save happens afterwards —
    but that save still rewrites the folder on your disk, so the Steam upload
    that follows, and every future update to either store, would have shipped
    without it.

    **Why it wasn't caught.** `tools/upload_preflight.py` has a guard for exactly
    this. It counted the words "ModItemCode" in the file — and one of those words
    is in the **comment at the top of the file explaining the guard**. 75 real
    entries plus one comment made 76, which matched, so it printed PASS. Two
    mistakes cancelling each other out. The guard now reads the actual entries
    and checks their order too, and I proved it by putting the fault back (it
    fails, and names the file that would have gone missing) and by scrambling the
    order (it fails, and says so).

    ⚠️ **The same broken arithmetic was reporting a *phantom* problem on the
    Opt-In pack**, whose list is in fact correct. That is fixed by the same
    change. And the Save Rescue mod has **no** editor list at all — probably fine
    for a different reason, but I did not verify it and it is not this chain's
    repo to touch. Worth one look before it ever uploads.

47. ⚖️ **Two wording calls on the modder page — your call, ten minutes, and
    neither blocks launch.** Both are on `README.md` and the site's
    "For modders" page, which say the same thing in the same words.

    **(a) The example code we publish trips the game's own strict-globals
    check.** We tell a modder to write
    `SMRFixPack_Disabled = SMRFixPack_Disabled or {}`. Reading a name that does
    not exist yet is exactly what the game complains about — and our own code
    never does it: every place the pack reads that table it uses the safe form,
    `rawget(_G, "SMRFixPack_Disabled")`. The snippet still *works*; the cost is a
    line in the log, and I could not establish whether the retail build even
    prints it (the one time we have seen it was a debug build). **Suggested:
    publish the safe form, since it is the same one line our code already uses.**

    **(b) The page tells a modder the load order does not matter, and it does.**
    It says it *"does not matter whether yours or ours is created first — only
    that the values are set before our code runs."* Both halves are true, but
    together they require the modder's mod to load **before** this one — which is
    the player's enable order, with no priority field and no way to ask for a
    position. **Suggested: say that plainly on the modder page.** ⚠️ This is a
    *modder*-facing page, so it does not touch your standing rule that players
    never get load-order advice.

### ⚠️ 2026-08-19 — run B now has an ATTENDED moment in it. Nothing to decide; something to know.

45. ⚠️ **The launch rehearsal is no longer zero-cost to you, and finding that out
    early is the good news.** The verification launch measured something nobody
    knew: **pulling a mod's junction disables it in account state, and putting the
    junction back does NOT re-enable it** — proven across two relaunches, and the
    mod vanishes *silently*. Run B was written to pull the fix pack's junction the
    same way, so as designed it would have shown the pack **absent** and read as a
    catastrophic failure of the mod — when it was a failure of my procedure.
    ⇒ Run B now budgets **one Mod-Manager tick from you** after the swap, and
    reads the gate line before believing any other number.

    ⭐ **Two console lines ride along on that same visit, and they are the last
    outstanding verification of the two fixes that paused this upload.** The
    console is blacklisted in unattended runs, so this visit is the only place
    they can happen — and they now cost nothing extra:
    `print(SMRFixPack.fixes.SaintBlessing.update_suspect)` (expect `nil`) and a
    duplicate check on the module list after forcing a second script load.

    ⛔ **Why they were not done already, and it is not an oversight:** the
    falsifier I wrote for those fixes could not work. It used the pack's own
    `UpdateSuspects()`, which reads the suspect mark **only** on modules that are
    switched off — so a stale mark on a *working* module is invisible to it. The
    verification session ran it, got a clean `0`, and **refused to call the fixes
    verified**, which is exactly right and better than the brief it was given.

    ℹ️ **Nothing owed by you** beyond being at the keyboard for that one moment.

    ⚖️ *Recorded so nobody does it casually later:* the obvious permanent fix —
    add a Test Kit probe that checks this every run — is **post-launch work**.
    Adding a probe moves the suite count 96 → 97, and *"a suite of 96 checks"* is
    printed on the store card. That number has already been wrong twice.

### ⛔⛔ 2026-08-17 — THE UPLOAD IS PAUSED ON YOUR OWN WORD. Two defects found at the sitting and fixed; two questions for you.

37. ⛔ **What happened, in plain words.** You opened the Mod Editor to upload,
    and a dialog appeared from the *other* mod saying *"2 of this mod's modules
    found that the game code they patch has changed… Switched off: NoHomeless,
    NoHomeless"*. You asked whether that was only there because the opt-in mod
    was switched on. It was — five separate controls confirm it, and **a player
    installing the fix pack alone could never see that particular box.** But
    reading *why* it said the same name twice found **two real defects in code
    the fix pack ships too**, and you overrode the recommendation to ship and
    fix later: *"I don't want to launch with an immediate planned 1.0.1 fix
    routed for launch. I want us to be clean period."* Both are now fixed.

    * **The false alarm.** A module that fails one start-up pass and succeeds on
      the next — normal, documented, happens every launch — kept a "suspect"
      mark that nothing cleared. Any later stand-down then read that stale mark
      and would have shown a player a box on a **brand-new release** claiming
      the game's code had changed and inviting them to go find a newer version,
      about a fix that had just worked. It never fired, by timing rather than by
      correctness. ⛔ It would have been a bad first impression that was also
      simply false.
    * **The double name.** Our own registry appended a module twice whenever the
      game reloaded its scripts, so one module was counted and listed twice.
      That is why it said "2" and named NoHomeless twice when only one module
      had stood down.

    ✅ **Both fixed in `Code/00_Core.lua` (`2f077e8`); `metadata.lua` untouched,
    so this is NOT a 1.0.1 — nothing has been published, and 1.0.0 is simply
    what 1.0.0 now is.** ⛔ **Nothing is verified yet in a running game**, and
    the release tag is deliberately parked one commit behind until it is.

    ⭐⭐ **Your chain is built and waiting: `agent/prompts/prelaunch-sweep/`** —
    your design, *"a chain that is self replicating… it doesn't stop until a
    chain finds nothing,"* with three changes I'd argue for and you can overrule:

    * ⛔ **Blinding the next session does not work in this repo** — our own rules
      make it read `git log` and STATE, and our commit messages are essays. So
      links are blind on **findings** (`SWEEP_FINDINGS.md`, forbidden) and
      sighted on **coverage** (`SWEEP_LEDGER.md`, required). Chain commits use
      deliberately boring one-line subjects so a staleness check can't leak.
    * ⭐ **Vary the question, not the sweep.** Eight lenses, one per link. The
      reason is your own observation: tonight's finds came from asking something
      no brief had asked, not from sweeping harder. Five identical sweeps mostly
      re-cover the comfortable ground.
    * ⚠️ **"Until one finds nothing" is not safe on its own** — silence has two
      causes, and one of them is a shallow sweep. So it stops on *nothing new in
      **unswept** territory*, or two cosmetic-only links, or a cap of 5 — and the
      terminal audit must **name which**, because reporting a cap as a clean bill
      is the worst thing this design could do.

    Links 1–2 may fix; 3+ record only (each fix adds risk to a release
    candidate), except launch-blocking findings, which are fixed at any link.
    **Each link reports to you and stops; you kick off the next.** The Fable
    terminal audit reads everything, re-reads today's fixes hostilely, does its
    own final sweep, and issues the upload verdict.

    ⭐ **Plus the two things you added, which are the best part of it.** The
    launch **dry run** (`98_LAUNCH_REHEARSAL.md`): ⛔ nothing may touch a portal
    API — the first API call is the one that *creates the listing*, so "every
    step up to publish" isn't the safe line — but the upload's **validation** is
    separable from its transmission, so `tools/upload_preflight.py` now runs all
    six Paradox guards plus Steam's size limits locally, **in seconds, forever.**
    I proved it catches tonight's blocker by deleting the field again. And your
    A/B call is written in as you framed it: **A is information, B is the gate.**
    ⛔ B is the first time in this project's history the mod will be run the way a
    player receives it — **packed, junction pulled, TestKit and opt-in off.**
    Every gate number we own was taken unpacked with a third mod loaded that
    rewrites globals.

    ❓ **Q1 — mirror the two fixes into the opt-in pack now, or leave them?**
    Both defects are identical in that mod's own core — it is where the dialog
    came from. It is parked and not uploading, so this does not gate tonight.
    **Recommendation: yes, now**, while the diagnosis is fresh; the alternative
    is that its launch session rediscovers this from scratch. ⚠️ Its own gates
    would need re-running, which is why it is your call and not mine.

    ⚖️ **RULED 2026-08-20: yes, mirror them.** Done in `SMR-OptInPack`
    (`2cedf7d`), nothing in this repo touched — the receipt, including what is
    measured there versus pre-emptive, is **item 55**.

    ✅ **Q2 — Steam's version number: CLOSED, no decision needed.** Retired by
    circumstance at the 08-20 dual upload, and doubly moot since: from the 08-24
    sitting on, an UPDATE bumps once and Steam packs after Paradox's save, so
    **both listings now ship the same `version` 4** — measured in the delivered
    Steam archive 2026-08-29 (`EF-068`). ⇒ item 37 is closed in full.

    <details><summary>The original question</summary>

    ❓ **Q2 — Steam's version number.** ⛔ Decide **after** Paradox, not now.

    </details>
    Paradox Mods saves *after* it uploads, so it receives a clean **1.0.0**.
    Steam saves *before* it packs, so a straight second upload would ship
    **1.0.1**. Getting Steam to 1.0.0 as well costs one extra restart and a
    one-field edit. **Recommendation: take the extra restart** — you ruled a
    clean first number for exactly the reason it is worth keeping on both
    stores — but it is genuinely a shrug either way and you lose nothing by
    deciding when you get there.

### ⛔ 2026-08-19 — THE VERIFICATION LAUNCH RAN: the mod is running clean in a real game. Nothing blocks launch. Two things need your hands, and one of them is a mess I made.

43. ⛔ **I broke the Opt-In pack's enable state, and I could not put it back.**
    Telling you straight, the way the autosave deletion was told to you.

    To run the suite "as a player will have it" I needed the Opt-In pack absent.
    Changing that switch properly needs the Mod Manager, which needs you — so I
    used the documented reversible trick instead: remove the folder shortcut, let
    the game not find it, put the shortcut back afterwards. **The putting-back
    did not work.** The game now sees the Opt-In pack sitting there, lists it,
    and **never runs a line of it**. I relaunched twice to be sure. Our own notes
    said this could happen; they blamed it on a Mod Manager visit in the middle,
    and there wasn't one this time, so the note was wrong about why.

    **The fix is one minute of yours and there is no other route:** open the game
    → **Mods** → untick and re-tick **"Relaunched Fix Pack: Opt-In Modules"** →
    close the dialog → **restart the game**. If it comes back, its own line in
    the log reads `opt-in pack present: 8/8 modules active`.

    ⚠️ **The Fix Pack itself is completely unaffected** — it ran perfectly in all
    three launches. And this is worth knowing before launch day for a second
    reason: **the final release check (run B) plans to pull the Fix Pack's
    shortcut exactly the same way.** If it does that, the packed mod may sit
    there not running, and the check would look like a disaster that is really
    this same switch. That is now written into the rehearsal's own notes.

44. ⭐ **Two minutes at the keyboard finishes the two core fixes — four sessions
    have now been unable to.** The two defects you paused the upload over were
    fixed on 08-17 and have **still not been proven fixed**, and I can now say
    exactly why: proving them needs the game's console, and an unattended
    session cannot type into it. Everything else about them is done.

    The good news first: **the fixed code definitely runs.** In tonight's
    launches the exact sequence that used to leave the false flag behind played
    out in the log, the repair line executed, and the module ended up healthy —
    all 75 fixes active, no error, no box on screen. What I cannot read from
    outside the game is the one leftover flag itself, and whether the second
    defect (a fix being counted twice) is gone, because that one only shows up
    when the game reloads its scripts mid-session.

    **The recipe. Any save, any colony, press Enter for the console, type these.**

    1. `print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())`
       — must print **`1  false`**. ⛔ If it says `true`, **stop and tell me**:
       the next line would bump us to 1.0.1 and you ruled 1.0.0.
    2. `print(SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order)`
       — expect **`nil  75`**. *(That `nil` is core fix ① proven.)*
    3. `DbgPackMod(Mods.SMR_CommunityFixPack, false)` — this is the reload. It
       does not upload anything and does not touch either store.
    4. `print(SMRFixPack.fixes.SaintBlessing.status, SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order, #SMRFixPack.UpdateSuspects())`
       — expect **`active  nil  75  0`**. *(The `75` is core fix ② proven — it
       used to become 150. The `0` is the box confirmed not to fire.)*
    5. Optional, ~30 s, and it settles a prediction nobody has ever tested:
       `*r SMRTest.RunAll()` — link 2 predicted **2 false failures** after a
       reload. Either answer is worth having.

    **Paste me back what those four lines printed and the core fixes are closed.**
    Anything other than the expected values is a launch-blocker and I want to see
    it before you upload anything.

    ⭐ **Two extra lines, ~20 seconds, added 2026-08-19 by the failure-and-
    containment sweep — same sitting, nothing else needed.** Neither changes
    anything; both just print. They are optional, but line 6 is the only way to
    settle a question three of our fixes depend on.

    6. `local n = 0 local ok = pcall(function() AllMapsForEach(true, "Colonist", function(c) n = n + 1 if n == 2 then local t t.x = 1 end end) end) print("L5 MapForEach:", ok, n)`
       — **what it means.** Three of our repairs walk every colonist (or every
       track piece) in the colony and fix what they find. If one object goes
       wrong halfway through, does the game skip that one object and carry on, or
       does it silently abandon the rest of the list? Nobody knows, because that
       loop lives in the game's C code and cannot be read. This line deliberately
       breaks the **second** item and prints what happened.
       *`true` and a number bigger than 2* → it carries on, and this is a
       non-issue. *`false 2`* → it abandons the rest, and three of our fixes want
       a small change before the next release. **Either answer is worth having**;
       neither is a launch-blocker.
    7. `print("L5 errbox:", config.DisableErrorReporting, ReportedMods)`
       — the game has its own pop-up that says *"Mod-related problem detected…
       Mod Flagged: Relaunched Fix Pack"* whenever a script error touches our
       folder. We only found it this week and it has **never fired** in any of
       our 73 recorded sessions. This prints whether it is switched on at all on
       your machine. Expect `nil` and `false` (or `nil nil`).

### ✅✅ 2026-08-18 — STATE.md WAS EVICTED ON YOUR DIRECTION, AND YOU RULED THE CAPS THE SAME DAY. Nothing here is owed from you.

42. ⭐ **What happened.** The agents' one mandatory-read file had quietly grown
    to **~130KB (~33,000 tokens)** — every session paid that before doing any
    work, and its 60-line budget was being satisfied while being defeated
    (single lines had become thousand-word walls). On your direction it was
    evicted: STATE.md is now a kernel (current position · hazards · your
    rulings in force · pointers), the six days of closed history moved to the
    session log as digests with grep tags, nothing was deleted (the full old
    file is readable forever via git), and a standing cleanup prompt
    (`agent/prompts/STATE_EVICTION.md`) exists so you can fire future
    evictions with one line.

    **The measured numbers you asked for: old file 71,077 bytes = 33,066
    tokens (its emoji-heavy prose cost ~2.2 bytes/token); clean kernel 4,524
    bytes ≈ 1,200–2,000 tokens** — a 16–27× cut.

    ✅✅ **RULED SAME DAY** — you asked whether the line budget still matters
    (*"Is the line budget even important anymore if we are capping the token
    size?"*) and ruled: *"format it in the most efficient and safest way
    possible because the token cap will do the read job."* **Applied:** the
    60-line budget is RETIRED; doccheck now enforces **warn 9KB** (the flag
    line must be copied verbatim into your after-run report; you fire the
    eviction prompt at your leisure), **hard 18KB** (commit blocks — even
    ignored, a boot read stays under ~8,400 tokens at the old file's worst
    density vs this week's 33,000), and a **200-byte per-line cap** so walls
    can never return inside the budget. STATE.md was reflowed to
    one-fact-per-line, the eviction prompt carries your formatting rule, and
    both new checks were falsifier-proven before this note was written. All
    three numbers are adjacent constants in `tools/doccheck.py` — retuning
    is one edit whenever you want.

### ⭐ 2026-08-18 — SWEEP CHAIN, LINK 4 REPORTED. Nothing blocks launch. No code changed. One wording call, and one bigger question about the chain itself.

41. ⭐ **Link 4 — lens 4 of 8, "player experience".** The question: **what does a
    player actually SEE and READ?** The answer should be *nothing*, and it very
    nearly is — the pack raises **no** notification, popup, banner or voice line
    of its own. Everything it can put on screen is a box the game already owns.

    **But there is one place the mod speaks in its own voice**, and it is the box
    you saw at the upload sitting: the message that appears when a fix has stood
    itself down after a game update. **Two things about its wording need you,
    because it is the mod's only voice — and on Xbox and PlayStation it is the
    only thing a player can ever see from us at all** (no log, no console there).

    * **It lists our internal file names, not the fixes.** It would say
      *"Switched off: AstrogeologistExtractors, SaintBlessing"*. Those names
      appear on **no page a player can reach** — not the mod page, not the fix
      list, not the FAQ. Meanwhile every one of the 75 modules already carries a
      plain-English title in the same style the fix list uses ("Command Center
      graph captions count maintenance, like the bars do"). We have the readable
      version and print the unreadable one. *(Same trap as the Bottomless Pit
      building that actually displays as "Experiment 1: Big Drop".)*
    * **If one of our fixes crashes, the box blames the game.** The message is
      one sentence covering every reason a fix switched off, and it says the game
      code "has changed — usually after a game update" and tells the player to go
      look for a newer version of our mod. That is right when a patch really did
      move something. It is **wrong** when the cause was a bug in **our** code or
      a clash with another mod — we would be pointing at Paradox for our own
      mistake and sending the player after a version that does not exist.

    ⛔ **Neither can happen today** — this box has never once appeared in any of
    the 57 recorded sessions, and no fix has ever crashed in one. This is about
    what it would say on the day it does.

    **Recommendation: fix both, in the terminal audit, as one small text change**
    — print the readable titles, and say "switched themselves off" without
    blaming a game update unless we actually detected one. It is words only, in a
    box no player has yet seen, so the risk of touching it is about as low as a
    code change gets. Say the word and it goes in the audit's list.

    **Nothing else needs you.** A third finding — our log never writes a line when
    a fix *recovers*, so 56 of 57 recorded logs end up saying a module is switched
    off when it is actually working — is a plain repair with no decision in it,
    and it is routed to the audit. Three other things were checked and came back
    clean: the mod-page claim that *every* fix inspects the game's code first is
    true for all 75 (checked one by one); the "five judgment calls" count matches
    on every surface; and the box's plumbing was traced through the game's own
    code for the first time and works.

    ⭐⭐ **The bigger question — and it is a real one.** Your chain has a cap of
    **five** links, and I am the fourth. **Four of the eight lenses would still be
    unasked**, and each of the remaining three owns a job with a track record:
    the "does the mod promise anything it doesn't deliver" lens (we have found
    that class of mistake **four** times now, most recently this session); the
    "packed install" lens, which covers the fact that **the mod has never once
    been loaded the way a player will load it**; and the "another mod is
    installed too" lens, which link 1 explicitly left 15 unchecked items for.

    **Recommendation: raise the cap to 8 and let the rotation finish.** Your own
    spec says stopping because you hit the cap and calling it "we found
    everything" is the worst thing this design can do — so I am saying plainly
    that I do **not** think one more link closes it. Each link is unattended and
    costs you only the moment you spend kicking it off.

### ⭐ 2026-08-18 — SWEEP CHAIN, LINK 3 REPORTED. Nothing blocks launch. No code changed. One call for you, and it is a small one.

40. ⭐ **Link 3 — lens 3 of 8, "save & exit".** The question: **not "is each fix
    save-safe" — every module was checked alone — but "what does the whole pack
    put into one savegame, and what happens to all of it at once when someone
    removes the mod?"** Nobody had added them up.

    **The one thing that needs you.** The pack keeps a small amount of its own
    bookkeeping inside your savegame — eleven named items, and our own rule says
    every one of them must be called `SMRFixPack_something` so that a sweep can
    find them all. **One does not follow that rule.** A single flag written by
    the Shuttle Hub fix is called `smr_shuttles`, and because our master list of
    "everything of ours that ends up in a save" was built by searching for the
    `SMRFixPack_` name, that one item was never on the list — the list even says
    explicitly that the place it lives contains *"nothing of ours"*.

    ⛔ **It is harmless, and I want to be plain about that before the question.**
    It is one true/false value tucked onto a cache entry. The game ignores it
    completely when the mod is gone, and the whole cache it sits in is thrown
    away and rebuilt the next time a dome is connected or a train route is
    rebuilt — so it does not even survive long. It changes nothing a player can
    see, and it does not block launch.

    ❓ **The call.** Your own hard rule from 2026-08-01 is that *every* place the
    mod can leave something in a save gets a written decision — and a place with
    no written decision blocks release by default, whichever way the decision
    goes. This one now has a written decision (it is recorded, with its reasons,
    in `agent/reports/L3_SAVE_FOOTPRINT.md`). So:

    * **(a) Accept it as recorded — RECOMMENDED.** The decision is written, the
      thing is harmless and short-lived, and nothing in the shipped code changes.
      This is the cheapest option and it satisfies the rule as you wrote it.
    * **(b) Rename it to `SMRFixPack_shuttles` first.** One word in one line of
      one file. It buys tidiness — every future sweep would find it — at the
      cost of touching the release candidate again, which is the thing you have
      been deliberately not doing.

    ⚠️ I could not make this change myself either way: from link 3 onward the
    chain only records what it finds, so that the final review sees every finding
    together before anything is edited.

    **Four smaller things found, all recorded, none needing you.** A comment in
    the meteor fix says one of our savegame flags *"stays in your save after
    uninstall"* — it does the opposite, the game drops it, so we have been
    describing more leftovers than we actually leave (the player-facing uninstall
    text already had this right). The knock-on: uninstalling and later
    reinstalling re-rolls the meteor timer once, which is bounded and arguably
    what you would want anyway. The savegame-repair module sets its "already
    done" marker *before* doing the work, so if a future game update ever moves
    the two functions it needs, it would mark the save done without having done
    it. And a comment in that same module lists 8 fixes as carrying their own
    load-time repair when the real number is 17 — one of the 8 no longer exists
    as a module at all.

    ⭐ **One genuinely good result worth telling you.** An older audit left an
    open question about three of our background timers having no "the mod is
    gone, stop cleanly" guard. All three have one now — checked by reading the
    code, not by trusting the notes — and across all six of the pack's background
    timers there is exactly one without a guard, which has a written decision
    already and cleans up after itself regardless. That question can be closed.

    ⛔ **What I could not reach, so you know what this did not cover.** Nothing
    was run in a game — no save was opened and nothing was weighed, so every
    *measured* number in this area is still the older one. Of the 18 repair
    passes that run when you load a save, I cross-checked 5 against the game's
    own 237 built-in save repairs; the other 13 are unchecked for interference.
    And nobody has ever actually walked an uninstall, let alone a reinstall.

### ⭐ 2026-08-18 — SWEEP CHAIN, LINK 2 REPORTED. Nothing blocks launch. One real defect found and fixed; one small call for you, and it can wait.

39. ⭐ **Link 2 — lens 2 of 8, "lifecycle & idempotency".** The question: **what
    happens the second time our code runs in one session?** The game re-runs every
    mod's scripts whenever you close the Mod Manager after changing anything — so
    "the second time" is not a corner case, it is what happens to any player who
    turns on a second mod.

    ⛔ **It found a real one, and it was already sitting in your own logs.** Two
    archived sessions — both ones where you took a Mod-Manager tick — show the
    pack loading **twice**. Comparing the two halves of those sessions gives the
    same answer in both, and it is the *entire* difference between them:
    **four modules switch themselves off the second time, each giving a reason
    that is not true** — *"the shipped presets are already correct"*, *"the
    shipped tech already matches its own param1"*, and two more like it. The data
    **is** correct, because those four modules corrected it the first time round
    and the correction survived the reload. What did not survive was each module's
    memory of having made it.

    **Why it matters, and it is not the wording.** Three of our *save-repair*
    passes only run while their module reads "on". So a player with an older save
    who happens to have visited the Mod Manager that session silently does not get
    the Astrogeologist extractor bonus applied to their existing colony, does not
    get the Independent Terraforming discount corrected from 10% to the 20% it
    advertises, and does not get their dome Saints' blessing re-filed. Nothing
    errors, nothing is shown, it just quietly doesn't happen.

    ✅ **Fixed in `Code/00_Core.lua`.** The "have I already changed this data?"
    memory now lives for the whole session instead of for one script load.
    ⛔ `metadata.lua` untouched, no module added or removed, every count unchanged
    — this is still 1.0.0.

    ✅ **It is a relative of the two defects from your upload sitting, but not the
    same one, and the good news is that your dialog cannot fire from it** — all
    four of these stand-downs are the flavour the code marks "harmless", so no
    player sees a "check for a new version" box because of it.

    **Proven, not asserted:** I built a harness (`tools/l2_reload_sim.py`) that
    runs the pack's own shipped code twice in one process. Before proving anything
    it has to earn trust, so first it reproduces your two archived sessions
    exactly — all five of their first-load lines, word for word, and all four of
    the false second-load lines. Then: with the fix in, the four false lines are
    gone and all four modules stay on. And a control in the other direction — if a
    future game patch genuinely fixed this data itself, all four still correctly
    say "already correct". ⛔ **This is not a launch.** It runs our real code
    against a stand-in for the game.

    ❓ **The one call for you (it can wait, and "leave it" is a fine answer).**
    Our "some fixes switched themselves off" dialog is created fresh each time the
    game reloads scripts. So if that dialog ever *does* have something to say,
    a player who opens the Mod Manager again gets shown it **again**. The code's
    own comment calls it "a one-time dialog", so today it doesn't do what it says.
    **Recommendation: show the box at most once per session, keep writing the line
    to the log every time** — that keeps the diagnostic and drops the repeat.
    ⚠️ I did **not** just do it: it changes what a player sees, in a release
    candidate, and it is a judgment call about what the pack *should* do rather
    than a defect. Also worth knowing: that dialog has **never once appeared** in
    any of the 58 logs we have archived.

    ⛔ **What link 2 did NOT look at.** Nothing was run in a game — so the fix
    above, and both of the 08-17 fixes, still have not executed inside Surviving
    Mars even once. I have written down the shape of the single unattended run
    that would verify all three at the same time, but I did not build it. Also
    untouched: a third-and-later reload, whether a reload can happen mid-colony,
    the TestKit's own behaviour, save footprint and uninstall, what a player sees,
    failure containment, packed-vs-unpacked, and any other mod. **Two lenses of
    eight. The chain has not converged.**

### ⭐ 2026-08-17 — SWEEP CHAIN, LINK 1 REPORTED. Nothing blocks launch. One small call for you, and it can wait.

38. ⭐ **Link 1 of your chain is done — lens 1 of 8, "structure & collision".**
    The question it asked, which no brief here had asked before: **do our own 75
    modules step on each other?** To answer it properly I built the thing the
    project has always described and never produced — a map of *every symbol the
    pack patches and which module patches it* — and then checked it against the
    game's own class tree. It is committed as
    `agent/reports/L1_COLLISION_MAP.md`.

    ✅ **Nothing blocks launch, and I changed no code.** The pack does not fight
    itself: 16 global replacements, 16 different globals; no two modules write
    the same preset field; no two share a thread. The eleven modules that all
    hook "game loaded" don't overwrite each other — the engine appends them —
    which I re-derived from the engine source rather than trusting the comment.

    **Three things worth knowing, none urgent:**

    * ⚠️ **Two fixes wrap the same colonist function, and which one wins depends
      on the order they are listed in `metadata.lua`.** Right now the order is
      the *safe* one — but by luck, not by design, and nothing anywhere says so.
      If that list is ever reordered, alphabetised, or regenerated, one fix could
      start silently skipping the other. ⛔ I have **not** proven a player can
      actually hit the overlap; that needs a running game.
    * ⚠️ **Two fixes cover slightly less than you'd assume.** The asteroid-habitat
      fix doesn't reach the *Naturalist Habitat* building, and the track-connector
      fix's secondary "let the neighbours reclaim the hex" step doesn't run when a
      **Station** is destroyed — in both cases the game defines its own version of
      the function we patched, so ours is never consulted. ⭐ **Both are "we do
      less than we could", never "we do something wrong",** and the *main*
      track-connector repair does reach stations.

    ✅ **RESOLVED SAME DAY — nothing is owed, and you do not need to answer this.**
    You asked whether the fix was mine or the final audit's. It was mine (links
    1–2 may fix), and asking the question exposed that **my recommendation was
    answering the wrong version of it.** I had priced "pin the order" as *a
    comment in a file that ships* — which is why I said wait. There is a version
    that ships **nothing**: `*/tools/*` is excluded from the package, so a guard
    in `tools/doccheck.py` touches no byte a player receives.

    ⭐ **So it is enforced now, not documented.** `doccheck` fails **red** if
    those two entries are ever reordered, and prints the reason. That is strictly
    better than the comment I was hesitating over: a comment explains the rule to
    whoever happens to read it, and the guard stops the mistake.

    **Proven, not asserted:** I swapped the two entries — doccheck went red and
    exited 1 (so the commit hook blocks it); restored — `metadata.lua` is
    **byte-identical to HEAD** and doccheck is green. `upload_preflight` still
    passes 20/20. ⛔ **Zero shipped files changed**; the release candidate is the
    same bytes it was this morning.

    ⛔ **What link 1 did NOT look at,** so this is not read as a clean bill:
    nothing was run in a game; the two 08-17 core fixes still have not executed
    once; save footprint, uninstall, what a player sees, failure containment,
    packed-vs-unpacked, and any other mod are all untouched — those are lenses
    2–8. The chain has **not** converged; it has finished one lens of eight.

### ⭐ 2026-08-17 — THE RENAME IS DONE, EVERYWHERE A PERSON LOOKS. ✅ Your two calls came back the same day; nothing is owed.

36. ✅ **RULED 2026-08-17, both calls, same sitting.** (1) **You searched the
    in-game Mod Manager and "Relaunched Fix Pack" is free** — the one check no
    tool could run, done; the name is committed. (2) **Sibling titles: "rename
    them now"** — applied the same hour, one title line in each repo: the
    opt-in `metadata.lua` now says *"Relaunched Fix Pack: Opt-In Modules"* and
    Save Rescue's says *"Relaunched Fix Pack: Save Rescue"* (the family form
    you pre-approved in item 26, landing early on your word). ⛔ Title lines
    only, per the fence — each file's `description` still names the old family
    and carries a comment forcing that sweep before it ever uploads.
    ~~Search the in-game Mod Manager for "Relaunched Fix Pack" before it goes
    out — the Paradox Mods catalogue is the one place I genuinely cannot read.~~

    ✅ **The rename itself is DONE, same day** — every live surface in both
    repos now says **Relaunched Fix Pack**: the `metadata.lua` title that
    ships, the store card and its source record (re-proven identical by diff),
    the site's five pages, both playtest docs, the launch sheet, the in-game
    "fixes stood down" dialog, README and LICENSE. The true count was **113
    occurrences in 43 files** against the prompt's surveyed 72 — line-wrapped
    names hide from search — **and two of them were pictures: both preview
    images had the old name painted into the art.** They are re-lettered in
    the same design and typeface, and the originals are kept beside them.
    Every count the text moved was re-measured (title 18 → 19 characters; card
    body 10,781 → 10,782; nothing else moved), and **⛔ no GitHub repo, remote
    or org was touched**, exactly as you ruled. Historical records keep the old
    name on purpose — CLAUDE.md now carries the translate-mentally note.

    ✅ ~~The one timing call routed to you: the other two mods' internal
    titles~~ — **ruled above: renamed now, applied.** ⭐ **And your follow-up
    ("fix any references that you recommend") finished the job the same
    sitting:** both sibling repos are now swept end to end — metadata strings,
    the on-screen dialogs and rollover titles, code headers, READMEs, LICENSEs
    and their own CLAUDE notes all say *Relaunched Fix Pack*, with
    translate-mentally notes added so their records keep the old name honestly.
    Two genuinely stale non-name claims found on the way were fixed and
    annotated: the opt-in's `Opt_DroneOverhaul` header (old path, missing
    suffix) and the rescue `CLAUDE.md` still claiming the attended pass was
    owed (it passed 2026-08-14). ⚠️ One consequence carried forward, not
    hidden: the rescue tool's dialog text changed after its witnessed readings,
    so if that contingency ever fires, the already-required item-28 re-witness
    launch covers the new wording too. **This repo's README was also rewritten
    to current truth** — the ghost optional-modules section is gone, every
    count is this sitting's emitted number, and the false "disable via
    console" claim is replaced with the real veto-mod mechanism.

    ⚠️ **One small call I did not make for you.** The mod's internal id and its
    log tag both still say `CommunityFixPack`. Neither is something a player
    ever searches. **My recommendation is to leave both alone** — for the same
    reason you gave about GitHub: risk without reward. Every archived log and
    every baseline this project compares against greps that exact bracketed
    token, the Save Rescue tool removes things by name, and changing it would
    make no future test comparable to any past one. A bug reporter might
    briefly wonder why the log says one thing and the mod says another; that
    is the entire downside.

    ⭐ **For the record, since it will come up:** we are not the ones who
    copied. Our first commit is **24 July** with the tracker already carrying
    29 findings; his repository starts **4 August**. Two people reached for the
    same plain words. This rename is courtesy and clarity, and **no public page
    of ours mentions his mod or explains why we renamed.** *(While in there:
    two records cited his mod as Paradox Mods 153410 — that is his older *Bug
    Fixes* mod; corrected to 154004 per your screenshot.)*

    ⇒ **Owed from you: the Mod Manager search above, and the sibling-titles
    timing call. Nothing else.**

### ⛔⛔ 2026-08-17 — SOLO LAUNCH: ✅ the parking work is DONE; one question left before you upload

35. ✅ **The prep prompt ran the same evening and everything mechanical is
    done.** Every public surface now describes the fix pack standing alone —
    landing page, install, FAQ, fix list, for-modders, site README, the site's
    search-result description, the store card, and **both `metadata.lua`
    player strings** (not just the changelog — the description also named the
    opt-in mod, which the 22-reference survey had missed; the real count was
    ~46 passages, most saying "optional mod" in words no opt-in-shaped search
    catches). Nothing is lost: **every removed passage is stored VERBATIM,
    byte-compared before deletion, in
    `agent/reports/PARKED_OPTIN_REFERENCES.md`** with the restore trigger
    (*the opt-in publishes*) and a step-by-step restore checklist — the F85
    shelf treatment, as promised. Store card ↔ source record re-proven
    identical after the edits; every count re-measured (card body 11,209 →
    10,781 chars; the description 844 → 779; changelog now just "Initial
    release.", 16); doccheck and the site's strict build both GREEN; and the
    code was checked, not assumed — nothing in `Code/` behaves differently
    with or without the opt-in mod. **Release tag `fixpack-v1.0.1` is placed
    on this tree** per the new WORKFLOW procedure.

    **Q1 — "coming soon" vs silence: ✅ SILENCE IS APPLIED as the reversible
    default** (my recommendation — a teaser is an undated promise on a mod you
    called not ready, and it re-couples the products). Say the word and a
    one-line "coming soon" goes in exactly ONE place, the site FAQ — never the
    store card or `metadata.lua`, the two expensive-to-change surfaces.
    Nothing else moves if you flip this.

    ✅ **Q2 — RULED 2026-08-17 ("lets go with 1.0.0") AND APPLIED THE SAME
    HOUR:** `metadata.lua` now renders **1.0.0** (`version=0`), the tag moved
    to `fixpack-v1.0.0` (the interim `fixpack-v1.0.1` deleted, local and
    remote), and the ④ sheet says so. **Nothing on this item is owed any
    more — ④ is decision-free: upload the fix pack, link, Pages.** Your
    follow-up question was also acted on: the opt-in repo's STATE now carries
    the restore obligation, so the session that launches that mod cannot miss
    `PARKED_OPTIN_REFERENCES.md`.

    ✅ **Already done earlier, no action needed:** release procedure in
    `WORKFLOW.md` (tags mark what shipped), stale `wave4` branch deleted.


Things that need **your** call, not an agent's. One line each plus where the
reasoning lives; **an agent strikes a line the moment you decide** — just say so
in any session. Added 2026-08-03 by the docs-restructure chain (spec §7 / R10):
these used to be filed only in agent reports, which is where you never read.
⭐ **And fully-CLOSED decision records move whole to `PLAYTEST_ARCHIVE.md`
(rule adopted by you 2026-08-10)** — same treatment as completed test
sections, but only when nothing is owed to you; anything on-hold or holding an
owed input stays here no matter how struck-through it looks.

### ⭐⭐ NEW 2026-08-16 — "ONE MOD FIX ALL": I checked the other community mod against the game's code. Four real bugs we had missed. **One call from you: build them now, or after launch?**

34. ❓ **THE ONLY QUESTION: do these get built before you upload, or after?**
    You said you'd like ours to be *"fully fledged, one mod fix all"*, so I took
    `fredware`'s **SMR Community Fixes** — 15 fixes, 8 of which we already
    cover — and adjudicated the other **seven** against the game's own code. I
    did **not** install their mod (a third mod would have wrecked the baselines
    every gate in this project is measured against); I read a copy of their
    source to find out *where to look*, then reached every verdict myself from
    the shipped game files. **No fix code was written and nothing under `Code/`
    changed.**

    **Four are real bugs we had missed, and are now on the record:**
    * **`C51` — three bits of the interface can never be translated, and the
      translations are sitting right there in the game's own files.** This is
      the strongest one and the only one I could *prove* rather than argue: I
      opened the shipped German language pack and the German text for
      "OVERALL TERRAFORMING PROGRESS" and the rocket's "Back to Earth" button
      **is in there** — the game just never asks for it. Nine languages ship;
      any non-English player sees three English strings in an otherwise
      translated UI. Repairing this loses nothing in any language.
    * **`C52` — the in-game Mod Manager can never show a mod's screenshots.**
      The download loop reads a variable that has gone out of scope one screen
      earlier, so it fails on the first image, every time — and the developers
      left `-- todo: this is not working` in the file twice, directly above it.
      ⚠️ **One piece of this touches your upload:** the thumbnail cache is keyed
      on mod id + version and never re-checks. **If you ever swap a preview
      image after publishing without also bumping the mod version, players who
      already saw it keep the old picture forever.** Nothing to decide — just
      worth knowing before step ④.
    * **`C50` — SpaceY gives +20 Drone Hub command capacity and never says so.**
      It is the only sponsor in the game with a bonus its description hides; the
      other five that have bonuses all describe every one of theirs, three with
      the exact number. ⚠️ The obvious fix is a trap — replacing that text would
      hand eight languages an English description to gain one English line.
    * **`C49` — a soil-overlay bug that is real in the code and unreachable by
      any player.** The function that picks the overlay has a misplaced
      bracket — but the mode it fails to guard has **no button, no keybind and
      no caller anywhere in the game**. Filed honestly as latent. This is the
      third time here that "it's in the source" turned out not to mean "a player
      can hit it".

    **One I rejected**: their *Restore Clustered Lights* blames an assertion
    that lives in the engine's C++, not in any code we can read. I could not
    confirm or refute it, their own module says it is unproven, and their remedy
    changes behaviour rather than repairing a defect. Written up with reasons
    rather than filed.

    **Two we already knew about** (Jumbo Cave `C25`, Lander cargo `C35`).
    ⭐ The Lander one **paid off**: their module named a function ours had not
    followed, I re-checked, and **they were right and our record was
    incomplete** — confirming a payload edit doesn't just disconnect drones, it
    actively interrupts them, and the game's own code contains an assertion
    saying a drone on the ramp must never reach that line. Our entry is
    corrected and strengthened.

    ⇒ **My recommendation, and it is only a recommendation: investigate now
    (done), build after launch.** Adding four to five modules is not a tidy-up —
    each one costs a save-safety pass, a probe, a suite re-measure and three
    store surfaces, which is a release-delaying body of work. Nothing here is a
    release gate and nothing is broken by waiting. **"One mod fixes all" stays
    the direction either way.**
    → `agent/reports/SMRCF_COVERAGE_SWEEP.md`, entries `C49`–`C52`.

    ⭐⭐ **UPDATE, same day — THE CHAINS ARE WRITTEN AND WAITING. Nothing has
    been built and nothing has run.** You asked for chains for everything we can
    fix, simple ones combined, complex ones standalone, and the underground
    cave on its own. That is four chains, 13 prompts, drafted and committed:

    | chain | subject | prompts | **your time** |
    |---|---|---|---|
    | **A** `smrcf-verify` | answers every open question at once, arms two detectors | 2 | **zero** |
    | **B** `smrcf-text` | SpaceY + localization (+ dust devils if A clears it) | 3 | ~15 min |
    | **C** `smrcf-modbrowser` | the mod browser's three defects | 4 | ~15 min |
    | **D** `jumbo-cave` | the underground cave, solo as you asked | 4 | one playthrough segment |

    **A runs first and costs you nothing.** Three of the four currently rest on
    questions nobody has answered — are those dust-devil markers actually on the
    map, does the screenshot downloader exist, can we drive map generation from
    Lua. A settles all of them in one unattended launch, and if the answers come
    back wrong then B, C and D get smaller or disappear. **B, C and D are
    independent of each other and can run in any order.**

    ⭐ Your "stack the deck" idea is written into D as its method, with the one
    line it must not cross: **we turn up the rock density the game's own
    generator reads and let the game place them — we never place a rock
    ourselves**, because then we would only be testing our own placement. And
    the confound you would have hit is pre-registered: at high density rocks can
    block rocks, so when one strands we record what is *around* it. Terrain means
    the bug is real; other rocks means we only proved the consequence.

    ⇒ **Still nothing owed from you except the original question: now or after
    launch?** My answer is unchanged — after. ⛔ And one small thing is owed
    from me either way: **`C49` should be flipped to `wontfix — unreachable`**,
    which is what our own policy says for a defect no player can reach. Say the
    word and it is a one-line change.
    ✅ **RULED AND DONE 2026-08-20 — `C49` is retired `wontfix — unreachable`.**
    The C50/C51/C52 complexity you asked about the same day is measured in
    **item 56**; the "now or after" question here is still open.
    → `agent/prompts/SMRCF_CHAIN_SET.md` has the map and the kickoff lines.

    ⚠️⚠️ **AND ONE THING THAT IS *NOT* POST-LAUNCH — I FOUND STALE TEXT ON THE
    LIVE PAGES WHILE WRITING THESE.** You asked for a checkup of the public
    docs; ten minutes into scoping it, three things were already wrong:
    * **The FAQ contradicts itself about how many fixes are judgment calls** —
      it says *"Six fixes are judgment calls"* in one paragraph and *"Five"*
      fifteen lines later, and five is correct. That is the F85 removal sweep
      missing an instance, and it is on a page a player reads.
    * **"A suite of 95 checks"** appears on the store card **and** in its source
      record. The measured number is **96**. 95 was a prediction we made when
      F85 came out; the real re-measurement came back higher because the farm
      probe landed. This number has now been wrong twice.
    * Assume more survived the same sweep — counts moved on six surfaces at once
      that day.

    ✅✅ **THE CHECKUP RAN 2026-08-16 AND IS CONSUMED** (brief deleted; grave
    `git show <sha>:docs/agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md`). What it
    found beyond the three seeds, all fixed the same sitting:

    * **The removal sweep had missed more than one sentence.** The FAQ's
      balance answer also said *"in three of them the game's code is not
      wrong"* (now **two**), and the **landing page** still said six judgment
      calls (now **five**). Both were player-visible.
    * **A third stale record:** the metadata-strings report still quoted the
      fix-pack blurb saying "Six" as *"as shipped"*, when the live file says
      Five. Corrected, with the miss recorded.
    * **A fourth find, on your launch sheet:** the fix-pack card's body size
      was wrong — the 08-15 re-measure (11,542 characters / 2,011 words)
      never subtracted the deleted distress bullet. Measured today: **11,209 /
      1,957**, by the same method that reproduces the other two cards' cells
      exactly. Smaller, so no character-limit risk moves.
    * **Verified rather than inherited:** the achievements wording is the
      correct "Steam and other PC versions" form on every public surface
      (re-read at the game's own code, not from our records) · the item-29
      notice STRIKE held everywhere · no public page has grown load-order
      advice · the `%AppData%` log path the pages name exists on a real
      machine · both STORE↔RELEASE card pairs re-proven **VERBATIM** by
      actual diff after the edits · all twelve metadata string counts match
      the sheet · `doccheck` and `mkdocs --strict` GREEN.
    * **Readability, since you asked for it explicitly:** read cold as a
      stranger arriving from a store link, the five pages hold — one voice,
      problem-first FAQ order, searchable fix list. That is a judgment, not a
      measurement; no accurate sentence was traded for a smoother one, and
      zero pure-style edits were made.

    ⭐ The preview-image note is now **on the ④ sheet itself** (§0(a)): the mod
    browser caches preview images by mod id **and version only**, so swapping
    a preview after publishing without a version bump leaves everyone who
    already saw it on the old picture. Upload-day image choice is unaffected.

    ⇒ **The pages are ready to upload as they now stand.**

### ⭐⭐ NEW 2026-08-15 (late) — WE MEASURED YOUR OPEN FARM CASE ON YOUR OWN SAVE, AND IT DID NOT REPRODUCE. One sentence from you would explain that.

33. ✅✅ **ANSWERED BY YOU THE SAME EVENING, AT THE KEYBOARD — and then you went
    considerably further than the question.** Your answer was *"nothing but
    normal maintenance, not player build construction ongoing"*, which rules out
    the free-hex transient I had proposed. We then watched your save together and
    **the symptom reproduced**: your Potato farm was **stopped for 52% of the
    session** with its seed buffer hitting a true zero, while your other farm and
    all 36 Forestation Plants never stopped for want of Seeds. *(Audit precision,
    2026-08-15: late in the sitting one Forestation Plant did stop twice — for
    power/malfunction, nothing to do with seeds.)* You typed the banner sighting
    into the log, so for the first time this project can say a player *saw* it
    rather than that a counter fired.

    ⭐ **And you found the thing underneath it, which none of my instruments
    would have caught.** You noticed drones fetching single seed crates out of the
    landscape while a full 4,000 depot stood beside the farm, and guessed there
    was "a hidden rate at which vegetation offers seeds". There is — it is called
    `seed_cooldowns`, and grown plants offer their seeds to your drones through an
    invisible requester object. **That requester gets no distance penalty at all**,
    while the one comparable scattered source in the game was deliberately given a
    50% penalty by the developers. So on your carpeted map, hundreds of one-plant
    trickles compete with your depot on equal footing. You also explained why one
    farm is always silent — it sits in sparser ground with less drone-extender
    coverage, so its drones fall back on the depot.

    ⇒ **Filed as `C48`, credited to you, and it may be the real defect** — in
    which case enlarging the farm's buffer would only have hidden it. ⛔ **No fix
    will be built for either case until `C48` is measured**, which is a
    zero-cost unattended run I have already built the instrument for.
    → `agent/bugs/C48.md`, and the original question is kept below.

    ℹ️ **Update, 2026-08-15 late (the test you authorized — no decision owed):**
    the intervention ran. We applied the developers' own 50% distance penalty to
    every vegetation seed offer on a staged copy — all 3,390 of them, provably —
    and **the routing did not change at all**: your farms went right on eating
    280-seed crumbs from the landscape while 12.4 million seeds sat in storage.
    So the "just add the missing brake" fix is dead — on a map as green as
    yours, distance isn't why drones choose the landscape. The cause sits
    deeper (in the engine's own supply pairing, which modding can't read), the
    trickle costs you drone efficiency but never starved a farm in any
    unattended window, and the seeds-only "top-up" idea parked in the opt-in
    mod is now the one remedy still standing. Nothing is built; nothing new is
    owed from you. → `agent/bugs/C48.md` (the full readings).

    ⭐⭐ **CASE CLOSED — mechanism proven, 2026-08-16 (your go, your controls):**
    we put a log on the exact spot where every drone receives its assignment
    and watched **985 real decisions** on your own colony. For seeds, the
    matchmaker picked the landscape over storage **479 times out of 479** — and
    in **399** of those, a *full, available* depot sat **closer to the drone**
    and lost anyway (one drone flew 7× past a stocked depot for a single bush).
    Your reading was right on every count: **storage depots are a hard last
    resort** — the network only touches them when no loose source exists, which
    for food happens constantly (so your diners get bulk deliveries and never
    starve — we measured one draining ~48,000/sol and keeping up fine) but for
    seeds on a terraformed map happens *never*, because the bushes never run
    out. Your "desired amount" understanding was also confirmed with data (it
    withholds nothing from consumers), and your depots turn out to *restock
    themselves from bushes* — that's why your seed hoard keeps growing. **This
    is deliberate engine machinery with a cost the designers never priced on a
    terraformed map. Whether that's a bug or a design cost is your ruling to
    make, whenever you want to make it — nothing ships either way, and the
    top-up ("gleaner") idea in the opt-in mod remains the remedy that fixes
    the waste without touching the choice.** → `agent/bugs/C48.md`.

    ✅✅ **AND YOU CLOSED THE LAST LOOSE END THE SAME EVENING, 2026-08-16 —
    nothing owed, recorded here because it is your call and it kills an option
    nobody should reach for again.** Your words: *"I don't think a buffer will
    fix it because they don't fill the current buffer as of now"* and *"we can
    retire that for the bug fix mod, and leave it solely for the opt in mod."*
    ⇒ **The "just give the farm a bigger seed buffer" fix is dead**, and it was
    the cheapest-looking one on the list. You are right and our own numbers say
    so: the farm never fills the 5000 it already has, because every delivery is
    one bush's 280 seeds against a drone that can carry 3000. Raising the
    ceiling to 10000 would leave a bigger buffer sitting at 400. ⇒ **The old
    warning "don't fix C47 until C48 is measured, a bigger buffer would hide
    it" is retired with it** — a buffer that never fills can't hide anything.
    ⇒ The whole farm family is now **solely the opt-in mod's**, the buffer shape
    is struck there too so the gleaner work can't inherit it, and the fix pack
    keeps only the records and the probe. Nothing is built, nothing is owed.
    → `agent/bugs/C47.md` (shapes section), opt-in
    `agent/reports/SEED_LOGISTICS_HANDOFF.md` §2.

    ~~**When you saw the endless "waiting for Seeds" popups — had you just done
    something to those farms?**~~

    **Why it is the only thing left to ask.** We ran your save `C47FARM` seven
    times unattended tonight (your cost: zero) and watched both of your Open
    Farms for 15 in-game hours — about 51 planting ticks. **The sampled buffer
    never once read empty** *(the sitting later proved it did touch zero
    briefly — 2, 0 and 4 times across the runs — between our polls; the point
    that this is nothing like what you saw still stands)*. The Potato farm's
    lowest reading was 305 of 5000; the
    other farm's was 1661, and that one never raised a single "not working"
    event in any run. The Potato farm raised 2, then 0, then 4. That is nothing
    like what you saw.

    **We also found out why, and it is a real correction to our own filing.** We
    had assumed a farm plants 3–5 hexes every tick and pays for all of them. It
    doesn't: it only pays when it finds an EMPTY hex, or one growing the wrong
    crop. Your farms are fully planted, so they averaged **2.2 hexes a tick and
    spent nothing at all on about a quarter of the ticks** — roughly 40% of what
    we told you. Which means the drain we described is real but it is the rate a
    farm hits when it has hexes to fill: right after you build it, enlarge it,
    change its crops (every existing hex becomes "wrong" at once), or after a
    wither. **A terraforming speed-run is when a player does all of those.**

    ⇒ If the answer is "yes, I'd just been fiddling with them", the case is
    explained and we can talk about whether it is worth repairing. If the answer
    is "no, they were untouched", then something we have not found yet is going
    on, and it is worth another look.
    ⛔ **Nothing is built, nothing is decided, and no repair is proposed** — this
    is still a candidate, not a confirmed defect.
    → full readings, every prediction and how it fared, and the three defects we
    found in our own instruments: `agent/bugs/C47.md`.

**Two smaller things worth knowing, neither needing a decision:**

* **Your drones carry 3 loads, not 1** (the Drone carry capacity dial in Mod
  Options, set to +2). So a Seeds trip is 3000, not the 1000 we quoted you. It
  makes your observation more striking, not less.
* **That save cannot be run past Sol 385 by an agent.** At the sol boundary the
  game opens a popup, which pauses the clock, and with nobody at the keyboard it
  stays paused forever. It is normal game behaviour; it just caps how far any
  unattended run of ours can get on that colony.

<details><summary>The original source answer, from earlier the same day — kept because the two numbers in it are still exactly right</summary>

ℹ️ **No decision was owed on this part** — it is your rider, recorded so your own
testing has something to argue with. You asked two questions and for a
comparison; all three are answered at source, on the pinned build.

* **Is the storage right?** ⛔ **It was never set.** `OpenFarm.lua` has no
  `consumption_max_storage` line at all, so it takes the editor default of
  **5** — which is the `0/5` on your screen.
* **Is the consumption right?** ⭐ **The consumption is the half that WAS
  deliberately tuned**, which is what makes the pair look wrong. Open Farm
  overrides its planting interval from the class default **2.0 in-game hours to
  0.3** (a 6.7× speed-up), plants **3–5 hexes every tick**, and at **Potato**
  each hex costs **600** — so a single tick can cost **3000 against a 5000
  buffer**. It can never bank two ticks, and a drone only carries **1000** per
  trip. That is why a full depot and 24 idle drones do not help.
* **The comparison you asked for, and it is decisive.** The only other Seeds
  consumer and only other plant-building, **`ForestationPlant`, SETS its storage
  to 10000 explicitly, keeps the 2.0 h tick, and plants ONE hex** (two under the
  Forestation Effort law). Runway on a full buffer: **~40 in-game hours for
  Forestation vs ~0.5 for the Open Farm — about 80×.** Even your cheapest crop
  (Cover Crops) only buys ~3 hours.
* **Across the whole game:** 287 templates, 29 consumers. Ten leave the storage
  at default — but ⭐ **Open Farm is the only one of those that also tuned its
  consumption cadence.** Everyone who made a building drink faster also made
  the cup bigger. One half of a paired change, the same shape as `C39`.

⛔ **What I am NOT claiming.** No code comment ties the two fields, so this is
an *unset field*, not the self-contradiction `C39` was — "farms are meant to be
supply-hungry" is a defensible reading, and the popup is the game correctly
reporting a genuinely empty buffer. And **nobody has measured it in game** —
your observation is the only runtime evidence. So it is filed as a candidate,
not a defect, and **nothing is built**.
→ full derivation, every citation, and three unranked repair shapes (size the
buffer · debounce the notification only · document and do nothing):
`agent/bugs/C47.md`.

⚠️ **Superseded the same night by the measurement above, in two places:** the
"3–5 hexes every tick" and the runway figures that follow from it describe a
farm with hexes to fill, not a planted one; and the "80×" comparison is a
template ratio, which the run could not turn into a measured multiple because
the control never flapped at all. The two template numbers — the buffer that was
never set and the cadence that was — are confirmed in the running game and a
permanent check now re-tests them on every run.

</details>

### ✅ 2026-08-15 — the 54 MB leftover is DELETED (was: one word from you)

32. ✅ **RULED + DONE 2026-08-15: DELETED.** Your word: *"You can delete that
    save."* Removed and verified absent; the save directory now holds **77
    entries**, and the only non-`.sav` files left are `account.dat`,
    `account.dat.bak` and `steam_autocloud.vdf` — i.e. nothing of ours and no
    stray from the 08-12 cloud-restore batch. `EF-051`'s falsifier stands.
    ~~`U2RT1` (no file extension, 54 MB) is still in your save folder — delete
    it or leave it?~~ It is the one member of the 08-12 cloud-restore batch the
    08-14 cleanup missed: that sweep listed `*.sav` files and this artifact has
    no extension (a quirk this project's own testing produced — `EF-050`). Both
    of last night's launches were checked by creation-time window: **neither
    touched it**, so the cloud-off retirement stands and nothing is wrong. It is
    unattended-2's leftover, not a save you made, and nothing reads it.
    **Rec: DELETE** — same population, same license as the 888 MB you already
    ordered swept; it was left only because deleting it unattended felt like a
    daylight call. Say the word either way; "leave it" costs only the 54 MB.
    → `agent/facts/EF-051.md`, the 2026-08-15 bullet.

### ⛔⛔ NEW 2026-08-15 (later) — pricing your "quick playtest?" question found that the F85 dialog CANNOT BE OPENED IN THE GAME AT ALL, and two player-facing pages describe it as if you had seen it

31. ✅✅ **RULED 2026-08-15 — REMOVE IT, BUT KEEP IT RE-APPLIABLE. DONE THE SAME
    DAY, ACROSS EVERY SURFACE.** Your words: *"I think we remove it but document
    it, so we can easily re apply it as a fix, if something ever player facing
    comes out we already know how to fix it."*
    ⭐ **The shelf record is `agent/reports/SHELVED_F85_DISTRESS_PAUSE.md`** — it
    carries the module and its probe **verbatim** (byte-compared before the
    originals were deleted), the trigger that would make them worth shipping
    again, a 30-second source check that answers that trigger, a six-step
    re-apply checklist, and a table of everything already proven so none of it
    is ever redone. ⛔ Deliberately NOT "it's in git history" — that is the
    hand-wave the file exists to prevent.
    **What moved:** module deleted (and its row pulled from `metadata.lua`'s
    file list — that one would have broken the mod); probe deleted; this entry
    → `wontfix`; the judgment bullet gone from the card and the whole entry gone
    from the site fix list; the judgment-call count five→six→**five** again in
    all six places it appears; suite **96 → 95**; modules **76 → 75**. doccheck
    GREEN, `mkdocs build --strict` GREEN.
    ⇒ ✅ **Item 5 closes with it** — `P3` / LATENT / tier U is exactly right for a
    defect that is real, reproduced and unreachable.
    ⛔ **One number is PREDICTED, not measured, and I will not quote it as a
    reading:** the suite baseline should become `79/0/16/0 of 95` and the gate
    `75/75`. No launch has run since the removal — the next unattended leg
    measures it. Nothing is owed by you either way.
    *The question as it stood, kept for the record:*
    ~~The distress-call dialog is dead-coded out of the shipped game. The fix
    is fine; the two places that describe it to players are not.~~
    **How this surfaced:** you asked whether I was proposing a quick playtest for
    F85. Pricing that meant working out how anyone *raises* that dialog — a route
    nobody had ever checked, because the record simply said "open it from the
    console". The answer is that **nothing can raise it**.
    **What the game's own code says**, re-read at Src today and traced
    exhaustively: the dialog has exactly **one** caller in the entire tree — the
    `DISTRESS CALL` button on the rival-colony action bar — and that button sits
    inside a condition the shipped executable compiles to the literal
    `local cond = false / if cond then …`. The button is never built. Every other
    piece of the feature (the cooldown, the "allowed?" check, the resource
    request) is used by that dead button and nothing else. **The developers
    switched the whole feature off and left the code in place.**
    ⚠️ **This is the second time in this one entry.** The same shape retired the
    Quick Save route on 08-11 (`idQuickSave` compiled out behind
    `Platform.cheats`). You are the one who forced that check, against a
    confident source citation, and you were right then too.
    ⇒ **NO, there is no playtest to propose** — see item 5 for the whole answer.
    ⇒ **The fix still ships and is not touched.** It is a wrapper that pauses any
    popup declaring itself non-pausing; it is measured idempotent, measured not
    to disturb popups that already pause, and it no-ops if the flag ever
    disappears. On this game version it has **no live symptom** — it is a defence
    of the rule ("no save lands inside an open popup"), not a repair of something
    you could ever hit.
    ⛔ **What is actually wrong is the writing, on two surfaces**, and it is the
    same class as item 29 which you ruled STRIKE — a claim about what a player
    *sees*, resting on a mechanism that is real in source and absent from the
    retail screen:
    * the **store card** (`RELEASE_DESCRIPTION_FIXPACK.md`): *"every other popup
      window pauses the game while it is open; the confirmation for broadcasting
      a distress call deliberately did not"* — present tense, about a window no
      player can open.
    * the **site fix list** — worse: its entry opens **"What you saw:"** and then
      describes the clock running behind a window nobody can raise.

    ⭐⭐ **AND YOU IMMEDIATELY ASKED THE BIGGER QUESTION, WHICH I SHOULD HAVE
    ASKED FIRST:** *"if that is a button not built, and not something a player
    can ever get to — why are we building a fix for it?"* **I do not have a good
    answer, and I now think we should not be.** The question is no longer how to
    word the description; it is whether the module ships at all.

    **The case against keeping it, which I find decisive:**
    * ⛔ **It repairs nothing.** This repo's own premise (CLAUDE.md) is that
      *every fix repairs a verified defect in the game's shipped Lua*. On
      1.0.7.396349 no reachable popup sets the flag, so the branch that does the
      work **can never execute**. It is not a small fix; it is a dead one.
    * ⛔ **It is not free — it sits in a hot path.** The wrapper patches
      `PopupNotification:Init`, so it runs for **every popup the player ever
      sees**, forever, to evaluate a condition that is provably false. Zero
      benefit, non-zero surface. That trade is the wrong way round.
    * ⛔ **It overrides a deliberate developer choice to no effect.** We
      disclosed it as a design-judgment tweak precisely because the game's code
      is not wrong. Overriding a dev decision to fix something reachable is a
      judgment call; overriding it to fix nothing is just noise in the tree.
    * ⛔ **The one case where it CAN fire is arguably a harm.** Its own
      disclosure says so: *"a popup created by a future patch — or by another
      mod — that sets `dont_pause` would also be paused by this module."* Since
      no vanilla popup can reach it, **the only live scenario left is us
      silently overriding another modder's deliberate choice.**
    * ⛔ **This entry's own rule already prescribed the answer.** F85's original
      fork read: route real → owner decision; *"if the binding or save is
      refused, this drops to I/R4 and stays documentation."* Every route is now
      refused. The entry's own discipline says documentation.
    * ⚠️ **And your 08-12 ruling rested on a fact that has since been falsified.**
      You ruled build-it on the basis that *"the distress dialog is the game's
      ONLY non-pausing popup, so pausing it closes this entry's entire reachable
      surface"*. The first half is still true. The unstated half — that the
      surface is **reachable** — is false. Recommending removal is not
      overturning your judgment; it is reporting that the ground under it moved.

    **The case for keeping it**, stated fairly so you are not being nudged: it is
    a cheap class defence, so if a future patch re-enables the distress feature
    or introduces a new non-pausing popup, we are already covered. ⚠️ But that is
    exactly the "perpetual rider" class **you already ruled on** in item 14 —
    things that keep failing to produce their own precondition become
    post-release WATCH items rather than freight. A precondition that *cannot
    occur on the shipped build* is the limit case of that ruling.

    | | what happens | cost |
    |---|---|---|
    | **A. REMOVE the module ← recommendation** | delete `Fix_DistressPopupPause.lua` + its probe; F85 becomes documentation-only (`wontfix`, real defect / no reachable route); card bullet and fix-list entry deleted because there is no fix to describe | counts move 76→75 modules and 96→95 probes, and the suite gate re-baselines — ⭐ **prompt 03 was already re-truing every one of those numbers**, so this is close to free if ruled now. Reversible: if a patch ever revives the feature, the module is one file in git history. |
    | B. Keep it, ship it silently | module stays; card bullet + fix-list entry struck (item 29 treatment) | the fix list would then describe 75 fixes while 76 ship — an undisclosed module, which is its own small dishonesty, and the dead branch stays in every popup's constructor. |
    | C. Keep and describe it honestly | *"a dialog the shipped game no longer uses…"* | ⛔ worst of both: keeps the cost, and spends a player's attention explaining a non-event. |
    | D. Ship exactly as written | nothing changes | ⛔ present-tense false statement on a store page, plus a **"What you saw:"** for something nobody saw. Not recommended. |

    **Recommendation: A — remove it.** ⇒ ⭐ **Ruling A also CLOSES item 5**: with
    no fix, F85 is a documented, reproduced, unreachable defect, which is exactly
    `P3` / LATENT / tier U as already labelled. One word from you settles both.
    → the full derivation, every grep and the generated-file quote:
    `agent/bugs/F85.md` §2026-08-15 (later).
    ℹ️ *(Terminal-audit addendum, same day: the judgment-call COUNT rides this
    ruling too. It was settled at SIX this morning across the card, the
    mod-page blurb, the site FAQ, the landing page and the fix list; under A
    or B it reverts to FIVE on every one of those surfaces, under C it stays
    six. The full surface map is staged, the sweep is minutes. The C39
    disclosure paragraph and the "96 checks" sentence are independent of this
    item — though A also moves "96 checks" to 95 when the probe goes.)*

### ⭐ NEW 2026-08-15 — the C39 repair you ruled turns out to touch TWICE as many buildings as the ruling pictured. ✅ CONFIRMED THE SAME DAY.

30. ✅ **RULED 2026-08-15: SHIP AS BUILT — all eight families, no list.** Your
    words: *"Lets go with whatever is supposed to be true to the code, which
    fits this mod as a true to code bugfix as much as possible."* You also
    challenged the framing first (*"I thought we decided on this awhile ago?"*)
    and you were right — 08-12 already ruled "extend the compensation" and
    widened the sweep yourself; this was a confirm on the size of what the
    sweep returned, not a re-opening.
    ⭐ **Why the principle picks this option and not a narrower one.** The
    shipped module carries **no building list at all**: at runtime it asks the
    building in front of it two questions — does it carry *this active law's own
    effect object* as a `max_workers` modifier, and does it fail all three class
    gates — and pays back exactly the delta vanilla's own loop would have
    produced. Coverage is therefore "whatever actually has the defect", which is
    what true-to-code means here. **Restricting it to the four Workshops would
    have required ADDING a hardcoded template list that does not exist today**,
    purely to leave identically-broken buildings broken. That is the less
    faithful option, not the safer one.
    ⭐ **And it is faithful to the law's own player-facing text**, which is the
    other half of "true to code": the law reads *"Service buildings require 50%
    less workers"* — the trade is labour, nothing else. The declined delabel
    alternative would have made the law quietly not apply to those buildings,
    contradicting its own description; extending the compensation keeps the
    promise the law prints. (Comfort is not the law's trade — it is merely what
    the four *Workshops* happen to produce with their performance, which is why
    the 08-11/08-12 conversations were all about comfort.)
    ⇒ **Nothing to do. No code change, no re-run.** Prompt 03 writes the card
    and fix-list text against the real eight-family footprint.
    ~~Ship the repair as built, or restrict it to the four Workshops?~~ — the
    original question and its full breakdown are kept below for the record.

    **Why you are being asked at all.** Your ruling explicitly widened the
    scope — *sweep all three automation labels and cover every mismatch found* —
    so what shipped **is** what you ruled. But the picture in front of you at
    the time was "four Workshops whose Comfort payment is short", and the honest
    version of that picture is now bigger, so you get to see it before it
    reaches a store page.

    **The defect, unchanged:** all three Automation laws cut a building's
    workers by **label**, while the code that pays the workers back keys on
    **class**. Buildings on the wrong side of that line lose half their staff
    and get nothing back — roughly half their output. The game's own comment
    says the two lists are assumed to match.

    | | what the law halves | what it costs today |
    |---|---|---|
    | Art / Biorobotics / VR Workshop | ✅ already known | the Comfort their shift pays |
    | TV Studio (CCP) | ✅ **measured 08-11** | Comfort **+ TV-show progress** |
    | ⭐ **Security Station** | new | **renegades neutralised** — half the security you paid for |
    | ⭐ **Security Post (CCP)** | new | same |
    | ⭐ **Drone Assembler** | new | **drone and android build time** |
    | ⭐ **Bottomless Pit Research Center** | new | **resources processed into research** |

    The last four sit on `Service Automation` (the Security pair) and
    `Factory Automation` (the other two) — the Factory law had never been swept.
    Research Automation is clean.

    **What the fix does to them:** exactly what the game already does for a
    Diner or an Electronics Factory under the same law — nothing new, no new
    number, no balance invention. Each affected building rides to roughly double
    performance on half the staff, which is the "overall performance is
    maintained" the code says it is aiming for.
    **Recommendation: ship as built.** ✅ **This is what you ruled.** Restricting
    it to Workshops would mean deliberately leaving Security Stations and the
    Drone Assembler broken while fixing their neighbours, with no principle
    separating them.
    ⚠️ **What you should know either way:** these are gameplay-visible numbers
    (security, drone throughput, research), so a player who has been running
    Automation laws will notice the difference. That is the repair working — but
    it is a bigger visible change than "Workshops pay slightly more Comfort",
    and prompt 03 will have to say so on the store card. ⛔ **That disclosure
    survives the ruling** — shipping as built settles the SCOPE, not whether the
    card mentions it.
    ⭐ **Mitigating fact, from the sweep:** all three Automation laws share the
    `Automation` policy slot, so **at most one can be active at a time**. In any
    one game the repair reaches the four Workshops + two Security buildings
    (Service law) *or* the Drone Assembler + Bottomless Pit (Factory law) —
    never all eight at once.
    ⚠️ **Evidence honesty, unchanged by the ruling:** only `TVStudioWorkshopCCP1`
    is MEASURED (08-11 unfixed, 08-15 fixed). The other seven are SOURCE — a
    class-graph resolution with every row re-read by hand at its declaring file.
    The runtime discriminator bounds the risk: the code can only fire on a
    building that genuinely carries the cut and genuinely fails the gates.
    → the full sweep, every class chain re-read at source, and the design
    reasoning: `agent/bugs/C39.md` §2026-08-15.

ℹ️ **Also for awareness, no call needed:** the **F85** fix you ruled on 08-12
is built the same evening — the distress-call dialog's non-pausing flag is
cleared so the game's own code builds its pause layer. ✅ **2026-08-15: both
builds are VERIFIED** — the suite passed in a real launch (80/0/16/0 of 96)
and both repairs were read working in a second launch on your own colony copy;
both entries now carry `tested-unattended` under your 26b vocabulary. ⚠️ The
same day's route check found the dialog itself is dead-coded on retail —
item 31 above owns what that means for the two player-facing descriptions.

### ⭐ NEW 2026-08-14 (later) — ④ IS CUT: your launch afternoon reads ONE sheet, and the audit found one more call that comes before any paste

**The release-3 chain is closed** — both cards paste-ready and diff-proven
verbatim to their audited sources, the third card written and gated, the
uninstall story reconciled, the metadata strings applied and counted, the
packaging measured. **When you sit down for launch, read
`agent/reports/RELEASE_PORTAL_PREP.md` top to bottom — it is the whole
afternoon in order** (upload → links → Pages → fill-ins), and it names
everything below in context.

✅✅ **ALL FIVE CALLS RULED 2026-08-14, applied the same day:**
**29** strike → the notice paragraph is deleted from both cards, the rescue
card, the assembly and the site FAQ, with the source records corrected ·
**17** hold off → Save Rescue not published at launch, held as a contingency
for post-release reports; its fill-in marker and the assembly's rescue section
deleted per their defaults · **28** closes with 17 → ship as built ·
**cleanliness sentence** Reading A (the pack alone) → no text change, the
card's deliberate absence stands · **opt-in version** → **1.0.0 applied** in
its `metadata.lua`. ✅ **And the preview art is CHOSEN the same day — C1 for
both mods** (item 24's floor, built as designed Mars backdrops without a game
launch; `agent/reports/preview_art/FINAL_*.png`, both ~40 KB against a 1 MB
limit; alternates kept, vista-swap possible later). ⇒ **④ is fully prepared:
upload two mods with their previews → links → Pages. Nothing waits on a
decision.**
⭐ **Ordering, your word (2026-08-14 evening): the F85 + C39 builds run
FIRST** — "finish the f85 first since its all unattended." The `unattended-3`
chain is authored (`agent/prompts/unattended-3/`, Opus builds → Opus verifies →
Fable audits, including re-truing every card/site count the two new modules
move) and ④ follows its close. Also done on your word the same evening:
**Steam Cloud re-untick recorded** — the 17 strays the hold window restored
(888 MB) are deleted, the save directory re-listed by name at 76 files, and
"gone" claims are legal again (`EF-051`).
✅✅ **2026-08-15: THE `unattended-3` CHAIN IS CLOSED — terminal audit consumed,
folder empty.** Both builds sustained end to end (routes re-derived at source,
the C39 coverage list reproduced by an independent sweep, both launch logs
re-counted line by line), and every count the two modules moved is re-trued on
the cards, the mod-page blurb, the site and the portal sheet. ⛔ **One thing
now stands between you and the ④ paste: item 31 above** — the same-day route
check found the F85 dialog dead-coded, so rule 31 (one word; it also closes
item 5) and the staged minutes-scale sweep trues the last surfaces. C39's
disclosure and everything else on the sheet are ready as written.

29. ✅ **RULED 2026-08-14: STRIKE — and struck the same day on every surface**
    (both cards, the rescue card, the assembly, the site FAQ; trace rows and
    the §10.9(4)/D13 source records corrected so it cannot be re-inherited).
    The question as it stood: both store cards promised an on-screen notice
    the game never shows for our mods. The sentence: *"the first time you load a save that was made with
    any mod you have since removed, the game itself prints a notice that the
    save refers to a mod that is not there."*
    **What the route shows:** the measured evidence behind it is a **log-file
    line** (`Savegame references Mod … which is not present` — engine
    bookkeeping, written to the log only). The one thing the game puts **on
    screen** for missing mods is the "missing or outdated mods" warning, and it
    deliberately skips mods marked *optional* — **which all three of ours are**
    (the same flag that stops the game nagging players who removed the mod,
    set on purpose in all three `metadata.lua` files). A player who removes our
    mods sees **nothing**: no notice, nothing to dismiss, nothing that
    "disappears when you save". The record's "you will see one notice" was an
    inference from rig logs — the rig draws the log on screen; a retail player
    has no such overlay. Nobody has ever watched a retail-shaped load show one.
    **Recommendation: strike it** (or let the for-modders page alone carry the
    accurate log-line version). One agent sweep fixes every surface the same
    way once you rule — cards, rescue card, assembly, site FAQ (site edits are
    FILED, awaiting exactly this ruling). Shipping it as written is the
    harmless direction (players told to expect a notice just never see one),
    but it is a false statement of fact on every card, which is the exact class
    the whole evidence bar exists to keep off a store page.
    → route + evidence: `RELEASE_DESCRIPTION_RESCUE.md` audit section (engine
    cites: `Mod.lua:1199`, `SavegameMetadata.lua:97-99`); `D13_EXPOSED_SET.md`
    §10.9(4) is where the log measurement lives and where the "you will see"
    aside crept in.

ℹ️ **Also fixed by the audit, no call needed:** the rescue tool's instructions
("load once … delete it again") never said to **save** — and the clean pass
only edits the loaded colony; the player's save is what writes it into the
file. Corrected on every editable surface (rescue card, its `metadata.lua`,
the opt-in card's Save Rescue fill-in sentence). ⚠️ The rescue's **on-screen
dialog** has the same omission ("You can remove Save Rescue whenever you like")
— a code string. ✅ With 17 ruled hold-off and 28 closed **ship as built**,
nothing ships with it; ⛔ **if the contingency ever fires, re-open the dialog
text before upload and add the save-step line in the same one-launch
re-witness** (recorded on item 17 and in the rescue card's header).

### ⭐ NEW 2026-08-14 — the release descriptions are being written: ONE question, and it is bundled with a call you already owe

28. ⚖️ **The Save Rescue dialog buries the one line it exists to print. Fix the
    code (costs you one launch) or ship it as built (costs nothing)?**
    **Answer this together with item 17** — whether the rescue tool publishes at
    all — because better dialog text is only worth anything if a player ever
    sees it. If the tool does not publish, this is already answered: ship as
    built, and say so and I strike the line.
    **What you saw at the sitting**, reconstructed exactly from the counts in
    your own dialog:
    > Removed: 1 rain loop stamp · 1533 reservation timestamps · **2 drone stat
    > dials** · 22 dome flags · 4 building flags · 4 rocket payload flags

    The tool exists for the **drone dials** — they are the one leftover that
    keeps changing your game after you uninstall; everything else on that line
    is inert. It printed **third of six**, with no explanation, next to 1533
    timestamps. That is not a design choice: the groups are sorted as *text*, so
    they line up by the digits of their counts, and the drone line lands wherever
    its "2" happens to sort.
    **What the fix would look like:**
    > Removed: **2 drone stat dials (drone speed and carry capacity are back to
    > the game's own values)** · 1 rain loop stamp · 4 building flags · …

    **What it costs you:** the changed text has never been on a screen, and the
    only instrument that can ever check a dialog is your eyes — no log records
    one. The gloss also makes that line much longer on a dialog built for a
    gamepad, and whether it wraps badly is exactly the thing a log cannot tell
    us. So: I re-stage the save (my time, but note it is the copy-an-autosave
    hazard again, so it is not free of risk to *your* saves), you take **one
    launch, one Mod-Manager visit, and about five minutes** reading one dialog.
    **My recommendation: decide item 17 first.** Publishing → do the fix, it is
    the tool's entire user interface and it is currently unreadable at the one
    place it matters. Not publishing → ship as built.
    ℹ️ **Nothing is blocked either way.** The descriptions being written now do
    not quote the dialog; they say in plain words, on the page you read *before*
    installing, that a non-base drone speed/carry dial keeps working forever
    after uninstall. And your `tested` verdict on the rescue tool is untouched —
    it was granted against the text the build really prints, which is still
    exactly what it prints. → `agent/reports/D13_EXPOSED_SET.md` §10.5's
    correction block (three more mismatches found there, all cosmetic bar this
    one), `agent/bugs/D13.md`.
    ℹ️ **Your launch-day sheet exists:** `agent/reports/RELEASE_PORTAL_PREP.md`.
    The full ④ picture — the five calls in order, the preview-art blocker, and
    one more audit finding that touches this item's "fix the dialog" branch —
    is the **④ IS CUT** block above this one.

### ⭐ NEW 2026-08-13 — the SITE is built (unpublished): one small question, and two things for your awareness

ℹ️ **2026-08-14 — the site chain is CLOSED; nothing here is owed by you.** The
terminal audit read all five pages and both store cards as a player, re-ran the
"which shipped module delivers this?" control firewalled from the ledger
(**clean — no new false claim**), re-verified the exposure gate and that both
issue trackers are really open, and applied the one correction routed to it:
the store card's patch-retirement sentence is narrowed to its accurate
shape-of-the-code version, under your 22d item-1 approval. Still nothing on the
web; publishing remains yours. Open decisions stay at 3.
*(Superseded the same day: the release-description chain added **item 28**
above, so open decisions became **4** — its terminal audit added **item 29**
for **5** — and the owner then ruled all five release calls in one sitting
(29 strike · 17 hold-off · 28 ship-as-built · cleanliness A · opt-in 1.0), so
open decisions are back to the **3** standing non-release items.)*

27. ~~⚖️ **WHERE DOES A BUG REPORT GO?**~~ ✅ **DECIDED 2026-08-13, same session:
    BOTH, COMMENTS NAMED FIRST — and it is written into the site already**
    (`content/faq.md` → "Where do I tell you?"). The mod page's comments are the
    main route, read first, needing no account a player does not already have
    and working on every platform; the project's issue tracker is named once,
    for the reporter who has a **save file or a log**, because a comment section
    cannot carry either. One tracker covers both mods. ⚠️ **What you took on:**
    a tracker is a place you have said you will look — issues are open on both
    mod repos (verified live). ⛔ The store-page link is still a hole until you
    upload. ℹ️ Offered, not built: a short issue form that asks for platform,
    when it started, whether it survives a save and reload, and the save — say
    the word and it is ten minutes of agent time.
    ℹ️ **Awareness, no decision owed — the frozen description has TWO MORE false
    claims than the four on record, and both are the `F76` shape.** Writing the
    fix list meant asking, for each of its bullets, *which shipped module
    delivers this?* — and two had no module at all: the **dome-plumbing**
    bullet describes `F24` and the **research-counter** bullet describes `F28`,
    both closed `wontfix` on 2026-07-30 with their code files deleted. Neither
    ever reached a store card. ⛔ They are recorded in
    `agent/reports/SITE_BUILD_AUDIT.md` so the release-prep rebuild of that file
    cannot inherit them.
    ℹ️ **Awareness — the Sensor Tower sentence in that same file is backwards,
    and so was the site's own specimen.** It says towers *made meteors worse*;
    the code says the opposite — towers added warning time, warning time WAS the
    interval, so towers accidentally spaced strikes out and the players actually
    hurt were early colonies without them. The site now says the true version.
    Nothing shipped is affected: neither store card mentions Sensor Towers.

### ⭐⭐ NEW 2026-08-13 — D13 CHAIN CLOSED; the ONE combined sitting is READY (step ② — the release line's next move is yours)

26b. ✅✅✅ **THE COMBINED SITTING RAN 2026-08-14 AND ALL THREE MOMENTS PASSED.
    ⭐⭐ D13 IS `tested`. NOTHING HERE IS OWED BY YOU ANY MORE.**
    **Your cost: 34 minutes** of parked handover time measured off the harness
    heartbeats, against a 30–45 promise — inside a ~67-minute wall clock whose
    difference is your own landscaping lead and one stalled launch. Six logs
    archived byte-verified (`archive/cs_*`). **0 `[LUA ERROR]` in every cell.**
    * **F102's minute** → item 11 above, struck. Sign renders, selectable.
    * **PT-20 redo** → state 3 confirmed (`pack=0/0` + `opt-in=0/0`, kit alone in
      `Loaded mod items for:`), all 8 pack-naming lines accounted, ~21 min of your
      ordinary play + a save + a reload, **zero errors in the flushed file**.
      Recorded as **superseding** the old 98-vs-98, not confirming it — that was an
      error count from the F86 era and F86 is repaired.
    * ⭐⭐ **D13 after-sweep** → `removed 1566` by name on a NATIVE witness,
      **matching a prediction committed before the sitting row for row and skip for
      skip**; the F48 repair kept; `heals: 0, 0, 0` because nothing was broken. And
      the three readings no log can ever hold: **report dialog raised** with the
      right text, **cleaned reload silent** (with `save-rescue=1/1 active` beside
      it, so the silence means something), **stand-down exactly once**.
    ⚠️ **Three things went wrong and none of them was the mod.** (1) Save Rescue
    came back from its junction round trip **not enabled** — that cost you one
    Mod-Manager visit and a launch, and it contradicts `EF-055`; two candidate
    causes recorded, neither ruled out. (2) The frozen spec promises the dialog
    says *"(drone speed and carry capacity are back to the game's own values)"* and
    the code prints a bare *"2 drone stat dials"* — step ③ would have shipped a
    text the build does not produce. (3) Two defects in my own instruments (the
    Test Kit's on-screen output covered the dialog it was there to witness; a
    reader applied the removal contract in a packs-present cell and cried wolf).
    ℹ️ Your landscaping-overlay lead is carried as a rider and costs you nothing.
    *The prep note that preceded it:*
    ~~⭐⭐ **THE COMBINED SITTING'S PREP IS *DONE AND MEASURED* — IT IS WAITING ON
    YOUR CHAIR ONLY** (2026-08-13). Three unattended dry-run launches have
    already happened with the game closed and nobody at the keyboard; every
    fixture is verified to exist, the harness is proven, and the predictions
    are committed. **Sit down and say "run the combined sitting"** on a session
    opened at `agent/prompts/COMBINED_SITTING.md`. **Your part: ~30–45 min, four
    launches, two Mod-Manager visits.** The measure-moments (full table in the
    brief):
    * **F102's minute** (packs ON). ⛔ **Two corrections you would otherwise have
      hit at the keyboard.** There is **no save called `Sylmacaink BH25`** — all
      88 were read at their headers and nothing carries that name. And there is
      **ONE** deposit sign on your campaign's asteroid, not three. ⭐ The rig
      switches to the asteroid map and *selects the deposit for you*; you only
      look. Everything else is already measured: the fix's LoadGame sweep fired
      on it (`1 … re-signed onto the clean entity`), the deposit reads the new
      entity, and `ExoticDepositSign [active]` is in the log. Your words:
      **"sign renders: yes/no"**, **"selectable: yes/no"**. Closes item 11's
      local half.
    * **PT-20 redo done RIGHT**: your Mod-Manager disable of **both** packs
      (Test Kit stays) + **full restart** (state 3 — the old 98-vs-98 may have
      measured the half-disabled state) + ~10 min ordinary play + one save and
      reload; every rig reading carries its `pack=0/0` gate line.
    * ⭐ **D13 attended after-sweep, same state-3 window**: you load a staged
      big-save copy and WATCH — the two dialogs write no log line, so your
      eyes are the only instrument that can ever sample them (report dialog
      raises with the frozen text; second load silent; stand-down dialog once
      after you re-enable). **A clean run here is what finally grants D13
      `tested`.** ⭐ The staged save carries **both Drone stat dials natively**,
      so you will watch the artifact take off the one piece of residue that keeps
      changing a player's game after they uninstall.
    * Optional: the CAPTURE_SITTING passes that fold in (item 24) — prep worked
      out which pass rides which launch, and they cost no extra restarts.
    ℹ️ **Two things prep found and fixed, no decision owed.** (1) Leaving Save
    Rescue installed for the PT-20 leg would have silently voided it — it would
    have stripped the very leftovers PT-20 exists to prove are harmless. It is
    now pulled for that leg and restored afterwards, agent-side, at no cost to
    you. (2) ⛔ **A byte copy of an autosave is still an autosave to the game's
    rotation, and it deleted this sitting's own fixture *and* your held
    `Autosave Sol 311` during prep.** `Sol 311` was **restored byte-exact** from
    the pre-copy; the fixture was re-staged from a save that is not an autosave;
    `EF-056` is amended. Nothing of yours is lost.~~
    ⚠️ **The autosave rotation fired twice more DURING the sitting** — it took
    `Autosave Sol 311` and `Autosave Sol 311(2)` while you played, and wrote
    `Autosave Sol 316`. **Both restored byte-exact**, and every autosave was
    re-verified at close-out. That is the amended rule paying for itself three
    times in two days, and it is why it now says reconcile after *every* launch
    rather than reason about which one will fire.
    ✅✅ **RULED 2026-08-15, AND THEN AMENDED THE SAME DAY BY YOU — THE SPLIT IS
    ADOPTED AND IT IS ALREADY BUILT.** Your first answer was "a sitting with me
    at the keyboard earns `tested`", which would have left every unattended
    verification stuck at `fixed`. You then backtracked on exactly that
    consequence: *"If we are changing rules I think I would be more comfortable
    with labeling things tested - unattended / tested attended. It still gives
    unattended appropriate weight, but allows the attended tested to have more
    serious weight if we are troubleshooting, because that has the approval of
    the agent and human hands on."* **Adopted as written.** The vocabulary now
    has three words and `doccheck` enforces them:
    * **`tested-attended`** — you were at the keyboard. The strongest word the
      project has, and the one a troubleshooting session is entitled to lean
      on: agent instrumentation *and* human eyes.
    * **`tested-unattended`** — real launches, nobody watching. Full weight for
      anything an instrument can read; ⛔ **never for a screen event** — "the
      flag read false" is a measurement, "the popup visibly paused" is not.
    * ⛔ **bare `tested`** — LEGACY, closed to new work. See the honest caveat
      below.
    ⭐ **Applied immediately, and it pays today:** `F85` and `C39` were verified
    unattended last night with real launches and zero errors, and they move
    **`fixed` → `tested-unattended`** rather than being stranded. No evidence
    changed; the word for it did. What `tested-attended` would still buy is
    named on each entry (F85: the screen witness — does the popup visibly
    pause; C39: seven of eight families still SOURCE, and the law was enacted
    directly rather than voted).
    ⚠️ **The honest caveat, and it is why the old word survives.** 46 entries
    already carry bare `tested` and **their attendance was never recorded** —
    29 at least cite a sitting or co-run, but **17 carry the literal word
    `tested` and no narrative at all** (`F03`, `F44`, `F66` and 14 others).
    Retro-labelling them would mean stamping an attendance claim on entries
    whose record cannot support one, which is the exact failure mode the
    evidence bar exists to stop. So bare `tested` now means **"attendance
    unaudited"** — not "attended" — and no agent may read it as the stronger
    word or promote it without re-deriving from the archived record.
    ✅ **RULED 2026-08-15: NO RETRO-PASS.** The 46 legacy labels are left exactly
    as they are and are never upgraded in bulk. ⛔ **Standing consequence, for
    any agent reading one:** bare `tested` is an unaudited label — cite it as
    "recorded `tested`, attendance unknown", never as evidence a human watched.
    If a specific legacy entry ever becomes load-bearing in a real
    investigation, re-derive that ONE entry from the archived record; do not
    reason from the word. ~~whether you want that retro-pass done at all.~~
    ~~the status vocabulary has no word for "verified-unattended" (`doccheck`
    rejects `verified`), so that truth lives in narrative only.~~
    ℹ️ Also for your awareness, no decision owed: the audit FILED **F103**
    (our Crystals-mystery repeater can double its hourly broadcast after a
    mid-mystery load — harm nil, one consumer that wants the message,
    self-limiting three ways; remedy sketch recorded) as post-release WATCH
    under your frozen ship line.

### ⭐⭐ NEW 2026-08-12 — THE SHIP LINE (three rulings, decided in the process-audit review session)

14. ~~**⚖️ Is `fixed` + suite + self-checks enough to ship, or does the
    evidence campaign finish first?**~~ ✅ **DECIDED 2026-08-12, your ruling:
    "I don't want to drop quality, but I think in some ways we are over
    testing… if there are things that we can say 90+% chance this is good, I
    am not sure its worth the added hours."** Three parts, all recorded:
    * **The `fixed`→`tested` evidence campaign is FROZEN until after release.**
      The shipping bar is what already runs mechanically — the automated suite
      (⛔ **RE-MEASURED 2026-08-13** — the suite is now **94** probes and the
      both-mods read is **78 pass / 0 fail / 16 skip / 0 error**, the six extra
      skips being the new Save Rescue probes standing down because that mod is
      not part of your standing rig; with it loaded the same run reads
      **84/0/10/0**. Log `archive/rs_r0_Mars.exe-20260813-11.42.08.log`. The
      88-probe 78/0/10/0 this ruling was made against is the same bar, and the
      pre-split 77/0/10/0-of-87 before that — the only verdict change in the
      whole sequence is the deliberate Mod-Options check split),
      per-fix runtime self-checks, the
      fail-safe registry and per-fix veto, and the completed save-safety tier
      (F86 Tiers 1+2, verified). Keyboard re-witnessing stops being scheduled work;
      it may resume against the released mod if you still want it.
    * **Perpetual riders → post-release WATCH items** (C42, F99, F80, the
      F96 meteor coincidence): each has failed to produce its own precondition
      3+ times; they leave every chain's freight. A symptom appearing in your
      game still takes its tap.
    * **D13 stays BLOCKING, at hours-scale.** You challenged the audit-review
      estimate ("adds a week") and you were right — testing is: build the
      artifact, probe it, uninstall on a big save, run the after-sweep — a few
      hours unless it finds something. The heavy part is agent-side (the
      authoritative exposed-set derivation + the curated keep/remove list —
      some residue IS the repair and must survive). ⚠️ One design question is
      yours at spec time, deliberately reserved on the entry: what the player
      DOES with the artifact (run-after-removal / keep-installed /
      pack-is-own-cleaner). The spec session asks it; nothing owed before then.
    **What this buys: the release front is now the only main line** — D13
    chain + `unattended-3` in parallel (agent), then ONE combined sitting
    (PT-20 redo + D13 verify + the F102 minute), then MOD_DESCRIPTION +
    disposition table (agent), then your ~1–2 h of launch tasks. → the review
    that prompted this: your process-audit artifact + `agent/reports/`
    replies, SESSION_LOG 2026-08-12.

15. ✅ **DECIDED 2026-08-12, your order: the 8 opt-in modules split into a
    STANDALONE opt-in mod** (ClassicRockets, AcknowledgedWarnings,
    ResidencyControl, MultipleSuns, DroneOverhaul, CohortHousing, NoHomeless,
    DroneStatDials — the `optional = true` files). **Sequenced BEFORE D13, by
    D13's own rule:** the cleaner's exposed-set derivation must see the FINAL
    module sets, or it gets done twice. What the split chain owns: map the
    shared-framework coupling first (registry, logging, Mod Options bridge —
    the standalone mod needs its own slim copy or a deliberate dependency);
    move the files + their probes; re-derive every baseline the split resets
    (gate reads 81/81 → main + opt-in pairs, suite tally, doccheck counts).
    ⚠️ Scope you accepted with it: a second mod = its own metadata,
    description, preview image and portal pass at launch, and the D13 rescue
    artifact covers residue from BOTH mods (one artifact — spec-time detail).
    Nothing owed by you until its verification lands in the combined sitting.
    ⭐ **CHAIN AUTHORED 2026-08-12, same session, to your sharpened order**
    (*"true standalone… work with or without the bug fix mod… all our hard
    fault work makes it over… cleanly load its folders and just work on it"*):
    `agent/prompts/split-optins/` — design → fresh-context QA gate → build →
    three-cell verification matrix (+ a save-compat witness on a `CP15PT15`
    copy) → terminal audit with a no-retraining acceptance test run from the
    new repo alone. Binding invariants: zero `SMRFixPack` references in the
    standalone; **persisted names keep their exact bytes** (your saves are the
    contract); module behaviour unchanged. Three small calls come back to you
    later, none blocking: the mod's display name (launch prep), whether the 8
    default ON or stay opt-in-OFF in their own mod (design will recommend),
    and a one-minute Mod Options re-tick after the split (new mod id = fresh
    toggle state).
    ⭐ **DESIGN'S RECOMMENDATION IS IN (2026-08-12, chain prompt 1): keep them
    OFF by default — one line from you either way, and the build proceeds with
    OFF unless you say otherwise.** Why: flipping the default is itself a
    behaviour change (outside the chain's scope fence), and three of the eight
    are not things you'd want on unasked — `DroneOverhaul` is labelled
    *experimental* on its own toggle and is frozen pending PT-52,
    `NoHomeless` moves colonists between domes with an unwind that is still
    unverified, and `CohortHousing` re-homes Seniors and Children.
    `ResidencyControl` and `NoHomeless` also each add a row to every Dome
    infopanel. Installing the mod buys the *choice*; the page costs one visit,
    which the re-tick above already asks of you once. ⚠️ Counter-argument,
    recorded so it is your call and not a fait accompli: everyone who installs
    that mod has already opted in once, so a second opt-in per module is
    friction — and if you prefer ON it is two lines per module in
    `items.lua` + `metadata.lua`, **nothing in `Code/`**, so it stays cheap to
    revisit after release. Reasoning: `agent/prompts/split-optins/90_DESIGN.md`
    §3.7.
    ⭐ **Your standing condition, recorded 2026-08-12:** *"Once we get it
    seperated I will keep the opt ins loaded in as they make testing easier."*
    → now a dormant WORKFLOW rule the split's audit activates: both-mods
    -loaded is the rig's NORMAL config; agents expect it, attribute opt-in
    lines instead of flagging them, name a confound only where a reading
    intersects what an opt-in changes, and any leg needing the opt-ins OFF
    declares it in its brief (a Mod-Manager toggle needs a full restart).
    Your ordinary play doubles as the continuous both-mods compatibility
    soak. Nothing owed.
    ⭐⭐ **BUILT 2026-08-12 (chain prompt 3), and ✅✅ VERIFIED THE SAME EVENING
    (prompt 4): the whole matrix is GREEN and it cost you ZERO minutes.**
    ✅ **Your minute is already spent — you did it at 18:30, before the leg ran**
    (enabled the mod, re-ticked the seven toggles and both dials at `5x` / `+2`).
    Nothing further is owed here, and ⭐ **your run turned out to be evidence**:
    it is the only recording that will ever exist of the fresh-default state, and
    it read exactly the predicted `1/8` with all seven modules `inactive`.
    **What the verification proved, in your terms:**
    * **Your saves are fine, and this was tested two different ways.** Four of
      your saves were read back (a copy of `CP15PT15`, a copy of `CP60RT`, a copy
      of `Autosave Sol 311`, and the PT-35 fixture): every dome policy and every
      drone dial the old single-mod pack ever wrote into them is still found, by
      the new mod, under its exact original name. Then the leg *wrote* all three
      policy fields onto 11 domes and 4 buildings, saved, reloaded, and got every
      one of them back on the same objects — **0 of 3 broke**.
    * **The bug-fix pack is untouched.** Across all 88 automated probes the only
      difference from before the split is the one deliberate change (the Mod
      Options check split in two, because there are two pages now). 86 of 86
      shared results are identical.
    * **Both mods work alone and together.** The opt-in mod ran with the fix pack
      completely uninstalled, and the fix pack ran with the opt-in mod completely
      uninstalled, both clean, no errors anywhere.
    ⚠️ Two smaller things the build learned, neither needing a call: the fix
    pack now has **no Mod Options page at all** (it has no options left, so the
    engine correctly stops listing it — do not report it as missing), and the
    display name above is still a PLACEHOLDER awaiting your launch-prep call.
    ⚖️⚖️ **AUDITED AND CLOSED 2026-08-12 (chain prompt 5, terminal audit): every
    matrix verdict re-derived from the archived logs and SUSTAINED.** All nine
    logs byte-compared identical to their originals and read whole; every tally
    recounted from the verdict lines themselves; the standalone claim re-proven
    by my own greps (fix-pack global nil in cell b; zero `SMRFixPack` references
    in the new mod's code); every persisted name re-derived from the shipped
    code and matched to the save readings name-by-name; the junction route
    (EF-055) re-derived from Src leg by leg. Two precision corrections, neither
    touching a verdict: "86 byte-identical rows" means 86 identical VERDICTS
    (5 rows' message text differs benignly — save-state/RNG, one of them
    independently confirming your dial change), and the 18:30 log you produced
    is now archived in the repo (it was load-bearing and only on the rotation).
    ✅ ~~Still yours, none blocking: the display name · the OFF default~~
    **BOTH DECIDED 2026-08-13, your rulings:** display name =
    **"Community Fix Pack: Opt-In Modules"** *(the family prefix was renamed by
    your 2026-08-17 ruling, item 36 — the name is now "Relaunched Fix Pack:
    Opt-In Modules")* (family-prefixed so the two mods
    sort together — swept the same day across all 15 player-visible sites in
    11 files, parse sweep GREEN, pushed `e17586b`; mod id / global / log tag
    unchanged, they are save contract) · **default-OFF RATIFIED** (as built
    and verified; two-line flip stays cheap post-release if you change your
    mind). The re-tick minute is spent; nothing else is owed.
    ✅ ~~whether the new repo gets a GitHub remote~~ **DECIDED 2026-08-13, your
    ruling: PUBLIC, same as the fix pack.** Live at
    `github.com/catt144/SMR-CommunityOptInPack` — all 6 commits pushed, tree
    clean, `git pull` resolves (so the D13 chain's staleness check reads it
    without tripping). ⚠️ **One thing that came out of doing it, and it is not
    caused by it:** your Windows username and SteamID64 were written into the
    public docs of BOTH repos (a hard-coded save-folder path in `EF-050` and
    `PLAYTEST_HELP`), and a SteamID64 resolves to your Steam profile. ✅ **SCRUBBED
    2026-08-13 at your word** — every live doc in both repos now says
    `%USERPROFILE%\Saved Games\Surviving Mars Relaunched\<steam-id>\`, which is
    equally usable. ⛔ **Read the sibling item below before assuming that closed
    it: the string is still in git HISTORY on both public repos.**

### ⭐⭐ NEW 2026-08-12 — THE SAVE-RESCUE ARTIFACT: three calls, and the derivation is done

The D13 chain's first prompt has finished the hard agent-side part — the
authoritative exposed-set derivation over BOTH shipped mods, from source, no
inherited count. **27 sites, every one with a disposition.** These three are
yours. Items 17 and 18 were reserved for you on the entry; item 19 is new and
is the one thing the derivation found that I will not decide alone.
Reasoning for all three: **`agent/reports/D13_EXPOSED_SET.md`** (promoted
2026-08-13 to its permanent home — the chain folder it was drafted in is
deleted when the chain closes).

17. ✅ **PUBLISH HALF RULED 2026-08-14: hold off.** Save Rescue is **not
    published at launch** — held in reserve, to be launched **if post-release
    reports show players stuck with the problem it solves** (the dial residue).
    The card stays ready (`RELEASE_DESCRIPTION_RESCUE.md`); item **28** closes
    with this ruling: **ship as built** (re-decide the dialog text before
    upload if the contingency ever fires — including the audit's save-step
    line). ✅ **DECIDED 2026-08-13, your ruling: (c) — the packs are their own
    cleaner; the artifact serves ONLY the already-uninstalled.** You first
    challenged the premise ("nobody but me has ever run the pack — why build a
    cleaner at all?") and then **reaffirmed the 2026-08-01 launch-dependency
    ruling** on the honest version of the case: the population is empty until
    launch and the residue never expires (the tool works retroactively), so
    the real reasons to build NOW are the open sequencing window (derivation
    frozen + QA'd against exactly these trees) and day-one messaging — and
    **build ≠ publish**: whether/when the rescue goes to a store stays a
    release-time call (noted for the release checklist). The ask as it stood:
    ⚖️ **What does the player actually DO with the rescue artifact?**
    (a) run-it-after-removal · (b) keep-it-installed as a permanent runtime ·
    **(c) the packs already clean themselves and the artifact serves ONLY the
    already-uninstalled case ← my recommendation, and the derivation now backs
    it with specifics rather than architecture.** Why (c): the two residues
    that ever *did* anything after uninstall are already healed on load by the
    packs themselves (the meteor thread restarts onto the game's own body; the
    rain loops migrate onto the game's own body). What is left is inert named
    data — **except one thing**: a save made with a drone dial off base keeps
    that boost **permanently** after you uninstall, and a player who has
    already uninstalled cannot run any in-pack pass. That is a real population
    and it is what the artifact is for. **Cost of each option:** (c) is the
    smallest — one load-time pass, no UI, no extra surface; (a) adds an invoke
    path that has to work on a gamepad for console players; (b) is not a
    cleaner at all but a mod you maintain forever, and it re-opens the "what
    does *it* leave in the save" question we just closed. ⭐ Under (c) the
    artifact may end up with **no thread surgery whatsoever**, which would make
    it markedly smaller and safer than every earlier sizing — one open
    question in the derivation decides that, and the QA prompt attacks it next.
    **QA update (2026-08-13): the attack ran, and the answer is "smaller, but
    not zero."** The derivation held up everywhere else, but "no thread
    surgery" only covered saves the *current* pack has touched — the rescue's
    real audience includes people who uninstalled an **older** version, whose
    saves can still carry a dead meteor timer or an old rain loop. The QA
    verdict keeps two small, one-shot repairs in the plan (both re-use the
    game's own machinery; the meteor one costs a one-time timer re-roll, which
    the tool will say out loud). **Nothing about the (a)/(b)/(c) choice
    changes — (c) is still the recommendation.**

18. ✅ **DECIDED 2026-08-13: CONFIRMED — mod-shaped.** Same day you also
    **ratified the naming proposal** (display "Save Rescue" · repo
    `SMR-SaveRescue` · mod id `SMR_CommunitySaveRescue` · log tag
    `[CommunitySaveRescue]`) and **pre-created the public remote yourself**:
    `github.com/catt144/SMR-CommunitySaveRescue`, empty — prompt 3 scaffolds
    into it (note: the remote's name differs from the proposal's repo folder
    name; prompt 3 aligns the local folder to the remote). Publishing the MOD
    to a store stays a release-time call. The ask as it stood:
    ⚖️ **Confirm the artifact is built AS A MOD (not a console procedure) —
    and that this makes the channel question stop blocking.** I verified the
    argument against your own Paradox Mods check (2026-08-01), not from
    assumption: that audience has no console, so a rescue path that means
    typing commands reaches **nobody** there — while a mod-shaped cleaner
    installs through whichever channel the player already uses, on PC and on
    Xbox/PS5 alike. Its reach is a strict superset on every platform, so
    "which channel do we publish to" no longer changes what the artifact *is*.
    **Recommendation: confirm mod-shaped**; it costs a third small repo (I have
    the scaffolding proposal ready, deliberately thinner than the opt-in
    pack's — no options page, no toggle machinery). ⚠️ Channel note, separate
    and still open from your own browse: searching Paradox Mods for `bug` or
    `fix` returned **zero** hits while searching your author name worked — a
    naming/listing problem for the store page, never re-checked, not a code
    one.

19. ✅ **DECIDED 2026-08-13: GO — build the three gates in-pack. ✅✅ DONE the
    same day** — all three gates inserted (`Fix_CrystalMysteryHang:78`,
    `Fix_ExtenderFlapChurn:96`, `Fix_TrackConnectorPingPong:179`), the four
    modules' save-footprint disclosure rewritten, parse sweep and doccheck
    GREEN, module/file/probe counts unchanged. **Nothing for you here** — no
    behaviour change while installed and nothing to look at in game; the gates
    only matter in a save the pack has been removed from. One thing found on
    the way and NOT changed, disclosed in the code and routed to the next
    prompt: after a load, the crystal repeater restored with the save cannot be
    stopped by the handler that stops the fresh one, so during that mystery the
    hourly re-announce can double up — inert (the message has exactly one
    listener, which wants it), unmeasured. The ask as it stood:
    ⚖️ **Three of our own background threads have no "the mod is gone" exit,
    and I want to fix that in the packs before building any cleaner.** The
    rule we wrote says every mod-owned background body must check whether the
    mod still exists each time it wakes. One of four does
    (`MeteorStormWedge`). The other three — the crystal-mystery repeater, the
    extender-flap debounce, the track-connector reclaim — are written entirely
    in the game's own vocabulary, which under the corrected rules is exactly
    the case that **keeps running after you uninstall** rather than stopping.
    Worst case today is small and not an error (the crystal one re-broadcasts
    a message hourly for up to 10 sols in a save we no longer occupy), but it
    is undisclosed, and a cleaner cannot reach it by construction — those
    bodies run *from* the save the moment it loads. **Recommendation: build
    the fix in-pack now — three one-line insertions, no behaviour change while
    installed, no new save state, one short prompt inserted before the build
    step.** Our own policy bars handing this to the cleaner instead ("the
    cleaner is not a scoping escape hatch" — your words). Say go and it rides
    the chain; say no and all three get recorded as accepted residue instead.

26. ~~**⚖️ ONE 15-SECOND ACTION: tick "Save Rescue" and restart**~~
    ✅✅ **DONE BY YOU 2026-08-13 at 11:16, and the tool has now been TESTED on
    the back of it. Nothing here is owed from you any more.**
    Your tick is in the game's own log (`SaveRescue: ready`), and the whole
    verification ran unattended off it: **nine launches, about eight minutes of
    machine time, zero minutes of yours.**
    ⭐ **What it actually did, on a real save carrying real leftovers:** it
    removed **1617** items across all eleven names it targets — including both
    Drone dials, the ones that otherwise keep boosting your drones forever with
    the mod gone — **kept both of the leftovers that ARE repairs** (the Wind
    Turbine buff and the track latch), restarted a stalled rain cycle and a dead
    meteor timer, and left **nothing of its own** anywhere in the save. Loading
    the cleaned save a second time it correctly did nothing at all. No errors in
    any cell.
    ⚠️ **One honest caveat, and it is small.** We claimed the tool leaves "zero
    lines" behind once removed. Measured, there is exactly one — the game itself
    notes `Savegame references Mod Save Rescue … which is not present` on the
    first load after you uninstall it. **This is not special to this tool: the
    Fix Pack and the Opt-In Modules do exactly the same**, and the note
    disappears the next time you save. It will be said plainly in the mod's
    description rather than papered over.
    ✅ **RULED 2026-08-15: the display name becomes "Community Fix Pack: Save
    Rescue" — pre-approved, applied only IF the tool ever publishes** *(the
    family prefix was renamed by your 2026-08-17 ruling, item 36, so the name
    to apply at publish is now "Relaunched Fix Pack: Save Rescue")*. Your
    words: *"This is fine for if we ever need it."* ⛔ **Deliberately NOT applied
    today:** item 17 holds the tool unpublished, so the rename rides the
    pre-upload pass that the contingency already mandates — the same pass that
    re-decides item 28's dialog text and adds the audit's missing save-step
    line. Recorded at the point of use in the rescue card's header so it cannot
    be forgotten there. One line in one file when the day comes.
    ~~the display name is **"Save Rescue"** as you ratified it, but the same day
    you renamed the opt-in mod to *"Community Fix Pack: Opt-In Modules"* so the
    family sorts together in mod lists.~~
    ⚠️ **Your rig is exactly as you left it** — both packs back at `74/74` and
    `8/8`, drone dials still `5x` / `+2`, all seven opt-in toggles still on, and
    every save you own byte-identical (the four protected ones were MD5-checked
    either side). Save Rescue itself is installed but **not** loaded, by design:
    it is a repair tool, not a standing mod, and leaving it out costs you
    nothing — measured, a pulled mod produces no log line at all.

### ⭐ NEW 2026-08-13 — public documentation: platform decided, one question back to you

21. ✅ **DECIDED 2026-08-13, your ruling: GITHUB PAGES** for the player-facing
    docs site. A working scaffold is committed at `public-site/` (MkDocs +
    Material — the sidebar tree, `Ctrl K` search, right-hand page TOC, dark
    theme and callout boxes you saw on the peer GitBook site). It is **free**
    on a public repo, and everything stays as markdown in the repo, which is
    how you already work.
    ⛔ **Nothing is on the public web.** The build workflow is manual-trigger
    only and Pages is not enabled on the repo, so the site does not exist
    publicly until you choose to turn it on. The four pages in it are marked
    LAYOUT SPECIMENS on their own face — they are there so you can judge the
    feel, not to be published.
    **To look at it, either** (⭐ paths updated for the move — these are the
    live ones, run them from `C:\Dev\SMR-CommunityMods`)**:**
    * **locally** — `python -m pip install mkdocs-material` then
      `python -m mkdocs serve`, open the address it prints; or
    * **live but private-ish** — Settings → Pages → Source: *GitHub Actions*,
      then run *Publish docs site* from the Actions tab. ⚠️ That URL is public
      the moment it builds, so do this only if you are content for specimens to
      be visible for a while.
    ✅✅ **TOPOLOGY DECIDED 2026-08-13, your ruling: ITS OWN REPO — and you
    created it the same evening.** Live at
    `github.com/catt144/SMR-CommunityMods`, public, and the scaffold is already
    moved: local clone `C:\Dev\SMR-CommunityMods`, `mkdocs.yml` and `content/`
    now sit at that repo's root, the manual publish workflow moved with them,
    and both are **gone from the fix pack repo**. ⛔ **Still nothing on the
    public web** — the workflow is still `workflow_dispatch` only and Pages is
    still not enabled; the four pages are still marked layout specimens.
    ⭐ **Two things fixed on the way in, and one deliberately left broken:** the
    sibling mod's decided display name replaced the dead working title, and this
    page stopped claiming that name was unchosen. ⛔ The line about whether an
    opt-in toggle needs a restart is now labelled *do not publish* rather than
    guessed at — two of our own documents claim it both ways and neither has
    been checked against the code. The `public-docs` chain settles it.
    **Nothing further owed by you here.** ~~The ask as it stood:~~
    ⚖️ ~~**THE ONE THING BACK TO YOU: which repo should host the site?**~~
    * **Its own repo** (e.g. `SMR-CommunityMods`) ← **my recommendation.** One
      site covering both mods and the rescue tool later, a neutral URL, and
      nothing ships inside either mod. It is also how the peer site works —
      "Dash's Vault" is one site with a mod tree under it. Costs you the same
      15 seconds as the last repo; the scaffold was built to move in one command.
    * **Leave it in the fix pack repo.** No new repo, but this repo *is* the mod
      (the game's Mods folder is a junction into it), so the site rides along
      inside the fix pack, and the URL would read `…/SMR-CommunityFixPack/` for
      a site that also documents the opt-in pack.
    Nothing is blocked on this — the `public-docs` chain can start either way.
    ⭐ **UPDATE 2026-08-13 (the chain's design prompt ran): the recommendation
    is unchanged but the argument got harder.** I checked whether extra folders
    in this repo actually reach the file players download — see item 23 — and
    they do. So "leave it in the fix pack repo" now also means "remember to
    keep the site out of the upload, forever"; its own repo makes that
    impossible to forget. Still your call, still 15 seconds either way.

### ✅✅ 2026-08-13 — public documentation, part 2: ALL FOUR DECIDED, same day

The `public-docs` chain's design prompt is done and **you cleared every item it
routed, in one sitting.** Full reasoning: `agent/reports/PUBLIC_DOCS_DESIGN.md`.
⭐ **Nothing in this section is owed by you any more** — it stays here rather
than moving to the archive only because item 24's artifact is not built yet.

22. ~~**⚖️ The "judgment calls" wording — DRAFTED, so you approve rather than
    compose.**~~ ✅✅ **DECIDED 2026-08-13: the five bullets SHIP as drafted
    (`PUBLIC_DOCS_DESIGN.md` §9), and the closing line is CUT.** Open since
    2026-08-04; closed after nine days.
    ⭐⭐ **AND YOU CAUGHT A FALSE CLAIM DOING IT.** You challenged the line that
    said the five could each be switched off individually on PC — *"as far as I
    know right now, we have no way to switch off parts of the fix module"* —
    and you were right. What the code says, checked in response:
    * The per-fix veto **is real** and would fully disable all five. But it is
      read at mod load (`00_Core.lua:384-388`), so it only works from **a
      companion mod that loads before ours** — a modder's tool, not a player's.
    * ⛔ **The developer console does NOT work.** By the time anyone can type,
      the fixes are already applied.
    * ⛔ The fix pack has **no Mod Options page** — everything settable moved to
      the opt-in mod at the split, and none of these five are in it.
    ⛔⛔ **The consequence, and it is bigger than the cut line.**
    `archive/MOD_DESCRIPTION.md:487-493` — the frozen text the real store page
    gets built from — tells players to set the veto *"in the console"*. **That
    is false and it would have shipped.** It is now recorded as a correction the
    chain's build prompt must make (§9.1). ⚠️ **Second false claim found in that
    one file** after the F76 explainer; everything else in it is now treated as
    unverified until re-checked.
    ⭐ The standing lesson written down from this: *a claim about what a player
    can DO needs a route check, not a source citation.* The sentence had passed
    a design pass, that file's own review and a chain QA before your instinct
    caught it.
    ⚠️ **AMENDED 2026-08-13 by the QA prompt** — you were right about the *each*,
    and the answer we wrote back was slightly too broad in the other direction.
    Re-reading all five modules: `F97` (dust devils) **can** be switched off from
    the console mid-session, because it re-checks the switch every time it runs.
    The other four cannot. **Nothing you decided changes** — the store page still
    will not offer the console route, because it works for an unpredictable few
    and a player has no way to tell which. Recorded so the file is not wrong.

22b. ~~**⚖️⚖️ ONE LINE FROM YOU — a factual error inside a sentence you already
    approved, and it points the warning at the wrong players.**~~ ✅ **DECIDED
    2026-08-13, your words in the build session: *"You can change any wordings
    to their accurate versions."* SHIPPED as the phrasing you approved on
    08-02 — "on some map settings"** — now the fifth judgment-call bullet in
    the fix pack store description (`agent/reports/STORE_FIXPACK.md`), with
    the six-row rate table recorded beside it per the process rule below.
    The terminal audit re-derived the bullet from the entry's own table
    (`agent/bugs/F97.md`: the heaviest preset is the one that does not change
    at all; the increases land on the light and middle presets; and the OG
    disassembly shows the defect spans both games, so "than the game has ever
    actually delivered" holds) and sustained the shipped wording. "Most map
    settings" was deliberately NOT used — truer-sounding, never approved.
    The original ask, kept for the record:
    ⛔ Not a
    re-litigation: the fifth judgment-call bullet's **substance is right and
    stays**. One phrase in it is backwards.
    * **What it says now:** *"On the heaviest settings that means noticeably
      more dust devils than the game has ever actually delivered."*
    * **What the numbers say** (the per-fix rate table, re-derived from our own
      entry): the **heaviest** setting is the one that does **not change at
      all**. The settings that change most are the light and middle ones — about
      half again as many devils on the common ones, and more than double on one.
    * **How it happened:** an earlier report of ours said "the default preset is
      untouched", the draft trusted it, and the wording drifted from the phrase
      that was actually approved back on 08-02 — *"on **some map settings**"*.
    * ⭐ **Recommendation: go back to "on some map settings."** It is the
      approved phrasing, it is true, and it is shorter. **Say the word and an
      agent strikes this line.**
    ⚠️ **The process point, which matters more than the sentence.** This is the
    second time in a week a decision reached you as *wording with its evidence
    left behind* — the console line was the first, and you caught that one by
    instinct. Nobody caught this one, because it sounded like the phrasing that
    had already been approved. ⇒ **From now on a wording decision comes to you
    with its evidence beside it** (here: the six-row rate table would have
    settled it in ten seconds). That is now written into the chain.

22c. ~~⚖️ **YES/NO — do we owe a page to the player whose game is broken and who
    thinks it is us?**~~ ✅ **DECIDED 2026-08-13: YES, as a small section** —
    written into prompt 5's brief (`agent/prompts/public-docs/05_BUILD_SITE.md`
    job 4). The original ask: The QA review found this is the one reader our whole
    surface plan has no home for. They arrive annoyed and want three things:
    *is it you · how do I get you out · where do I tell you*. Today the honest
    answer to the middle one is "remove the whole mod and restart", and it is
    written down nowhere a player would look.
    * **Cost:** ~1 agent hour, one short page on the site. **No cost to you**
      beyond this yes/no.
    * ⭐ **Why it may be worth more than it costs:** this is the reader who
      writes the negative review, and they write it from whatever they could
      find in five minutes.
    * **Recommendation: yes, but as a small section rather than its own page** —
      it is three answers, not a chapter.

22d. ~~⚖️ **ONE WORD APPLIES EIGHT CORRECTIONS; ITEM 9 IS A SMALL CHOICE.**~~
    ✅ **DECIDED 2026-08-13: batch APPROVED, and 9(a) chosen — all nine
    corrections are APPLIED to `STORE_FIXPACK.md` / `STORE_OPTIN.md`, doccheck
    GREEN, same session.** The terminal audit re-ran the store sweeps with
    fresh eyes and found nine claims the six build sweeps missed — none
    re-opened anything you decided; every one was a sentence saying more than
    its record supports, each re-derived from code or the entry before it went
    on this list. The list as it was put to you, kept for the record:
    1. Fix pack, twice: *"an official patch that repairs a bug retires our
       version"* — only true when the patch changes the code's shape; our core
       says self-checks **cannot** notice a same-named function edited in
       place (`00_Core.lua:492-497`). Fix: the conditional already live in
       `metadata.lua` — stands down *"if an official patch changes what it was
       written for"*.
    2. Fix pack, drones example: *"a landed rocket cancelled the orders…"* —
       `F50` scopes the defect to **automatic** rockets. Fix: one word.
    3. Fix pack, twice: *"**several** of the stamps clear themselves the next
       time you save"* — exactly **two** do (`D13_EXPOSED_SET.md` §2b D1/D2).
       Fix: "a couple".
    4. Opt-in, Nursery/Retirement policy: *"A new toggle row on **every**
       dome"* — the row deliberately does not exist on domes without cohort
       housing (`Opt_NoHomeless.lua:650-656`), and its Ctrl+click deliberately
       applies to every *such* dome, not everywhere (`:712-732`). The phrase
       is true for the Residency row; the Nursery block copied the phrase, not
       the behaviour. Fix: "on every dome that has a Nursery or Retirement
       Home", "applies it to every such dome".
    5. Opt-in, same block: the quoted row text `off (3 would move)` is not
       what the UI shows — the real title is *"Nursery / Retirement Dome
       (3 would move)"* → *"(3 moving out)"* (`Opt_NoHomeless.lua:700-702`;
       the page matched the design record, the code had moved on). Fix: quote
       the real strings.
    6. Opt-in: *"Seniors and Children stay, even while homeless"* — under
       Forever Young / "Put Them To Work", an **unemployed** Senior is
       workforce and IS movable, on purpose (`Opt_NoHomeless.lua:140-150`:
       "in such a colony a jobless Senior is not a retirement signal"). Fix:
       one clause carving out senior-work colonies.
    7. Both texts: the dial uninstall recipe never says **press Apply** — the
       dials only change on Apply or load (`Opt_DroneStatDials.lua:142-149`);
       a player who sets the dropdowns and backs out of Options has cleared
       nothing, then saves, then uninstalls, and keeps the boost the warning
       exists to prevent. Fix: "(press Apply)" inside both recipes.
    8. Opt-in, Multiple Suns: *"solar panels only ever check the first sun"* —
       the recorded defect is one-directional (`F39`: panels **built** near a
       second sun never bind; the reverse direction works). Fix: "panels
       built near a second sun never connect to it".
    9. ⚖️ Opt-in, drone dispatch overhaul — the page states *"repair and
       cleaning jobs go to the closest hub's fleet first"* as delivered
       behaviour. The only A/B (PT-52 B2) measured the gate firing **once in
       25 malfunctions** — the entry's verdict: *"the claim gate did
       essentially nothing"*, because resource-needing repairs go to the
       **delivering** drone before dispatch ever runs — and you ordered a v1
       rebuild 2026-07-31 (`D06.md:46-69`). "Experimental" is kept, but it
       discloses immaturity, not a measured null.
       * **(a) Recommended:** keep the mechanism claims, add one honest
         sentence — most repairs are decided by who delivers the parts, which
         this module leaves alone; it matters most for repairs and cleaning
         that need no resources.
       * **(b)** Leave it until the rebuild lands and rewrite then.
    ⚠️ Noted for awareness, no action owed: every console/controller route in
    both texts is source-derived, none play-verified (the build ledger says
    the same); and "back it up" names no backup route a console player can
    walk — the honest console form, if you want it, is "make an extra named
    save first".

23. ~~**⚖️ Folders in this repo that aren't part of the mod are currently going
    into what players download — including `CLAUDE.md`.**~~ ✅ **DECIDED
    2026-08-13, your ruling: YES, add the missing patterns — AT LAUNCH PREP.**
    Recorded on the release step list so it lands in the same pass that bumps
    the version and refreshes `last_changes`. ⛔ **All THREE mods**, including
    the rescue mod, whose `metadata.lua` nobody has checked for this yet.
    Nothing owed by you. The finding as it stood:
    Found while checking
    something else for item 21, and I did not fix it because it is a code change
    and outside that chain's fence.
    **What I verified, in the game's own source:** uploading a mod runs
    `CreatePackageForUpload` (`ModTools\Src\CommonLua\Classes\GedModEditor.lua`
    `:678-741`), which lists **the entire mod folder recursively** and packs
    every file that does not match one of the `ignore_files` patterns in
    `metadata.lua`. We ignore eight patterns: `.git`, `.svn`, `Source`,
    `SourceData`, `docs`, `.claude`, `README.md`, `.gitignore`.
    **What that misses today:** `tools/`, `CLAUDE.md`, `LICENSE`,
    `.gitattributes`, in every mod repo — and now that there are three mods,
    the rescue mod's own `metadata.lua` has never been checked for this at all.
    ⭐ **The docs site used to be on this list and no longer is** — it moved to
    its own repo the same evening (item 21), which is the one part of this that
    fixed itself. The rest did not.
    None of it *runs* — only files listed in `metadata.lua` execute — so
    nothing is broken and nothing is a security problem. But `CLAUDE.md` is
    agent instructions, and shipping it inside a player's download is the exact
    "player lands in our working notes" problem the whole docs-site design
    exists to prevent, just delivered to their disk instead of their browser.
    ⚠️ **One sub-case I could NOT verify:** whether `.github/` slips past the
    `.git` pattern depends on an engine function with no readable source. The
    other four match nothing under any reading.
    **Recommendation: add the missing patterns to both repos' `ignore_files` at
    launch prep** — a handful of lines, no behaviour change, no new save state.
    ⇒ **Your job: a yes.** If you would rather ship them, that is fine too and
    I will record it; I would just rather you chose it than inherited it.

24. ~~**⚖️ Preview art ×2 (×3 if the rescue tool publishes)**~~ ✅ **DECIDED
    2026-08-13, your ruling: BUILD A PLAIN TREATMENT NOW AS A FLOOR.** An agent
    produces a simple, clean text-on-image preview for each mod inside the size
    limits, so **launch can never be blocked on art**. ⭐ It is explicitly a
    floor, not a ceiling — replacing it later costs nothing and touches nothing
    else. **Queued as agent work; nothing owed by you.** ⚠️ It is the one item
    here with no artifact yet, which is why this section has not moved to the
    archive. The reasoning as it stood:
    Routed NOW
    because it is the only launch item with no ceiling. Everything else in
    the public-docs plan is agent hours or a decision from you; the preview
    image is neither. It does not get better with agent time, it is not a
    screenshot, and it is the first thing anyone sees on a store card.
    **Constraints already on record:** Paradox Mods ≤ 2 MB, Steam ≤ 1 MB.
    **The options, priced honestly:** make them yourself · commission them ·
    or ship a plain text-on-image treatment that is *fine* and takes an hour.
    ⚠️ There is no recommendation here because it is a taste-and-budget call,
    not a technical one. The reason it is on your list today rather than at
    launch is simply that the other three items have known endings and this one
    does not.
    ⭐⭐ **CORRECTED BY YOU 2026-08-13, and it improves the plan: the art needs
    the game open, so it cannot run beside D13 and it does not belong on its
    own.** A text-on-image preview wants a backdrop, and a backdrop is a
    screenshot — so **the art and the screenshots are now ONE sitting**, and the
    brief for it exists and is fireable:
    ⇒ **`agent/prompts/CAPTURE_SITTING.md`** — every shot with its framing note,
    ordered so the whole set costs **two game restarts, not one per pair**,
    with the `EF-056` autosave rule at the top and the preview-art backdrops as
    its Pass G. ⛔ **Do not fire it while the D13 chain is live** — that leg
    needs the game too.
    ⚖️ **One thing for whoever schedules it:** `STATE.md` already plans ② ONE
    combined sitting (PT-20 redo + D13 after-sweep + F102's minute). **Most of
    the capture list should ride that sitting rather than be a second one** —
    the brief says which passes fold in and which may need their own save.

25. ~~**⚖️ How one of our own research files talks about real modders**~~
    ✅✅ **DECIDED 2026-08-13, your ruling: BOTH EDITS — ✅ DONE the same
    minute.** `BUG_LIST_AUDIT.md`'s heading now reads **"Not used as sources,
    and why"**, and *"an aggregator repack"* now reads *"aggregates other
    authors' fixes"*. **Every assessment is byte-unchanged**; only the verdict
    tone went, and the reworded heading carries a short note saying why so no
    future session reads it as a softening of the findings. Nothing owed.
    ⭐ The related standing rule needed no decision and is now recorded
    (`PUBLIC_DOCS_DESIGN.md` §7): the public pages credit other authors
    generously, never say what another mod gets wrong, and never say
    "this fixes what mod X doesn't". The ask as it stood:
    `agent/reports/BUG_LIST_AUDIT.md:355-370` lists modders under a heading
    reading **"Rejected (with reasons)"** — `LukeH`, `Ayzo`, `Fizzle Fuze`,
    `Silva/Dash`, `Thorik`, `akarnokd`, `FirestormMk3`.
    **I read the whole section first, and in context it is fair and accurate.**
    "Rejected" means *rejected as a source of bug reports for our list*, not
    "bad mod" — and the surrounding text is generous (`fredware` is called "the
    one to watch"; `LukeH`'s entry credits a genuine fix mod). **Nothing in it
    is untrue and nothing in it is hostile.**
    **Three things still bother me:** the header word reads harshly to anyone
    who lands on that line without the paragraphs above it · "an aggregator
    repack" is a loaded phrase for a factual observation · and ⭐ **`Silva/Dash`
    is the author of the GitBook site you pointed me at as the model for this
    whole documentation chain.** These repos are public on purpose and we are
    about to send players to them, so "will they ever read it" is not
    hypothetical.
    ⚠️ The file is in `reports/`, not `archive/`, so it can be edited — this is
    a live decision, not an academic one.
    **Recommendation: two edits, no facts touched** — retitle *"Rejected (with
    reasons)"* → *"Not used as sources, and why"*, and change *"an aggregator
    repack"* → *"aggregates other authors' fixes"*. Every assessment stays;
    only the verdict tone goes. ⇒ **Your job: yes, no, or your own wording.**
    ⭐ Related and *not* needing a decision from you: the design also proposes a
    standing rule for how the public pages talk about other people's mods —
    credit generously, never say what another mod gets wrong, never
    "this fixes what mod X doesn't". Recorded in §7; say the word if you
    disagree.

> ⛔ **Nothing owed by you in this note — it is here so the pending change is
> visible somewhere you read.** `STATE.md` does not yet mention the public-docs
> chain, and I deliberately did not add it: that file is capped at 60 lines,
> sits at 60/60, and the D13 chain is editing it right now, so two writers means
> one of us silently deletes the other's line. **The line I want added**, once
> D13's chain is quiet: *"⑤ **public-docs chain** — design DONE 2026-08-13
> (`reports/PUBLIC_DOCS_DESIGN.md`); next `02_QA.md`. Platform Pages ✅,
> topology ⚖️ck21. Feeds ③."* **What I would drop for it if the cap binds:** the
> `⛔ Pre-split 82/75/8 … ERA-STALE` sentence — it exists only to stop someone
> quoting three superseded number triples, and both places those numbers are
> now read from re-derive them instead. The next prompt in the chain lands it.

### ⚖️ NEW 2026-08-13 — your Steam ID is scrubbed from the live docs, but NOT from git history

20. ✅ **DECIDED 2026-08-13, your ruling: LEAVE IT.** No history rewrite, ever,
    unless you re-open this: the ID is already on your public Steam profile,
    the live docs are scrubbed so it spreads no further, and every sha
    citation in three repos stays valid. CLOSED — nothing is scheduled and
    nothing rides prompt 5. The ask as it stood:
    ⚖️ **Do we rewrite the public repos' history to remove your SteamID64, or
    leave it?** The live files are clean as of today; the string is still in the
    commits behind them, and GitHub serves those to anyone.
    **Measured, both public repos:** fix pack **104 of 828 commits**, across 9
    files — `PLAYTEST_HELP`, `PLAYTEST_CHECKLIST`, `EF-050`, and six consumed
    prompt/spec docs (`corun-pt15`, `corun-pt60` ×2, `corun-rig`,
    `split-optins` ×2). Opt-in repo **7 of 7 commits**, one file (`EF-050`,
    which arrived by the whole-facts-folder copy at the split). The TestKit is
    clean and has no remote anyway.
    **What removing it costs, and this is the real reason it is your call:**
    it means `git filter-repo` + a force-push, which **rewrites every sha in
    both repos**. This project cites shas constantly — `90_DERIVATION.md:11`
    pins the D13 derivation to fix-pack `155869a` / opt-pack `a90d128` /
    TestKit `62f03da`; SESSION_LOG and the archived records cite dozens more;
    several docs tell a future session to run `git show <sha>:<path>` to
    recover a consumed prompt. **Every one of those pointers would break**, and
    the D13 chain is mid-flight right now.
    **The three ways out:**
    * **Leave it.** Costs nothing, breaks nothing. A SteamID64 is not a secret
      in the way a token is — it is on your public Steam profile already; what
      it adds is a link between this GitHub account and that profile.
    * **Rewrite after D13 ships**, when no chain is mid-flight and the sha
      citations can be re-pinned in the same pass. Cheapest safe version.
    * **Rewrite now** — I would not recommend it while D13 is live.
    ⚠️ Whichever you pick, the scrub already done stops it spreading further.

### ⛔ NEW 2026-08-12 — I DELETED ONE OF YOUR AUTOSAVES. Telling you straight.

16. ⛔ **`Autosave Sol 306` is gone and I cannot get it back. `Autosave Sol 311`
    is fine — I restored it byte-for-byte.** No decision is owed; this is a
    report, and the only thing you might want to do is check whether Steam Cloud
    puts `Sol 306` back next time you launch (cloud is still ON).
    **What happened.** The verification leg loaded *copies* of `CP60RT` and
    `Autosave Sol 311` to read your dome policies back off real saves. Copies are
    the rule precisely so your originals are never touched — and the originals
    weren't. But a copy of your campaign **is still your campaign**, so the
    game's own autosave timer kept running, wrote a fresh `Autosave Sol 311(2)`,
    and its rotation then deleted the older autosaves to stay under your autosave
    count. That is vanilla behaviour (`Savegame.lua:1484-1528`), triggered by me.
    **`Sol 311` survived only by luck** — the leg happened to be holding a byte
    copy of it as a witness, so I put it back with its exact bytes and its
    original timestamp. `Sol 306` was never copied, so there is nothing to
    restore from.
    **What stops it recurring:** recorded as `agent/facts/EF-056` — any future
    leg that loads a copy of a real campaign must byte-copy every autosave first
    and list them by name at close-out. "Use a designated copy" protected the
    file; it did not protect the folder, and nothing in the rules had noticed
    that gap before tonight.
    ⚖️ **Audit check, 2026-08-12 evening: `Sol 306` has NOT come back** — the
    save folder re-listed by name during the terminal audit; 79 `.sav`, no
    `Autosave Sol 306`, `Autosave Sol 311` still byte-exact (MD5 re-read), the
    leg's own `Autosave Sol 311(2)` still present (inventoried for the
    post-untick cleanup). The Steam-Cloud check at your next launch stays live.

### ⭐ NEW 2026-08-12 — asteroid Exotic-Minerals freeze (decided in-session; one owed minute)

11. ✅✅ **DONE 2026-08-14 — THE OWED MINUTE IS PAID, nothing further owed by you.**
    Moment C of the combined sitting. ⛔ Two things the item had wrong and you
    would have hit at the keyboard: **there is no save called `Sylmacaink BH25`**
    (all 88 read at their headers) and your campaign's asteroid carries **ONE**
    deposit sign, not three. The rig switched maps and selected it for you.
    **Your verdict: the sign RENDERS and is SELECTABLE** — it opened
    `Underground Exotic Minerals · 14,935/14,935 · Grade: Very high`, whose number
    is the log's `amount=14935000` read a second way. Log side: `ExoticDepositSign
    [active]`, `1 … re-signed onto the clean entity`, 0 `[LUA ERROR]`.
    ⭐ **One already-placed deposit beat three spawned ones**: it exercised the
    `OnMsg.LoadGame` sweep that the 2026-08-12 console-spawn leg never touched.
    ⭐⭐ **And moment A threw in a free measurement**: with both packs disabled the
    same deposit reverted to the vanilla sign with zero re-sign lines, so
    "uninstall is clean" stops being a source argument and becomes a reading.
    ⛔ **The CURE is still unverified and still ships disclaimered** — that has not
    moved and only a Linux/NVIDIA player's report moves it. → `agent/bugs/F102.md`.
    *The original item, for the record:*
    ~~**⚖️ `F102` — the community-witnessed asteroid freeze (Linux/NVIDIA):
    ship our entity-retarget fix without being able to verify the cure?**~~
    ✅ **DECIDED 2026-08-12, your ruling in-session: "Lets do option 3, its the
    easiest and safest, and we will just disclaimer it."** Built the same day:
    `Code/Fix_ExoticDepositSign.lua` re-signs subsurface Exotic Minerals
    deposits onto the remaster's own orphaned sign asset; gameplay untouched;
    safety verified (both sign entities ship in vanilla, saves carry nothing
    of ours, harmless if the freeze lives elsewhere). Your two test legs
    (Windows rig + Steam Deck, both clean) established the freeze is
    configuration-gated to hardware we don't own — the disclaimer text for the
    mod page is drafted in the entry, ready for launch prep (MOD_DESCRIPTION
    stays frozen till then). The outreach alternative (asking the community
    mod's author to test on a freezing save) stays available any time you want
    the cure confirmed. → `agent/bugs/F102.md`.
    **Owed: one minute, next time you're in game with the pack updated** —
    load the D-type asteroid save (`Sylmacaink BH25`), eyeball the three
    crystal deposit signs: new art renders, deposits still selectable, and
    `SMRFixPack.ListFixes()` shows `ExoticDepositSign [active]`. That closes
    the local (safety) half; the entry then waits only on witness-class
    reports.

### ⭐ NEW 2026-08-12 — raised by you mid-sitting during `corun-pt60`

**Cost, stated honestly: the brief promised ~40–60 attended minutes and the
sitting took about 95** (13:38 launch → 15:15 quit). **Roughly 45 of those
minutes were your own three challenges and two staged attempts, and every one of
them changed the record** — the trains question became item 12 below, and your two
F34 challenges (the rocket's reserved pad zone, then transports) rewrote that
fix's route documentation from three wrong claims to one correct route. That is
not overrun and is not scored against you. **Ours is about 10 minutes:** the
brief's console order could not be run as written (it assumed a console at the
main menu), and I compounded it by concluding main-menu input didn't work at all
— the log shows it *did* execute and simply never echoed to the screen, so the
extra load I asked you for was avoidable. The measurement legs themselves ran to
budget. ⭐ **What your minutes bought: the P8 decider, which was unrepeatable —
it needed a save written before 2026-08-02, and `USA Sol 302` was the only one.**

12. ~~**⚖️ TRAINS — do the remaining train items get any more of your attended
    time, or do we stop?**~~ ✅ **DECIDED 2026-08-12 — OPTION A: the train
    group ships at `fixed`; the verification queue is CLOSED.** F21 stays
    `fixed` (its restamp was already witnessed organically 08-10), F64 ships
    on the family-witnessed evidence, F11/F48/F91 were at their honest ceiling
    regardless (`agent/reports/TRAIN_SHIP_READY_ROUTE.md`). F80's tap survives
    ONLY as a symptom-triggered watch — no chain may schedule a train leg
    again. ⭐ One correction in your favor found during the audit review: F65
    and F66 (station↔tunnel grid + connector) are ALSO train-group entries and
    both are already `tested` — the group was more keyboard-verified than the
    inventory below said. The original question and record, kept for the
    reasoning:
    Your words, spoken during the PT-60 sitting and
    recorded here rather than only in an agent doc: *"I feel like I have been
    working on trains since day one of this mod and we still aren't done trying
    to fix and verify trains."* **That is a fair reading of the record, and here
    is the record so the call is yours on facts, not on mood.** Fifteen entries
    in `agent/bugs/` are train/track/platform defects — **`tested` (4):** F44,
    F45, F46, F47 · **`fixed`, never owner-witnessed as `tested` (5):** F11,
    F21, F48, F64, F91 · **`fixed*` (1):** F49 · **`wontfix` (2):** F62, F79 ·
    **still open (3):** F80 `investigating`, F99 `filed`, C45 `filed`. Four of
    the checklist's own test legs are train legs. **What that inventory says:
    the train FIXES are done — twelve of fifteen are built or deliberately
    written off, and nothing on the list is waiting on a train repair.** What
    keeps trains coming back to you is **verification**, not fixing: F21's
    re-earn rider, F80's symptom-triggered tap, and the two `filed` items that
    are rate questions. ⚠️ **F80 is the one that would genuinely cost you** —
    it can only be taken WHEN the symptom appears in your own game, and its
    entry says tapping must happen before you mitigate. **Your call, and any of
    these is a legitimate answer:** (a) close the train verification queue —
    F21 stays `fixed` forever, F80 stays `investigating`, and no future chain
    proposes a train leg; (b) keep only F80's opportunistic tap, drop the rest;
    (c) keep the queue as it stands. This sitting declined F21's rider on its
    own (no instrument in the armed harness) and **nothing here is blocked on
    your answer** — it decides what future chains are allowed to ask you for.
    → the sitting's own record lands in `agent/reports/` at close-out.
    ⭐⭐ **YOUR EXPLICIT ASK, 2026-08-12 — an AGENDA ITEM for the PT-60 audit,
    not a note.** You want the audit session to work out **a route that moves
    the train items into the ready-to-ship column**, instead of every chain
    re-proposing a train leg. ⚠️ **Two corrections the audit must carry into
    that discussion, because they change the question being asked:** (1)
    **nothing train-related blocks the release today** — F21 already ships as
    `fixed` and PT-62's remainder is explicitly NOT a release gate, so this is
    a question about what STANDARD you want (is `fixed` enough to ship, or do
    you want owner-witnessed `tested` on the train fixes before launch?), not
    about unfinished repairs; (2) **C42 is NOT a train item** — it is
    `PassageBase:TraverseTunnel` (dome passages), and it sat beside F21 in this
    sitting's skip list only because both fail for the same reason, a missing
    instrument in the armed harness. ⛔ **The audit does not get to answer the
    standard question itself.** What it owes you is a COSTED ROUTE per
    remaining train item — which instrument each read needs, whether it can
    ever be organic or is forced-only, and what it would cost you in attended
    minutes — so that the ship/no-ship standard becomes one decision in one
    sitting instead of a recurring ask.
    ✅ **ROUTE DELIVERED 2026-08-12 — `agent/reports/TRAIN_SHIP_READY_ROUTE.md`
    (the PT-60 audit).** The one-paragraph version: **three of the five
    unwitnessed `fixed` items (F11, F48, F91) cannot honestly be upgraded by
    any leg at any price** — their guarded states have no organic producer, so
    `fixed` on mechanism evidence is their ceiling and the report says why per
    item. **The two that CAN be bought are F21 (~10–15 min) and F64
    (~5–10 min), together one ~20–30 min rider block on any co-run that stages
    `TEST2H TRAIN`** — the natural host is the PT-20 redo already in the
    queue. F80/F99/C45 stay watch-only (zero scheduled minutes). **So the
    standard question collapses to one decision: ship the train group at
    `fixed` (option A, 0 minutes) or buy the F21+F64 block first (option B,
    one rider block).** Either answer closes the queue; nothing re-proposes
    afterwards.

13. ~~**⚖️ Are cheats on a playtest save a confound that needs defending every
    time?**~~ ✅ **DECIDED 2026-08-12, your ruling mid-sitting — NO, they are
    the normal condition and there is now a standing rule.** Your words:
    *"We really need a standing rule that these saves are play testing saves
    with colonies that are over sized and underindustrialized. They cannot
    support themselves so cheats are needed to keep the colonies alive and
    functional… And unless a chain truely needs a no cheat setup we will
    continue to have to use it, and we will need to prep a save with alot of
    reasouces if we need a no cheat run."* Written into
    `agent/WORKFLOW.md` as a binding rule: cheat markers are **expected** in a
    playtest log and get attributed, not excused; the reason is asked **once**;
    a cheat is a confound **only** where the reading intersects what it changed,
    and the agent must name the intersection or say there is none; and a leg
    that truly needs a no-cheat run must **declare it in its brief and prep a
    resource-rich save**, never improvise on an existing playtest colony.
    **Nothing is owed by you** — this is recorded so no future sitting spends
    your minutes re-litigating it. Trigger: six `ObjCheat CheatFill` markers in
    the PT-60 sitting log, which cost you an explanation you should not have
    had to give.

### ⭐⭐ NEW 2026-08-11 — from the `corun-pt15` SITTING (two calls, both yours)

**Cost, stated honestly: the brief promised ~45–90 attended minutes and the
sitting took about 3h10m.** The overrun is ours except the march itself — that
was you playing your own colony through the mystery, and prep had already
warned the mystery was far longer than the plan first assumed. Itemised on the
session record: our stop-instruction lost the organic wisp reading (recovered
forced — same trap, same 95 wisps, but no longer "your own click"), a speed
instrument recommended the wrong rung and had to be overridden, the HUD kept
silently dropping the march to 1×, and the cheat disclosure took three asks.
**Your deviations (the extra passenger rocket, activating all three shifts)
are what made C39 readable at all and are not scored against you.**

9. ~~**⚖️ `C39` — the four Workshops lose half their staffing with NO
   offsetting uplift whenever Service Automation passes. Repair or not?**~~
   ✅✅ **DECIDED 2026-08-12 — EXTEND THE COMPENSATION, plus the sibling-label
   sweep your questions surfaced.** Ruled after a full walkthrough: the
   Workshops DO take the cut (measured 12→6) and only miss the payback; the
   dev comment states the assumption they violate; performance feeds only the
   shift-end Comfort payment (consumption scales with staffing fraction and is
   untouched, so balance exposure ≈ nil — the fix restores the exact
   conservation your Diner already gets). ⭐ Your questions also found that
   **sibling automation laws exist for `FactoryBuildings` (confirmed in data)
   and `ResearchBuildings`**, never swept for the same label-vs-class
   mismatch — the build enumerates all three labels and covers every mismatch
   found, not just the four Workshops. The delabel alternative (your
   employment-sink intent theory) was considered and declined in favour of the
   dev comment's stated intent. Queued into the next unattended build chain;
   verification re-runs the same paused bracket on a `CP15PT15` staged copy
   (it holds the measured TV Studio Workshop). → `agent/bugs/C39.md`.
10. ~~**⚖️ `C46` — re-graded 2026-08-12 after your challenge: the phantom-power
    state we measured cannot be reached by normal play.**~~ ✅ **DECIDED
    2026-08-12 — WONTFIX, your ruling in your own words:** *"Lets just write
    that one off since its not a true bug."* Your challenge was what caught
    it: the omission is real in the shipped code, but every path that writes
    the trap's power value only runs in "free" mode and the once-only choice
    means the game can never reach the free→destroy sequence our rig forced —
    so organically there is no phantom. Nothing is built; the defensive
    one-liner was declined with this ruling. `CP15F15.savegame.sav` is no
    longer needed for any open question — keep or delete it as you like.
    → `agent/bugs/C46.md`.

### ⭐⭐ NEW 2026-08-10 — from the `corun-batch-2` SITTING (four calls, all yours)

**Cost, stated honestly: the brief promised 33–36 attended minutes and it took
about 75.** All seven legs ran and nothing was cut. The overrun is ours and it
is itemised — a keybinding the brief invented, three broken readers in one
function, a save witness that stopped witnessing, a leg that had to run twice
because it took no reading before its own save, an uninstall that needed a
restart nobody knew about, and one console line of mine that produced nothing.
**Your three deviations all bought evidence and none is scored against you.**

⭐ **What went right, so the list below reads in proportion:** the popup-audit
keystone is ANSWERED (a storybit popup survives a save/load *and* still applies
its outcome when you answer it afterwards), F21's fix was WITNESSED firing on a
real boarding, PT-47 passed every check it could sample, F99's last untested
cell is filled, and **`PT35FIXTURE.savegame.sav` now exists in your save folder**
— keep it, it unblocks a test that has been stuck since 2026-08-04.

5. **⚖️ `F85` — the defect is real, and the route we told you about doesn't
   exist. What do you want done?** A save **landed 39 seconds inside the open
   breakthrough-choice popup**, and reloading it **voided the choice** — popup
   gone, breakthrough never discovered. So the entry is right that the save
   system doesn't protect you. **But the entry's route is dead:** it said "rebind
   Quick Save to F9", and you established there is no save action in the
   key-bindings screen at all. The entry's own fork only has two outcomes
   ("R2-by-rebind" or "drop to I/R4, documentation") and **neither fits** — the
   defect is real and unreachable by the one route anyone had named.
   **Your call: severity, and whether anything gets built.** ⚠️ The half worth
   your attention now is the **distress-call popup** (audit §3.6) — it's the
   game's one popup that *doesn't* pause, so it's the only place a normal
   autosave could land inside a popup window with no rebind involved. That
   rider didn't run. → `agent/bugs/F85.md`.
   ⚖️ **2026-08-11 — you challenged the "no quicksave on retail" claim and the
   challenge holds: STILL OPEN by your call.** The only *sampled* fact is that
   the bindings screen has no save row. Source (including the generated
   executable) says the one Quick Save action is **Ctrl-F9** and only exists
   when `Platform.cheats` is on — but that's an inference chain, and nobody
   has ever pressed Ctrl-F9 on retail. **The 10-second check rides your PT-20
   redo sitting**: press Ctrl-F9 in a colony — a quicksave landing makes the
   default binding a live route into this defect and changes the whole
   disposition; nothing happening confirms the source read. Decision waits.
   ⭐ **Re-routed 2026-08-11 (your corun-pt15 order): the Ctrl-F9 check now
   rides the PT-15 sitting** — any colony works and it answers sooner. The
   PT-20 redo is unchanged otherwise.
   ⛔⛔ **2026-08-15 — ANSWERING YOUR "quick playtest?" QUESTION: NO, AND THERE
   CANNOT BE ONE.** The distress dialog is the last reachable surface this entry
   had, and today's route check found it is **dead-coded out of the shipped
   game** — its only caller is a button the executable compiles behind
   `local cond = false` (full derivation: item **31** above, and `F85.md`
   §2026-08-15 later). It cannot be reached by playing; the only way to put it
   on a screen is an agent console-call, which would prove the wrapper works and
   say **nothing** about retail play. So a sitting buys no knowledge here, and I
   am not proposing one.
   ⇒ ⭐ **The severity question is now answerable on evidence instead of taste,
   and every route into this entry's harm is closed:**
   * the breakthrough and Assembly popups **pause**, so no autosave can land in
     them;
   * there is **no save action on retail at all** (`idQuickSave` compiled out —
     your check, 08-11);
   * the one non-pausing popup is **dead-coded** (this finding);
   * and our wrapper pauses it anyway if a patch ever brings it back.
   ✅✅ **RULED + CLOSED 2026-08-15 with item 31: LEAVE it at `P3` / LATENT / tier U.**
   ⇒ *Recommendation as it stood:* **LEAVE it at `P3` / LATENT / tier U.**
   The label is now exactly right: the defect is real and reproducible (a save
   *was* landed inside a popup and *did* void the choice), and it is
   unreachable by any player route. Bumping it would overstate; dropping it
   would understate a reproduced fault. **One word from you closes this.**
   ✅ Item **31** is ruled and applied too — the module is removed and shelved,
   and both player-facing pages are corrected. **Nothing is owed on F85.**
   ✅✅ **THE CHECK RAN 2026-08-11 IN THE PT-15 SITTING — Ctrl-F9 IS NOT A
   ROUTE, and you were right to make us press it.** You pressed it; nothing
   happened on all three witnesses (no new save file, no `Game saved:` or
   `Save failed:` line, nothing on your screen). But three absences aren't a
   mechanism, so we took a structural read instead: **the Quick Save action is
   never built on retail.** `Platform.cheats` is falsy, so the block containing
   `idQuickSave` never runs — and `idQuickSave` reads `nil` against **437
   actions, 433 with ids, with the lookup proven working on a known-present
   id**. There is no save-the-game action in the entire set; the only
   `save`-ish entries are map/camera editor tools. ⚠️ Note the save was **not**
   refused — `CanSaveGame()` came back truthy. The action simply isn't there.
   ⇒ **your original challenge is fully vindicated and the observation is
   closed. Only the disposition is still yours** (severity, tier, whether
   anything gets built).
   ⭐ **Prep 2026-08-11 — the check now has three witnesses instead of one, so
   "nothing happened" will be a measurement rather than an impression.** (1) a
   new save file appearing in the save directory, which we list before and
   after; (2) the game's own log line — the quicksave routine prints either
   `Game saved: <name>` or `Save failed: <err>`, so **either line falsifies the
   source read**; (3) your eyes on the quicksave loading screen. Expected file
   name if one lands: `QuickSave.savegame.sav`. **Still your decision either
   way** — the sitting brings evidence, not a verdict.
   ✅✅ **DECIDED 2026-08-12 — BUILD THE `dont_pause` FLIP (your pick, on your
   own proposed fix).** You asked the question that found the better repair:
   the distress-call dialog is the game's ONLY non-pausing popup, and flipping
   it to pause like every other popup closes F85's entire remaining reachable
   surface in one property change (no autosave can land, nothing can queue
   behind it). Built as a chained wrapper, disclosed as a design-judgment
   tweak; queued into the next unattended build chain with its verification
   launch. The bigger per-site rewrite was declined; the distress-call watch
   rider below retires when the fix verifies.
   ✅✅ **BUILT AND VERIFIED 2026-08-15 (`unattended-3`, owner cost zero), and
   the terminal audit sustained it the same day.** The flag was read cleared
   in two real launches (once on a flattened tree after your own 47 MB colony
   copy loaded), an already-pausing popup untouched, a flagless popup left
   alone, the pass idempotent; the suite passed 80/0/16/0 of 96 around it. The
   §3.6 autosave rider is retired on its own condition. The entry carries
   **`tested-unattended`** under your 26b vocabulary — nothing here claims
   anyone watched a clock stop. ⚠️ **The screen-witness add-on this line once
   promised is MOOT by item 31**: the dialog is dead-coded on retail, so a
   screen witness could only be a console-raise that proves the wrapper and
   says nothing about play — item 31 owns the consequences.
   **Still yours here: severity/tier only** (rec on STATE: leave `P3`/latent-U
   — the defect's one reachable half is repaired, the rest was never reachable).
6. ~~**⚖️ Disabling a mod needs a full game restart — does `PT-20` need
   redoing?**~~ ✅ **DECIDED 2026-08-10 — REDO NOW.** A dedicated PT-20 redo
   co-run is queued (your part: the Mod-Manager disable click, a **full game
   restart**, ~10 min of ordinary play; save/reload/log reads are rig-side).
   Its result supersedes the old 98-vs-98 comparison, which may have measured
   the half-disabled middle state. → `agent/bugs/D13.md`, PT-20 section below.
7. ~~**⚖️ Our save-folder cleanup has now failed twice, and we may know
   why.**~~ ✅ **DECIDED 2026-08-11 — KEEP DELETING + VERIFY.** Agent saves
   keep dying in their recording commits; the close-out directory listing
   (now a standing WORKFLOW rule, and it held on the audit's re-check — none
   of the 15 returned) verifies each deletion stuck. The Steam-Cloud
   hypothesis stays parked: if a deleted save ever returns again, that run
   tests it. → WORKFLOW "Co-runs" close-out rule.
   ⭐⭐ **AND ONE RETURNED — 2026-08-11, so the parked hypothesis is now TESTED
   and CONFIRMED. Fourteen of them returned, at the next launch, written before
   the game process even started.** Your decision above was right about the
   listing (it is what caught this) and wrong only in what the listing could
   prove: it establishes that the deletion HAPPENED, never that it held.
   Nothing about the rule changes; a tick of yours removes the cause. See the
   two-ticks block at the top of this file and `agent/facts/EF-051`.
8. ~~**⚖️ There is uncommitted work in the repo that isn't ours, including an
   answer of yours nobody recorded.**~~ ✅ **CLOSED 2026-08-11** — the
   uncommitted work landed in the sitting's commit, and you CONFIRMED the
   typed line as your D07 ruling (item 2 above). Recorded on
   `agent/bugs/D07.md`; nothing further owed.

**⚖️ What the audit changed (2026-08-10, terminal audit of the sitting — every
verdict above SUSTAINED; four corrections to the record, none of which flips a
result):** the "unattributed modal" at ~16:02 **is in the log** — it was the
keystone test's own first storybit, whose popup was answered after a reload
(the sitting's "it's in no log" was wrong; run 1 stays void, run 2 carries the
pass). The mid-sitting instrument recorded as "produced zero output" **did
print** — the game only flushes its log tail at exit, so the check couldn't
see it (that flush behavior is now a recorded fact). The keystone's run-1 gap
was ~15 minutes, not ~8. And prep's wrong "0 defence towers" figure was NOT
inherited from batch-1 — prep re-read it live through the same broken reader.
⭐ One NEW find from reading the whole log: a single vanilla engine error line
during the bombardment window (a rocket departure hitting an invalid station
position) — filed as `C45`, one occurrence, nothing owed from you.

### ⭐ NEW 2026-08-05 — from the `corun-batch-1` sitting (four calls, all yours)

**Cost: the brief promised ~24 attended minutes and the sitting ran about two
hours — but you ruled that this one is not scored against the estimate**, since
the excess was your own deliberate deviation to chase F99 and the dev-cheat
leads (which is where `F101` came from). Recorded as an **owner override** in
the audit. The one piece it does *not* cover is still logged as a real miss:
**M1 was budgeted 3 minutes and took ~25**, because prep's measured fixture had
evaporated and it had to be built live.
→ `agent/prompts/corun-batch-1/03_FABLE_AUDIT.md` §8.

1. ~~**⚖️ Does PT-37's result unblock F48?**~~ ✅ **DECIDED 2026-08-11 — SHIP.**
   The evidence beat the criterion: case A removed a real stale connection
   from your own save lineage and survived reload; case B's assert is
   measured unreachable by meteor. The corrected pass is queued into the next
   unattended chain; PT-35's do-no-harm run covers it in the same launch.
   → `agent/bugs/F48.md`.
2. ~~**⚖️ Should pinning a colonist to a residence also pin them to their
   dome?**~~ ✅ **DECIDED 2026-08-11 — NO DOME PIN**, your 2026-08-10 line
   confirmed as the ruling: *"It should not pin them to the dome, seems like a
   risk for a bunch of weird bug cases."* The module's deliberate split
   stands; no code change. → `agent/bugs/D07.md`.
3. ~~**⚖️ How much do the two new dev-tool defects matter?**~~ ✅ **DECIDED
   2026-08-10 — OUT OF SCOPE, `F101` is `wontfix`. Nothing gets built.** Your
   ruling, in your own words: *"If it works fine from what we can tell in dev
   mode then its not in this mods scope. If a modder wants to build out a
   toolkit for users then that should be something they fix."* ⭐ **What the
   session found before you ruled, because it is the reason the question was
   answerable at all:** neither throw is *possible* on a build where those
   buttons belong — `TestMeteor` is missing precisely because `Platform.cheats`
   is false, and `GetSpotNameColor` precisely because the `DevToolsPublic`
   library is absent — so there is nothing to reproduce in dev mode. On retail
   the button only executed because the engine's own gate passed first
   (`ObjCheat CheatMeteorHit` prints one line ABOVE each throw), and that gate
   is `Platform.cheats or AreModdingToolsActive()` — so a **Ged mod-tool window
   was open**, the same state that blocks achievements. ⛔ **And it was not our
   TestKit forcing it:** the kit enables only the console, which is not part of
   that gate, and neither repo writes the cheat flags at all. Pressing them
   damages nothing (the meteor button throws before it runs anything, under
   `procall`; the spot toggle only leaves its own dev-UI state one click out of
   phase). → `agent/bugs/F101.md`, "The reachability gate".
   **The dev-tools-for-players idea is parked** in
   [FUTURE_IDEAS.md](FUTURE_IDEAS.md) as a SEPARATE post-launch mod — not this
   pack, and not work.
4. ~~**⚖️ `Opt_NoHomeless` self-deactivates at the main menu**~~ ✅ **DECIDED
   2026-08-10 — the F100 hold is LIFTED and the repair is the reason-string
   fix ONLY** (the log line stops crying wolf; the preflight target stays as
   is until D12's own review settles). Queued with the C43 TestKit fix into
   the next unattended chain, which verifies both against a live boot.
   → `agent/bugs/F100.md`.

### ⭐ NEW 2026-08-10 — from `corun-batch-2` prep (nothing needs your call; two are cleanup already done)

**FYI, and it is a gap in our own gate.** Four agent-created staged saves —
`CB1STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`, about **223 MB**, all byte-identical
copies of `TEST2H TRAIN` — were still sitting in your save folder and in your
in-game load list, while `corun-batch-1`'s terminal audit had recorded *"all
staged/throwaway saves gone from the save dir"*. **Deleted this session**, with
`TEST2H TRAIN` re-verified byte-identical (MD5 `103B320A…8958`, mtime unchanged).
⛔ **The cause is structural, not a slip:** the co-run close-out gate runs
`git status` in both repos and **never looks at the save directory at all**, so
a staged copy that outlives its commit is invisible to every check we have. The
next chain's close-out is told to check it; whether that becomes a standing
WORKFLOW rule is worth one line from you if you care.

**Also, two entries had results that never reached them** — C42's and F21's
2026-08-05 readings were on their checklist riders only. Both entries corrected;
the archive cross-check rule you got from batch-1 caught both on its first use.
**And F21's "penalty half unmeasured" turned out to be our reader**: `spent_time`
is not a field on any class in the game, so that `nil` was guaranteed. The real
statistic reads fine — station rolling average **516,309** against its trains'
**47,968–183,186**, which is the shape F21 predicts.

**Not decisions, just so you know where things stand:** D07 is **4-of-5**, not
3-of-5 — trigger A passed on 2026-07-30 with your Forever Young A/B and the
entry had been stale for five days; you caught that from memory during the
sitting. PT-47, M5 and M7 never ran and stay routed. F99 did not fire once in
two hours; the one condition it names is still untested and the recipe for
building it is on the entry.

- **The mod-page relabel package** — ✅ **proposal ADOPTED 2026-08-04 (your
  `--approved`, in your own hand), ⚠️ but NOT closed: the wording is still
  owed by you.** Five shipped fixes (F55 forever-mark, F40 android dust
  sickness, F73(b) shelter reflex, F70 template refill, F97 dust-devil gate)
  are correct repairs whose *bug-ness* is a design judgment; the adopted
  proposal is a short "judgment calls" section in `MOD_DESCRIPTION.md` so they
  aren't presented identically to, say, F23 or F12. **The wording is yours** —
  the item said so, and approval adopts the proposal, not the words.
  `MOD_DESCRIPTION.md` is **FROZEN until launch prep**, so this is now a
  **launch-prep instruction with an owed input**: when the freeze lifts, the
  section goes in with your wording. This line stays until that wording
  exists. → `docs/agent/reports/CHAIN_QA_REPORT.md` §3.
⭐ **CONVENTION (added 2026-08-03, chain-12 QA, from `BUG_LIST_AUDIT.md`
§10.6f(i)): record the SESSION UPTIME next to any error COUNT.** Cross-arm
count comparisons (this leg's 0 vs that leg's 80) depend on comparable
exposure, and the owner's sessions run 1–6 hours — which makes zero-error
results *stronger* than they read, but only if the uptime is on the record.
One line per leg: "session ~Nh".

⭐ **CONVENTION (added 2026-08-04, owner): CO-RUNS — a rider class where the
agent drives and you are on call, not on duty.** For items with heavy setup and
a short measure, or intermittent triggers you'd never catch in hours of
organic play: the agent preps everything unattended (scripts, staged save
copy, a measure-moments list), launches and drives the game, and you attend
ONLY the minutes where eyes or a judgment call are needed. Such riders are
tagged **TAKEABLE IN a co-run**. Protocol and the forced-vs-organic evidence
rule: `docs/agent/WORKFLOW.md` "Co-runs". First candidates: the F11
pre-wrapper watch (below), C41's vanishing picker (amplified spawn/open loop),
F99's no-cheat discriminator (forced break, organic drone repair), plus the
two C-side console reads that need no eyes at all.

⭐ **ROUTING SWEEP 2026-08-04 (post-rig; the block above predates the rig).**
Every open item re-triaged under WORKFLOW's routing rule now that the rig is
proven. ✅ **ADOPTED by the owner same day** — each item's Status line now
carries its mode; ⚠️ each converted test still gets its setup re-derived in
rig terms by the session that runs it — the designs below were written
assuming the owner drove everything.

⚖️ **Execution rule for unattended work (owner, 2026-08-04):** a truly
unattended item runs as a **two-prompt chain — Opus executes, Fable audits**.
Batched unattended work runs as a **full chain: Opus throughout** (top tier
mid-chain only where something is genuinely complicated), **closed by a
terminal Fable audit**. Full form: `agent/WORKFLOW.md` routing triage.

⚠️ **CORRECTED same day, and it upgrades two verdicts:** the sweep first
claimed "no verified command forces a dust storm". **Wrong — table-staleness,
not a source fact.** `CheatDustStorm(storm_type, setting)` exists, ungated,
with `"normal"` / `"great"` / `"electrostatic"` types (`DustStorm.lua:540`),
and a **static-charged dust devil** can be forced outright (both now in the
HELP verified table, `[NEVER RUN]`). So **F90 moves from organic-only to
co-run STAGEABLE**, and PT-27/PT-28 no longer wait sols for a storm.

| verdict | items | what you still do |
|---|---|---|
| → **UNATTENDED** | **PT-35** (all reads are numbers + save/reload — the "nothing changes on screen" check becomes "the read-back numbers don't change", which is the entry's own claim) · **F99 residue rider** (the rig can STAGE break + cheat + pre-reload read deliberately — it no longer waits for a sitting to happen to use the cheat) · **F99 no-cheat discriminator** (forced break, organic drone repair at speed, log watch — no eyes; still gated on your go, it feeds your severity call) · **load-heal sweep** (Do-first #2 — was ~1 h of you; save/reload cycles are the rig's proven core; re-scope first) — ⭐ **all four are now the `unattended-1` chain** (`agent/prompts/unattended-1/`, built 2026-08-04, Opus×2 + Fable audit per your rule), plus the two `[NEVER RUN]` command verifications and a C42 ride-along | kick off the chain |
| → **CO-RUN** (was full playtest) — ⭐ **the front four + ride-alongs are now the `corun-batch-1` chain** (`agent/prompts/corun-batch-1/`, built 2026-08-04: PT-37 · PT-47 · PT-42 · PT-53 E + F21/C42/popup-trio rides + the optional PT-35 fixture build; Opus prep → your ONE sitting, est. 15–25 attended min → Fable audit. Kickoff: Opus on `01_OPUS_PREP.md`; the sitting runs when you sit) | **PT-37** (break staged via the proven `BreakTrackElement` route, reload cycles rig-driven; your eyes: route formation + the salvage-cursor check) · **PT-47** (agent forces the volley + runs the 5 integrity checks; your eyes: scatter-vs-rank, the one thing that is eyes by nature) · **PT-27/PT-28** (provisioning is the real cost; catch-lists and Health-drop patterns are console reads; PT-28 rides PT-27's storm nearly free) · **PT-42** (agent stages stock/drain at speed; your eyes: the faction panel goals at 3–4 moments) · **PT-53 E** (two hands moments — manual assign, Mod-Manager disable; the load-clean read is log) · **PT-18** (agent stages the landings on a SAVE-E copy; deaths/stranding are counters; ⚠️ SAVE-E itself is still ~30 min of your provisioning) · **PT-10** (setup rig-driven; your eyes: clumping + screenshots) · **PT-15** (reads scripted, `SetLightTrapMode` is a verified command; fixture still needs the mystery pick) · **F74+F53(a)** (harness builds the fresh colony unattended; you: the pack-disable click + the two UI acts) · **PT-60** (suite/reload/log halves rig-side; you keep only the 15–20 min ordinary-play segment) · **PT-20** (you keep the disable click + 10 min play) · riders **F21 · F34(d) · F85 · F38 · popup keystone · §3.6** (each a hands-moment or ride-along once staged) | minutes, named per brief |
| **stays PLAYTEST** | **PT-62 remainder** (the campaign gate — behavioural drain judgment through a landing; rig can carry P12's save/disable/load mechanics) · **PT-21** (organic play IS the test) · **PT-30** (mystery playthrough, UI actions) · **C39** (explicitly a keyboard judgment) · **doctrine C-sitting** (likely co-runnable — re-scope against `CHAIN_QA_REPORT.md` §1.3 before promising) | the sitting |
| **stays ORGANIC-ONLY rider** | **F80 · C25 · F06 · F83 · C40 · C32 · F76/C41 recurrence** (situation must arise; the READS are one-line co-run/console asks when it does) · ~~F90~~ (moved to co-run — see the correction above) | tap when it happens |

Two consequences worth knowing: **your dominant remaining cost shifts from
sittings to fixture provisioning** (SAVE-A/D/E builds — cheats are
scriptable but building placement is UI, so those stay co-op sessions); and
since co-runs ARE attended, a co-run pass you witness can earn `tested`
exactly as a sitting does — F11's watch was denied only by a fixture gap,
not by the format.

## Do first — the campaign's ordered top (chain-12 QA, `agent/reports/CHAIN_QA_REPORT.md` §9)

1. **PT-62's remainder** (→ Colonists & domes) — D12's only gate, ⛔ NOT a
   release gate (opt-in; owner, 2026-08-03). ✅ P4/P6 PASSED 2026-08-03 (dome
   23 → 0, overpop cleared); still owed: **P12 · P13 · P14 + the landing
   check** — the PT-62 block is the truth, this line is its summary.
   *(Queue line re-synced 2026-08-11 by a doc sweep — it had frozen the
   pre-08-03 remainder while the block below moved on.)*
2. ✅✅ **The load-heal round-trip sweep — CLOSED 2026-08-12 by your call.**
   Both legs ran and passed (unattended, 2026-08-04: D1 natural-state ×3 loads
   clean, D2 forced-defect heals fire once and hold; details annotated below).
   You ruled D1+D2 close it: everything sampleable passed in both directions,
   the unsampled families (H1 astro — wrong commander; H3 biorobots — none on
   the save; H2/H4 deliberately unforced) stay recorded as unsampled, never
   clean, and return as their own findings if one ever misbehaves organically.
   Nothing further owed.
   *(Original ask, kept for the annotations that follow:)* save, reload twice, read the
   heal numbers (the Astrogeologist +10% class of defect; two-for-two
   defective on the heals actually tested is the project's worst base rate).
   Design: `CHAIN_QA_REPORT.md` §9 item 2.
   ⭐ **HALF DONE UNATTENDED, 2026-08-04, and it cost you nothing** — the
   `unattended-1` chain re-scoped this into two legs and ran the first.
   **Leg D1 (natural state) — RESULT: nothing fired, nothing repeated.** Three
   loads of a staged copy of `TEST2H TRAIN` (load 1 cold, save, reload, reload),
   pack **81/81 active as READ**, **0 `[LUA ERROR]`**, six heal families read
   identically at every load: all three `HEALDIFF VERDICT` lines say **0 of 6
   families changed**, and **not one pack heal line appears anywhere in the log**.
   Log: `docs/archive/u1c1_Mars.exe-20260804-16.46.30.log`.
   ⛔ **What that does and does not buy, because the difference is the whole
   point.** It *does* falsify the F92 shape on this save — the identity-keyed
   heal that turned 1 modifier into 2 after one save+reload would have shown as a
   growing count, and `AutomaticMetalsExtractor` read 2 on all three loads — and
   the F88 shape, the unlatched restart, which would have re-printed every load.
   It does **not** test any heal doing its job: nothing was broken, so nothing
   healed. Two families were **not sampled at all** — H1 astro (the colony runs
   the **rocketscientist** commander, not astrogeologist) and H3 biorobots (0
   biorobots on the save) — and are reported as unsampled, never as clean.
   ⇒ **The remaining hour of your time is not owed:** leg D2 forces the defect
   state and samples the heals firing. Your call is only whether the D2 result
   plus this one closes the item.
   ⭐⭐ **LEG D2 RAN TOO — DONE, and it PASSES. Nothing here is owed to you.**
   Two families were driven from their actual defect state on a staged copy and
   watched through a save/reload/save/reload cycle
   (`docs/archive/u1c6_Mars.exe-20260804-17.24.57.log`):

   | family | forced to | after the healing load | after a further save+reload |
   |---|---|---|---|
   | **H5** `Fix_MeteorFrequency` (F88) | `SMRFixPack_MeteorLatch = false` | one `one-shot heal … (latch false -> 1.0.1)` line, latch `1.0.1` | **no line**, latch `1.0.1` |
   | **H6** `Fix_RainsDeadlock` (C34) | `RainsDisasterThreads = false` | one `RainsDisasterThreads was false — recreated as an empty table` line, `type=table entries=2` | **no line**, `type=table entries=2` |

   All three PASS conditions hold: a heal line for each forced family after the
   healing load, **none** after the idempotence load, and every number back to
   **exactly** the baseline — never above it, which is the F92 compounding shape
   that would have been the failure.
   ⛔ **Ceiling and honest gaps, stated with the result rather than after it.**
   This is **MECHANISM**, not `tested` — it says how these heals behave when they
   fire, not how often a real save needs them. **H1** (Astrogeologist) stayed
   **unsampled**: the colony runs the **rocketscientist** commander, so there was
   nothing to strip. **H2 / H3 / H4** were deliberately not forced — doing so
   means editing colonist traits, dome membership or built objects, a bigger
   mutation than the measurement is worth — so they stand as leg D1 found them.
   ⭐ **A vanilla fact fell out of the forcing:** with `RainsDisasterThreads`
   set to `false`, shipped code threw `attempt to index a boolean value (upvalue
   'old_threads')` at `TerraformingDisasters.lua:411`. The state C34 repairs is
   not merely untidy — vanilla indexes that GameVar with no type check and
   raises. That error is **ours**, inside the probe's marked forcing window, and
   is reported as a consequence of the forcing, not as a new defect.
   ⇒ **Do-first item 2 is complete to its unattended ceiling.** What is left is
   your judgment call on whether that closes it, not an hour of your play.
3. **The doctrine C-sitting** — closes the one INFERRED cell in the "OFF is
   three different things" doctrine, the one the owner said we cannot be wrong
   about. Protocol ready in `CHAIN_QA_REPORT.md` §1.3; the agent builds the
   TEMPORARY probe in-sitting and it dies in the result commit.
4. After those: pick a group and clear it in one sitting. Riders are
   opportunistic — take them when their situation arises; never schedule one.

## The protocol — what a sitting is

A sitting = you at the game + a live agent session reading this file and the
entries. You supply observations **in the moment**; the agent supplies
expectations, forensics and log links. Probe-verified ≠ tested: a pass at the
keyboard is what earns a fix `tested` in `agent/bugs/`.

1. **⛔ PT-00 — the stale-probe sweep, BEFORE the game launches** (hard rule,
   owner, 2026-08-01). The agent runs
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` and reports
   **CLEAN** — zero hits, or every hit declared by this sitting's design. Not
   clean → delete the stale probe (+ its metadata/items lines), commit,
   re-sweep — or the sitting does not test. No result is recorded without it;
   the `PROBE SWEEP:` line goes in every result commit. Full rule:
   `agent/WORKFLOW.md` "Probe hygiene".
2. **Predictions BEFORE the leg.** The agent writes numbered predictions from
   the entry before anything runs — the discipline moved from this document
   into the sitting, and PT-61 is the proof it pays (ten predictions, ten
   readings, two riders closed free). A prediction that misses is the finding.
3. **Console steps come from the agent, one command per line**, drawn from the
   entry and PLAYTEST_HELP's verified command table.
4. **PT-22 — the log review, after EVERY session, together.** Newest
   `Mars.exe-*.log` under `%AppData%\Surviving Mars Relaunched\logs`: any
   `[CommunityFixPack]` error/inactive/deactivation line, any `[LUA ERROR]`
   naming pack code, any engine error you did not see vanilla,
   `SMRFixPack.ListFixes()` reading `active` for every default fix (count per
   `agent/STATE.md`; opt-ins read `inactive` unless you enabled them — and
   Mod Options survive a Mod-Manager disable, so read the list, never assume).
   ⛔ **Every unexplained line is reported verbatim with its age** — "not
   caused by our leg" is an attribution verdict, never a dismissal; every
   pushback so far has turned up a vanilla defect that was not on our list.
   Passive watch, no action: if `WATCHDOG — Meteors thread silent` ever
   appears, report it verbatim (F02).
5. **Recording (the agent, same sitting or next session):** the result goes on
   the `agent/bugs/` entry with the date and the **session uptime next to any
   error count**; a PASS flips status in front matter AND heading tag (INDEX
   is generated — never hand-edit); a FAIL files a finding and flips nothing;
   when a status flip will cite a log's numbers, the log is copied into the
   repo in the same commit (R8) — ⛔ **`.gitignore` line 2 is `*.log`, so a
   plain `git add` DROPS IT SILENTLY and the commit still looks complete; use
   `git add -f docs/archive/logs/<name>.log`** (found the hard way 2026-08-03,
   after one commit shipped claiming logs it had not committed); the completed
   section moves WHOLE to
   `PLAYTEST_ARCHIVE.md` and is **deleted from here with no stub or pointer
   left behind**. `python tools/doccheck.py` before every doc commit.

*(This section recreates the checklist's "Reporting protocol", which turned
out to have been deleted by accident in commit `22d7b36`, 2026-08-02 — the
top-of-file link had been dangling since. The original text, old paths and
all, is in git and in the snapshot.)*

---

# Trains — one sitting clears the group

> ✅ **PT-37 RAN 2026-08-05 (corun-batch-1 sitting, attended) and moved WHOLE
> to `archive/PLAYTEST_ARCHIVE.md`.** Case A PASS (better than a no-op:
> 559→558 connections, persisted through save+reload; you watched a train pass
> through every station); case B UNSAMPLED — the harness refused to run it
> because the walk cannot fail via meteor damage, which contradicts F48's
> blocking premise for its cited scenario. **The F48 ship/hold decision is
> yours — "Decisions waiting on you", item 1.**

### Rider — F80: colonists wait at platforms, or walk past working stations · Status: unrun — take it WHEN the symptom appears; never schedule it
**Bug:** trains sometimes never enumerate a valid destination from a stop —
one origin/destination pair fails inside an otherwise healthy network, so
colonists either queue forever or set off overland and suffocate. The
strongest reported-but-unpinned defect on the list; the mechanism now has an
exact source predicate but the trigger has never been proven.
→ [agent/bugs/F80.md](agent/bugs/F80.md)
**Requirements:** None / any colony where the symptom appears — colonists
queued while trains come and go, or walkers passing a working station.
**Setup:**
1. ⛔ **Tap before mitigating** — adding trains is the known workaround and it
   destroys the evidence. Open the agent session the moment you see either
   symptom.
2. Tell the agent which symptom (waiting vs walking) and the exact
   origin/destination pair that fails.
3. The agent hands the three reads (classify · enumeration tap · both-ends
   reachability test) — all read-only, all on the entry.
**Good to have:** note whether any track segment on the line was under
construction (the rival explanation the agent must exclude).

### Rider — F21: re-earn `tested` for the wait-time fix · Status: unrun — optional · ⭐⭐ **2026-08-10 THE PENALTY HALF IS MEASURED AND THE FIX WAS WITNESSED FIRING** (`corun-batch-2`): one named colonist watched across a real, unforced boarding — `start_wait 239310758 -> 239344642`, **+33,884 ms to the boarding moment**, after 205 polls reading `Waiting`. The 2026-08-05 `spent_time=nil` was our reader, not the game. ⚠️ Still NOT re-earned as `tested` — one boarding is an instance, not a keyboard pass · **mode: co-run ride-along** (routing 2026-08-04) · ⚠️ 2026-08-05 HALF measured: the platform-population read ran live (11 stations / 21 colonists waiting / 8 trains) but the penalty half is UNMEASURED — every train sampled read `spent_time=nil` (4 of 8 sampled), a reader gap, not a verdict; stays `fixed`, not re-earned
**Bug:** the fix (platform waiting no longer billed as travel time) passed
PT-43, but the Tier-2 rewrite replaced the mechanism that pass exercised, so
F21 was honestly downgraded to `fixed`. Two quick reads on any working train
line re-earn the tag; skipping costs nothing — it simply stays `fixed`.
→ [agent/bugs/F21.md](agent/bugs/F21.md)
**Requirements:** None / any colony with a working train line and commuting
colonists.
**Setup:**
1. Let someone wait long at a platform; the agent reads their Comfort log (no
   "travel time" entry from the wait) and the train's *Travel time (rolling
   average)* (excludes the wait).
**Good to have:** a long platform queue — it makes the discrimination obvious.

---

# Drones & hubs

> ⛔ **DRONE PLAYTEST FREEZE (owner decision, 2026-07-31).** No drone
> playtesting of any kind until a final drone plan is in place — half-finished
> tests of superseded designs cost sittings and produce evidence about code
> being replaced. When the rebuild lands, **ONE multi-step drone playtest
> replaces the whole PT-52 family** (one toggle, all or nothing). If a drone
> anomaly shows up organically mid-sitting, capture it on the D06 entry or as a
> new F-number — observing is not playtesting. **NOT frozen:** PT-10 below
> (dome-entrance data, untouched by any dispatch redesign) and F77's own fix
> (shipped, default-on; only its test's packaging was frozen).

### PT-52 — Drone dispatch overhaul · Status: ⚖️ UNFROZEN 2026-08-31 (item 87) — still blocked on the design decision; the test needs its rewrite from the approved plan
**Bug:** tests D06 `Opt_DroneOverhaul`'s v1 design, and that design is being
rebuilt — every result it could produce would be evidence about code that will
not exist. → [D06](agent/bugs/D06.md), [F77](agent/bugs/F77.md),
`docs/agent/reports/DRONE_OVERHAUL_OPTIONS.md`.
**Requirements:** ⛔ BLOCKED — waits on the approved drone plan; do not run any
part of it. ⚠️ For whoever rewrites this test: the old Trigger C rider's
"uninstall shape" conflated the module TOGGLE with a Mod-Manager disable —
the toggle arm is VOID as an uninstall test ("OFF is three different things",
chain-12 QA re-label, in the snapshot); the rewrite must keep the two arms as
separate steps.
**Setup:** none until the rebuild. The B2 stress protocol and the CAN/CANNOT
judging lists are preserved in the archive snapshot — the rebuild's
verification leg is derived from them.

### PT-10 — Open-roof drone observation (F55) · Status: ✅✅ **RUN 2026-08-16, ATTENDED, BY THE OWNER — ❓ OPEN QUESTION CLOSED** · **no longer needs a co-run**
> ⭐⭐ **Answered, and better than the bar.** Owner ran it twice on their own
> colony — once via `CheatOpenAllDomes()`, once by reaching breathable
> atmosphere *organically* (Atmosphere 100% / Temperature 84.09%, Open Domes law
> actually passed). Drones **enter, service and TRANSIT** open domes (they
> pathfind straight through to tasks on the far side), a `dome_required`
> Amphitheater read 9% deterioration / last serviced 17 h, and there is **no
> clustering**. ⇒ The dome-entrance PF-tunnel concern is **disproven**, not just
> un-actionable. ⛔ It did **not** exercise the fix itself (that needs a drone
> that already failed an approach), so F55 was NOT promoted to
> `tested-attended`. Full write-up + the confound argument: [F55](agent/bugs/F55.md).
> ⚖️ Nothing owed from you; the promotion question is yours if you ever want it.
**Bug:** no expected answer — either result is useful data. The forever-cache
half is fixed and probe-verified; whether opening a dome's roof destroys the
dome-entrance attaches carrying the only drone pathfinding tunnels in is engine
entity data Lua cannot read. Drones-enter-normally closes F55; drones-locked-out
is a new engine-data finding. → [F55](agent/bugs/F55.md)
**Requirements:** SAVE-A / one dome with interior buildings needing maintenance
/ a drone hub with drones parked outside.
**Setup:**
1. `CheatOpenAllDomes()` (also maxes terraforming and activates the Open Domes
   policy — the prerequisites).
2. Run 1-2 sols at ultra; the agent records the four observations (entry): do
   drones enter · does interior maintenance pile up · do drones clump at the
   entrance · does `CloseAllDomes(MainCity)` recover it, alone or only after a
   save/load.
**Good to have:** screenshots — the clustering picture is half the evidence.

### Rider — C25: Jumbo Cave waste-rock wedge · Status: ✅ DONE 2026-08-30 — CONFIRMED, promoted to F110
**Result:** ran on a Reddit field save (build 1.0.7.396349, `VINTAGE true`). A
`JumboCaveReinforcementStructure` site with `waste_rocks_underneath = 1`, the last
rock a `WasteRockObstructor` (`Rocks_04`) in 2 drones' `unreachable_buildings`,
`JCRS completed = 0`; permanence witnessed (flag reset on load, rebuilt after
~1-2 min run). **Non-zero-while-stuck → C25 earned its F-row.** → [F110](agent/bugs/F110.md).
Fix decision is item 82 above. (This rider is closed; kept as the record of how
the read was taken.)

### Rider — F77: extender-flap Idle-kick · Status: blocked (frozen with PT-52)
**Bug:** the fix ships default-on and is NOT invalidated — how big is the
fleet Idle-kick with and without it? Its check folds into the consolidated
drone PT when the rebuild lands. → [F77](agent/bugs/F77.md)
**Requirements:** ⛔ BLOCKED with the drone freeze.

---

# Disasters

### PT-27 — Biorobots and Dust Sickness (F40) · Status: unrun · **mode: co-run** (routing 2026-08-04 — `CheatDustStorm` forces the storm, HELP table; catch-lists are console reads)
**Bug:** Dust Sickness infected Biorobots — androids bled Health every storm
until cure tech. Fixed: only organic colonists catch it; a load-time heal
clears already-sick Biorobots. → [F40](agent/bugs/F40.md)
**Requirements:** SAVE-A with the Dust In The Wind rule / Biorobots obtainable
(The Positronic Brain breakthrough — provisioning route on the entry) / a dust
storm.
**Setup:**
1. The agent provisions Biorobots and confirms the trait (entry; if none can be
   produced, record "could not set up" and skip).
2. Note who is a Biorobot; wait through a dust storm with the Dust Sickness
   event active.
3. When it resolves, list who caught it — the agent reads against the entry.
**Good to have:** load a save with already-sick Biorobots — the heal log line
(entry). Run PT-28 in the same storm; same save, same sitting.

### PT-28 — Dust Sickness damage spread (F17) · Status: unrun · **mode: unattended ride-along** (routing 2026-08-04 — pure numeric pattern; rides PT-27's storm sitting)
**Bug:** the per-colonist damage roll was computed then discarded — every
carrier lost a flat 10 Health/sol instead of 5-14. Fixed: the losses spread.
→ [F17](agent/bugs/F17.md)
**Requirements:** SAVE-A (Dust In The Wind) / an active dust storm / several
Dust Sickness carriers (PT-27 gets you there).
**Setup:**
1. Pick 4-5 sick colonists in the same dome; note each one's Health.
2. One sol at ultra speed.
3. Compare the drops — the agent reads the pattern (not exact numbers) against
   the entry.

### Rider — F90: underground breaks during a surface storm · Status: unrun · **mode: co-run, STAGEABLE** (routing correction 2026-08-04 — `CheatDustStorm` is real and ungated, so the storm can be forced on a staged elevator-colony copy; the break DISTRIBUTION stays the organic measured path. An organic storm sighting still counts — take it if one arrives first)
**Bug:** surface dust storms could break cables/pipes on the underground map
through the merged elevator grid. The defect is a victim *distribution*, so
one quiet session proves nothing — the read is zero NEW underground leak
notifications during a surface-only storm, cave-ins excluded.
→ [F90](agent/bugs/F90.md)
**Requirements:** underground unlocked / at least one elevator built / a
surface dust storm running / the merged fragment holding >10 connectors
(agent checks).
**Setup:** while the storm runs and for a while after, watch the underground
map's notifications; the agent excludes cave-ins and reads per the entry
(including the known surface-rate residual that is NOT a miss).

---

# Rockets & landers

### PT-18 — Arrival deaths, including the elevator path (F53) · Status: unrun · **mode: co-run** (routing 2026-08-04 — landings staged, deaths/strandings are counters; ⚠️ SAVE-E provisioning is still yours, ~30 min)
**Bug:** newly arrived colonists could walk toward unreachable domes and
suffocate, and the reworked fix's broken case WAS the elevator path — so that
path is tested deliberately. Fixed = nobody dies on arrival: safe drop spots,
elevator riders keep their assignment, unreachable-dome arrivals wait under
"Confused Colonists" and retry. → [F53](agent/bugs/F53.md)
**Requirements:** SAVE-E / an underground dome with free housing reachable
only via the Elevator / a surface rocket landing pad.
**Setup:**
1. Case A — land colonists on the surface away from any dome; watch where they
   walk and whether anyone dies or goes Abandoned.
2. Case B (the important one) — make the underground dome the only free
   housing (fill/close the surface domes), land a rocket, follow the arrivals:
   to the Elevator, down, and in.
3. Case C — land where the nearest dome by straight line is unwalkable while a
   walkable one exists further away.

### Rider — F74 + F53(a): the never-modded fresh-colony pair · Status: unrun · **mode: co-run** (routing 2026-08-04 — the harness builds the fresh colony; you: the pack-disable click + the two UI acts)
**Bug:** two "is the vanilla harm real at all" observations that need a true
vanilla control — a pack-lineage save cannot serve (persisted thread stacks
carry pack code). F74's half no longer decides anything (two outside witnesses
answer it); it rides only because the colony is already there.
→ [F74](agent/bugs/F74.md), [F53](agent/bugs/F53.md)
**Requirements:** a FRESH ten-minute colony that has NEVER had the pack
installed / pack disabled for the sitting.
**Setup:**
1. Order an RC Transport onto a landed storybit trade rocket — does the
   original harm actually occur?
2. Land a passenger rocket flush against a Universal Depot — do arrivals
   actually strand?

### Rider — F83: is the paid Detailed Scan reachable elsewhere? · Status: unrun
**Bug:** after declining or losing a `ReconCenterDiscoveryAsteroid` popup, is
the paid Detailed Scan reachable anywhere else (planetary view)? Settles the
popup audit's verdict on F83's second site. → [F83](agent/bugs/F83.md)
**Requirements:** a Recon Center holding enough Electronics for the scan / the
asteroid popup declined or lost.

### Rider — C32: the asteroid-abandon label read · Status: unrun
**Bug:** does abandoning an asteroid desync building labels? The row was
rewritten 2026-08-01: you must ABANDON manually (asteroids never expire on
1.0.7) and destroyed buildings must be excluded or the first meteor strike
false-confirms it. Non-zero = the defect; zero still proves nothing.
→ [C32](agent/bugs/C12-C38.md)
**Requirements:** an asteroid mission you are willing to abandon
(`UIAbandonAsteroid`) / the read taken on the map whose buildings you care
about.
**Setup:** after abandoning, the agent hands the corrected membership read
(entry).

### Rider — F34(d): landscape mark over a loading rocket · Status: unrun · **mode: co-run** (routing 2026-08-04 — staging rig-side; your eyes on the yank)
**Bug:** drop a landscape mark over a rocket actively loading drones — is a
mid-"Embark" drone visibly yanked, or does it recover silently? Settles the
reachability audit's verdict. → [F34](agent/bugs/F34.md)
**Requirements:** a rocket mid drone-embark / landscaping unlocked.

---

# Colonists & domes

### PT-62 — D12 "no homeless" remainder · Status: ✅ P4/P6 PASSED 2026-08-03 (dome went 23 → 0, overpop cleared) — P12 · P13 · P14 · the landing check still owed. ⛔ NOT a release gate (opt-in; owner, 2026-08-03)
**Bug:** the module works — same colonist, same moment: vanilla answered
`false nil`, D12 supplied a reachable suitable dome — but the first sitting's
drain fought an inflow (the ping-pong finding), and the three changes built in
response are UNRUN. This remainder is D12's only gate. → [D12](agent/bugs/D12.md)
**Requirements:** a STABLE colony — the drain must not fight an inflow /
restart first (**four** unrun changes as of 2026-08-03) / Mod Manager for the
uninstall half / **a flagged dome with an open service work slot, for P14**.
⛔ **Do NOT use D03 "Closed to new residents" as a fixture control** — the old
plan said to; withdrawn 2026-08-03. It works, and that is the problem: D03 sits
on the SAME two seams D12's guards do, so it would mask the guard under test and
make the loop check trivially 0 for the wrong reason. It also blocks Seniors.
Entry (incl. the same-day correction to an earlier, wrong reason for this).
**Setup:**
1. Restart, then the suite run.
2. The loop check — ⛔ **use the SPLIT counter, not the old one** (entry,
   2026-08-03): the blind version counts cohort delivery, which a flagged dome
   is REQUIRED to keep receiving, so it cannot fail honestly. Only **inbound
   SUBJECTS** is a leak, and it must be 0 and STAY 0 **through a rocket
   landing** — a single at-rest reading does not test the `ChooseDome` half.
3. P4/P6: the drain clears the dome, **run clean — no D03 crutch** (above); a
   dome that refills anyway is a FINDING, not a fixture problem. Mind the
   entry's employed-homeless caveat before reading P6.
4. ⭐ **P14 — the free-work door** (new 2026-08-03): flag a dome that has an
   open work slot and watch whether the slot **FILLS**. ⚠️ **`0 would move` on
   a recruiting dome is the door WORKING, not a miss** — that is the reading
   most likely to be misfiled. If the slot never fills while unemployed
   homeless sit there, the door needs a dwell bound and D12 does not ship as
   built.
5. P13: the repaired `SMROptInPack_Disabled.NoHomeless` lever mid-drain.
   ⛔ **RENAMED 2026-08-12 with the opt-in split** — `Opt_NoHomeless` lives in
   the Community Opt-In Pack now and reads `SMROptInPack_Disabled`. The old
   name is inert there: setting it silently runs the module LIVE, which is the
   exact PT-61 trap this lever was written after.
6. P12: save flag-ON → Mod-Manager disable → load clean.
   (Predictions P1-P13 and the four setup traps: archive snapshot; the re-run
   musts incl. P14: entry.)

### PT-53 — Cohort housing, Trigger E (D07) · Status: partial (A-D passed; E owed) · **mode: co-run** (routing 2026-08-04 — two hands moments: the manual assign, the Mod-Manager disable; the load-clean read is log) · ⚠️ 2026-08-05: E's precedence half ROUTED (fixture unholdable — every slot created was consumed in seconds; a design decision went to you instead, item 2 above); in-dome pass MEASURED at colony scale (76→37); **only the uninstall half below is still runnable as written**; ⭐ **the UNINSTALL half RAN 2026-08-10 (`corun-batch-2` leg T) and is CLEAN** — `pack=0/0 active`, zero engine errors, zero new log lines after a minute of play. ⛔ **But it took two attempts: a Mod-Manager disable does NOT take effect until a full game restart** (first attempt read `pack=81/81` and would have banked a clean log of the pack RUNNING). See decision 6 above and `agent/bugs/D13.md`
**Bug:** Seniors/Children in normal housing move to free cohort slots and are
otherwise left alone — triggers A-D passed live ("it worked wonderfully").
Only E remains: player-order precedence and the uninstall shape.
→ [D07](agent/bugs/D07.md)
**Requirements:** any colony with the module on / a Senior you can manually
assign to a normal residence / Mod Manager for the uninstall half.
**Setup:**
1. Manually assign a Senior to a normal residence (player order) — they must
   STAY. ⚠️ 2026-08-05: build the pin BEFORE any free cohort slot exists —
   pin first, create the motive second (three failed attempts and the 5-sol
   pin timeout are on the entry).
2. Toggle the module off — instantly vanilla (behaviour check).
3. Save with it ON → disable the PACK in the Mod Manager → load: clean, no
   `[LUA ERROR]` naming pack code. (A toggle cannot answer an uninstall
   question — "OFF" is three different things, `agent/facts/`.)

### Rider — C40: Crowded Living capacity read · Status: unrun — take it when the law + a working Ministry of Culture exist
**Bug:** not a defect hunt — the ministry gating is intended. Open: the law's
description says +3 while possibly delivering +6, and losing the ministry may
evict people already housed. Harm unproven and deliberately not guessed.
→ [C40](agent/bugs/C40.md)
**Requirements:** Crowded Living enacted / a Ministry of Culture built and
working.
**Setup:** note a Residence's capacity → stop the ministry (off, or cut power)
→ re-read the same Residence; then watch whether anyone was actually evicted
(entry details, including why shift rotation will not trigger it).

### Rider — C42: does a passage traversal leave a stale passenger behind? · Status: unrun — **TAKEABLE WHEN** any colony has a built Passage that colonists actually walk through · ⭐ mechanism link CLOSED 2026-08-04 · ⚠️ 2026-08-05: a WITHIN-SESSION read finally ran (no save/load since traffic) and was STILL unsampled — 0 unit entries over 4 passages; the gap now needs a **traversal witness** (a colonist seen inside a passage element), not merely generated traffic · ⛔ 2026-08-10: the dedicated witness poller ran (`corun-batch-2` prep) — **90 tries × 1 s at speed 20, `units` empty every sweep** — so THIS save cannot sample it; the TAKEABLE-WHEN condition is now "a colony where passages are demonstrably a colonist route", and no zero from `TEST2H TRAIN` may be quoted against the entry (C42 entry, 2026-08-10)
**Bug:** `PassageBase:TraverseTunnel` ends with a raw `unit.holder = nil`
(`Lua/Passage.lua:1055`), which skips the call that would remove the colonist
from the last passage element's `units` list. If so, demolishing that passage
later teleports uninvolved colonists to it and cancels what they were doing.
⭐ **The untraced link is TRACED and HOLDS (unattended-1 leg F, 2026-08-04;
re-derived independently by the terminal audit):** a passage element IS a
`Holder` (`Building`→`BaseBuilding`→`Holder`) and `LeadIn` really does set
the holder, so the stale-entry mechanism is real as written — refined: **one**
stale entry per traversal (on the last element entered), not N. The rig's
post-load read was `C42STALE 0` over **0 unit entries** — UNSAMPLED, and
nothing establishes `Holder.units` survives a load at all. → [C42](agent/bugs/C42.md)
**Requirements:** a Passage with traffic. Nothing else; no cheats, no save
juggling. ⛔ **The read must be WITHIN-SESSION** — after real traversals and
**before any save or load** (a post-load zero is the F99 mistake shape).
**Setup:** one console line, any time after some colonists have crossed —

```
*r local a=0 for _, c in ipairs(Cities) do for _, p in ipairs(c.labels.Passage or empty_table) do for _, el in ipairs(p.elements or empty_table) do for _, u in ipairs(el.units or empty_table) do if u.holder ~= el then a=a+1 end end end end end ConsolePrint(print_format("C42STALE", a))
```

**The counter can fail:** ⚠️ *(corrected 2026-08-04 by the unattended-1 audit —
this line used to say "`0` refutes the entry outright", and that is wrong: a
`0` counts as a refutation ONLY if the denominator was populated — units
actually inside passage elements when the read runs, within-session.)* A `0`
over a non-zero unit-entry population refutes the entry; a `0` over zero
entries samples nothing. Non-zero confirms the desync and the follow-up is to
demolish that passage and watch whether an unrelated colonist teleports to it.

### Rider — F99: re-read the track residue BEFORE a reload · Status: **unrun — the rig RAN the recipe 2026-08-04 and the rider's own precondition never arose; ⚠️ 2026-08-05 added TWO MORE witnessed attempts (meteor repairs on one track, 201 new-build sites across three tracks with the merge confirmed) and `TrackElement.lua:805` did not fire in either, so the gate still never opened — three attempts, zero throws, rate bounds only; ⭐ 2026-08-10 a FOURTH witnessed zero (`corun-batch-2` leg Q — the 2×2's last empty cell: repair sites on 2 DISTINCT tracks completed together, sites 2→0, residue read `0 0` before any save/load) — the `:805` gate has still never opened** · **mode: unattended, STAGEABLE** (routing 2026-08-04 — the rig stages break + cheat + pre-reload read deliberately; owner-rule chain applies: Opus runs, Fable audits. The old TAKEABLE-WHEN framing — wait for a sitting to happen to use the cheat — is superseded)
⭐ **What the 2026-08-04 attempt (unattended-1 leg B) established:** one staged
break + `CheatCompleteAllConstructions()` produced **zero** `:805` throws, so
the "if `:805` appears" gate below never opened — the rider needs a run in
which the throw actually happens. Gained anyway: `F99RESIDUE 0 0` pre-reload
is the reading a *healthy* completion produces (so the fixup is no longer the
only explanation shape); the `BreakTracks({element})` instrument is confirmed
by execution (`repair_cgs` 0→1); and the counter has a liveness witness. Log:
`docs/archive/u1c3_Mars.exe-20260804-17.06.05.log`; full record on the entry.
**Bug:** the `F99RESIDUE 0 0` reading that made F99 look harmless was taken
**after** a reload, and load runs `SavegameFixups.RebuildBrokenTracksAndConnect`,
which sweeps exactly what the probe was looking for. The null result is
therefore not evidence of no damage. → [F99](agent/bugs/F99.md)
**Requirements:** the cheat, plus at least one outstanding repair group —
`repair_cgs` is only ever populated by meteor strikes and disaster damage, so on
a clean build-out there is nothing for the probe to find and `0 0` is
guaranteed regardless.
**Setup:** run the cheat, and if `TrackElement.lua:805` appears in the log,
**read this before saving or loading anything**:

```
*r local a,b=0,0 for _, c in ipairs(Cities) do for _, t in ipairs(c.labels.TrackBase or empty_table) do if #(t.elements or empty_table) == 0 then a=a+1 end if t.repair_cgs and #t.repair_cgs > 0 and #(t.elements_under_construction or empty_table) == 0 then b=b+1 end end end ConsolePrint(print_format("F99RESIDUE", a, b))
```

**The counter can fail:** a non-zero `b` is a track stuck showing damage and
refusing to be salvaged, and would move F99 off `cand` on the spot. Note the
session uptime next to the count (the 2026-08-03 convention above).

### Rider — C39: Service Automation and the four Workshops · Status: ✅ **RUN 2026-08-11 (corun-pt15 sitting) — ANSWERED**
**Bug:** the law halves staffing by LABEL while its performance compensation
keys on CLASS; the four Workshops sit on the wrong side of that line. The sign
of the harm was genuinely unclear — this was a keyboard observation, not more
reading. → [C39](agent/bugs/C39.md)

⭐⭐ **RESULT: the Workshops are MISSING AN UPLIFT, not taking a penalty.** With
the game **paused** (both readings at the same game instant, so drift cannot
explain it), your TV Studio Workshop and a Diner in the same dome **both** took
the identical −50% staffing cut — and only the Diner was paid back for it:

| | before | law on | after revert |
|---|---|---|---|
| **Workshop** performance | 127 | **131** | 129 |
| **Workshop** workers/shift | 12 | **6** | 12 |
| **Diner** performance | 114 | **268** | 124 |
| **Diner** workers/shift | 2 | **1** | 2 |

The Diner's **114 → 268 → 124** reverses when the law is deactivated, which is
what makes it a measurement rather than a coincidence. Your words, kept in the
record: *"more than double when I reverted it dropped to 124 for the dinner."*
⇒ those four buildings lose ~half their output whenever Service Automation
passes.

⚖️ **YOUR CALL — nothing is built.** The chain's scope fence makes C39 an
observation only; if you want a repair, that is a new decision. Severity is also
open: it needs a late-game Technology policy (SortKey 900, 10th of 11) to be
voted through before it can bite anyone.
⛔ **Honest limit:** only **one** of the four Workshops (`TVStudioWorkshopCCP1`)
existed in the colony. The other three share the same class chain so the same
result is expected — but it is inferred for them, not measured.

---

# Mysteries

> ✅✅ **PT-15 RAN 2026-08-11 (`corun-pt15` attended co-run) and moved WHOLE to
> `archive/PLAYTEST_ARCHIVE.md`, audit-sustained the same day.** F07 is
> **`tested`** — your trap's 95 wisps produced 95 power (43% of the grid, ~47
> Solar Panels' worth; vanilla would have given 0.095), it survived save/reload,
> and your verdict is on the entry verbatim. F15's double-grant half is
> MEASURED gone on the same trapful. Kept saves (NOT strays — do not delete):
> **`CP15PT15.savegame.sav`** and **`CP15F15.savegame.sav`**. The two decisions
> the sitting raised (C39 repair, C46) are in "Decisions waiting on you".

### PT-30 — Finished Mirror Sphere site (F16) · Status: unrun
**Bug:** a finished excavation site kept offering its actions, wasting drone
work on a site that cannot progress. Fixed: the finished site starts nothing;
cancelling still works. → [F16](agent/bugs/F16.md)
**Requirements:** a Mirror Sphere mystery game (new-game pick) / played to a
scanned excavation site with a Drone Hub in range.
**Setup:**
1. Control: while the site is part-way done, confirm its actions can start.
2. Run the excavation to 100% — the sphere launches and detaches.
3. Try each action on the finished site — the agent reads per the entry.
**Good to have:** the settling observation rides along: do drones engage a
dead request when an action is clicked?

### Rider — F06: Mystery 10 epilogue arrival · Status: unrun
**Bug:** reach the finale and ignore the corner notification for one sol at
speed — does the Epilogue really arrive minimized and unpaused? Settles the
reachability audit's verdict. → [F06](agent/bugs/F06.md)
**Requirements:** a colony at the Mystery 10 finale.

---

# Any-save & factions

### PT-35 — Save sanitizer does no harm (F35, F03) · Status: **case A COMPLETE 2026-08-11 (mechanism grade — not `tested`); B/C parked** *(status token corrected by the unattended-2 audit; it still read "unrun" beside the completion record below)* — ⭐ case A RAN unattended 2026-08-04: do-no-harm half PASSES, turbine half UNSAMPLED (fixture gap, see below) · ✅✅ **THE FIXTURE GAP IS CLOSED 2026-08-10** — `PT35FIXTURE.savegame.sav` is in your save folder (`corun-batch-2` leg S): FrictionlessComposites researched, **one Large Wind Turbine**, **one applied building upgrade** (Remote Medic on a Hospital, for the F03 half). **The turbine-half re-run is now an unblocked 2-prompt unattended chain** — nothing of yours needed. ⛔ Do not delete that save · **mode: UNATTENDED** (routing 2026-08-04 — all reads numeric + save/reload; owner-rule chain: Opus runs, Fable audits) · ✅✅ **CASE A IS COMPLETE 2026-08-11 (`unattended-2`, re-run after the pack was re-enabled): BOTH halves sampled on a real population for the first time. Three loads, two save+reload round trips, six pass calls, and **0 of 14 readings changed at every single comparison including start-to-finish**. `RepairTurbineBuff`'s zero is no longer the trivially-forced early return — the tech IS researched, so the pass walked its whole body and its already-buffed guard did the skipping; `RepairLeakedUpgradeModifiers` returned 0 with **3 live upgrade-shaped modifier ids and 144 upgraded buildings** in front of it. 0 `[LUA ERROR]` in the whole log. ⛔ Still not `tested` — unattended ceiling is MECHANISM — and cases B/C stay parked.** → `agent/bugs/F35.md`, log `archive/u2run3_Mars.exe-20260811-02.01.06.log`
**Bug:** the pack's two sanitizer passes run automatically on every load for
every player, and the F03 pass REMOVES label modifiers from persisted colony
state — this is the do-no-harm check on auto-running save-writing code, and
the only part of PT-35 that was ever about risk. Cases B and C are PARKED
(`FUTURE_IDEAS.md` entry 4). Both passes are probe-covered; this is cheap
insurance, not substitute coverage. → [F35](agent/bugs/F35.md),
[F03](agent/bugs/F03.md)
**Requirements:** None / any healthy save with a Large Wind Turbine and an
upgraded Medical Center in a dome / ~5 minutes.
**Setup:**
1. Note the turbine's Power production and the dome's birth-comfort figure.
2. Run both console calls — `SMRFixPack.Sanitizer.RepairTurbineBuff()` and
   `SMRFixPack.Sanitizer.RepairLeakedUpgradeModifiers()` — both must return
   **0** and nothing on screen may change.
3. Save, reload, check again. A bonus that GREW on the second run is the FAIL
   (the pass is not idempotent — record the exact figures).

⭐ **RAN UNATTENDED 2026-08-04 (unattended-1 leg A) — case A's do-no-harm half
PASSES; half of it is UNSAMPLED. Status stays `unrun`; this is not a `tested`
grant and cannot be (unattended ceiling is MECHANISM).**

**Run conditions.** Retail `Mars.exe` **1.0.7.396349**, cold load of a staged
COPY (`U1STAGE.savegame.sav`) of `TEST2H TRAIN`, pack **81/81 active as READ**,
speed 3, 2 loads, **0 `[LUA ERROR]` lines in the window**. FORCED: nothing but
the two calls themselves. ORGANIC: nothing. Raw lines:
`docs/archive/u1c2_Mars.exe-20260804-17.03.10.log`.

| step | reading |
|---|---|
| both calls, load 1 | `RepairTurbineBuff ok=true returned=0` · `RepairLeakedUpgradeModifiers ok=true returned=0` |
| numbers before → after, load 1 | `0 of 7 readings changed` |
| save → reload, numbers across the round trip | `0 of 7 readings changed` |
| both calls again, load 2 | both `returned=0` |
| numbers before → after, load 2 | `0 of 7 readings changed` |
| start → finish | `0 of 7 readings changed` |

⇒ **Nothing grew, nothing changed, both passes returned 0 twice.** That is
step 2's "nothing on screen may change" and step 3's FAIL condition, in the
numbers the entry's own claim is about.

⛔ **What is NOT sampled, stated before anyone quotes the PASS.** The fixture
this test asks for is **not on this save**: `FrictionlessComposites
researched=false`, **0 Large Wind Turbines**, **0 Medical Centers** (13 domes,
47 dome label modifiers).

- **`RepairTurbineBuff`'s 0 is trivially forced and samples nothing.** It
  early-returns at `Code/90_SaveSanitizer.lua:58` —
  `if not colony:IsTechResearched("FrictionlessComposites") then return 0 end` —
  so the pass never reached its body. **UNSAMPLED, not a do-no-harm result.**
  Re-running this half needs a save with that tech researched.
- **`RepairLeakedUpgradeModifiers`'s 0 is real but partial.** It ran its full
  body over the colony, every city and all 13 domes — 175 label-modifier
  entries — and removed none. So *"it does not strip live state"* is sampled on
  a real population. *"It clears leaks"* is not: whether the save held any id of
  the form `<handle>_upgrade<N>_mod_<M>` at all was not measured.

**What it would take to close case A properly:** the same leg on a save with
Frictionless Composites researched and at least one upgraded building — which is
a fixture request, not a sitting. ⇒ routed as a gap by unattended-1 prompt 2.
⚠️ 2026-08-05: the corun-batch-1 sitting re-read the fixture on every load —
still `FrictionlessComposites researched=false`, 0 Large Wind Turbines — and
the sitting ended before its optional leg-5 fixture build was reached. The
fixture request stands; no FIXTURE save exists.

### PT-42 — Last Transmission notices your reserves (F22, F75) · Status: unrun · **mode: co-run** (routing 2026-08-04 — stock/drain staged at speed; your eyes: the faction panel goals at 3–4 moments) · ⚠️ 2026-08-05 SKIP re-confirmed LIVE, not on prep's word: Last Transmission read `active=false` on the staged `TEST2H TRAIN` copy — 5 active factions, none it, 0 legislature seats — so the fixture requirement below is real and still unmet
**Bug:** the faction's stored-resource goals never cleared no matter how much
you banked, the Oxygen goal was satisfied by Power, and the penalties became
unreachable once a second map was loaded. Probes prove the reserve maths; only
play shows the approval actually moving and the UI goal clearing.
→ [F22](agent/bugs/F22.md), [F75](agent/bugs/F75.md)
**Requirements:** a game with Last Transmission as an active faction (ideally
with the Underground map opened — that is what made the old maths hopeless) /
storage you can build up and then drain.
**Setup:**
1. Open the faction panel; note approval and the listed "How to achieve"
   goals.
2. Stock Power past 2 sols' worth, let a day pass — the Power goal stops being
   listed and approval rises (reason in the approval breakdown).
3. Repeat for Water, then Oxygen — the important one: only Oxygen clears it.
4. Drain one to zero — the matching "No X stored" penalty appears and approval
   falls.
5. The agent checks the two log lines (entries).
**Good to have:** F22's settling observation rides along — where is the
corrupted number player-visible in a young politics colony, before the Martian
Assembly stage?

---

# Cross-cutting — once per era of the pack

### ~~PT-60 — The chain-8b batch leg (F90-F96 + eight conversions)~~ ✅ **RUN 2026-08-12 (`corun-pt60` co-run) — all nine predictions resolved, audit sustained.** Moved WHOLE to `archive/PLAYTEST_ARCHIVE.md` (results banner + the pre-run spec + this tracker). Highlights: the P8 decider taken on your `USA Sol 302` copy (heal fired once, zero on reload, effect persisted); suite 77/0/10/0 with every SKIP matched by name; 0 errors in the whole log; F48 repaired 3 of 7 tracks in your campaign and the repair stuck; F34(d) re-derived on your challenges and observed reachable 20/20. Your original save byte-verified untouched. Decisions that came out of it: items 12 and 13 above.

### PT-21 — Long-save soak · Status: unrun
**Bug:** the whole-pack background check — nothing drifts, leaks or degrades
over a real session of ordinary play.
**Requirements:** any healthy colony / all default fixes `active`
(`ListFixes`) / 45-60 minutes of real play, no cheats.
**Setup:**
1. Just play — mixed speeds, at least one save/reload midway; note anything
   that feels off (stuck colonists, drone clusters, flickering notifications,
   unexplained deaths).
2. At the end, the agent runs the three state reports (reservations, trains,
   broken track — Test Kit, PLAYTEST_HELP).
3. Log review per the protocol.

### PT-20 — Uninstall safety · Status: ✅✅ **REDO RAN CLEAN 2026-08-14 in state 3 — this per-era re-check is DONE for this era** · standing (re-run per era and before release) · **mode: co-run**
✅✅ **THE REDO (your decision 6, 2026-08-10) IS PAID.** Combined sitting moment A,
log `archive/cs_a1_Mars.exe-20260814-11.57.50.log`. Both packs Mod-Manager-disabled
**with a full process restart**, so this is state (3) and not the mixed state (2)
the old reading may have sampled.
* **The gate, beside every reading:** `pack=0/0 | opt-in=0/0 | save-rescue=0/0`,
  all three registries ABSENT, and `MODORDER :: 1 mod(s) loaded ::
  1:SMR_CommunityFixPackTestKit` — the kit alone.
* **All 8 pack-naming lines accounted:** three mod-**def** loads (the def loads in
  state 3, the code does not) · `Loaded mod items for: …TestKit` · the save's own
  recorded mod list · one `Unpersist missing permanent: Mod/SMR_CommunityFixPack`
  · two *"…which is present, but not loaded"*. ⚠️ The `Unpersist` line is **not
  diagnostic** — it fires in state (2) with the pack fully live; it is only
  readable next to the `pack=0/0` gate.
* **~21 minutes of the owner's ordinary play** (building, trains, workers —
  *"everything seems normal"*), then a save as `PT20REDO` and a reload, which
  printed its own gate line.
* ⭐ **Verdict: 0 `[LUA ERROR]`, 0 `[ERROR]`** in the flushed file (absence read
  only from the archived file, `EF-047`). F99 `:805` and C45 `Quantum Comet`
  watches zero.
* **The leg's own point held:** the save still carried its leftovers throughout —
  `reserved_at ×1260`, `payload_set ×4`, `closed_to_new_residents ×4`, both Drone
  dial modifiers, the F48 latch — *and it behaved normally anyway.*
* ⛔ **Recorded as SUPERSEDING the 98-vs-98, not confirming it.** That was an error
  **count** comparison from the F86 era and F86 is repaired (PT-58 measured the
  same shape at zero); a clean state-3 run replaces it, it does not reproduce it.
* ⚠️ **One deliberate deviation from the setup below:** *both* packs were disabled,
  not the fix pack only. The host save was written with both, so disabling both is
  the true "the player uninstalled our mods" configuration — and it is what the
  D13 after-sweep in the same window required. ⛔ **Save Rescue was pulled for this
  leg**: left installed it would have stripped the residue two seconds into the
  load and the leg would have sampled nothing.
Earlier framing: ⛔ **2026-08-10: a Mod-Manager disable does NOT take effect until a FULL game restart** (D13, measured) — the prior 98-vs-98 comparison may have sampled the mixed state · redo ordered by your decision 6, 2026-08-10
**Bug:** the pack must never hold a save hostage. Steps 1-4 passed 2026-07-31;
step 5's hunt found F86 (both sites since repaired — PT-58 measured the same
shape at ZERO errors against leg 5's 80). This is the per-era re-check, not an
open debt. → [F86](agent/bugs/F86.md), `agent/FIX_POLICY.md` §3.
**Requirements:** any current save with the pack on / Mod Manager / ~20
minutes.
**Setup:**
1. Play a few sols, save.
2. Quit → disable the Relaunched Fix Pack ONLY in the Mod Manager (Test Kit
   stays) → restart, load.
3. 10 minutes of ordinary play, one save/reload — the save must behave
   normally (the original bugs coming back is expected and fine).
4. Log: zero errors naming pack code. The agent pulls the full step-5 hunt and
   the 2026-07-31 method corrections from the archive snapshot before running.

### Rider — §3.6 corner (optional): the sol-change autosave under a popup · Status: unrun — was M3 in `corun-batch-2` (2026-08-10) and was NOT reached (no sol boundary came near); ⭐ **now the interesting popup half**: F85's route refutation makes this the one popup that does NOT pause, i.e. the only place a vanilla autosave can reach a save under a popup with no rebind involved (F85 entry, 2026-08-10) · **mode: co-run ride-along** (routing 2026-08-04)
**Bug:** with the distress-call popup left open, does the sol-change autosave
fire under it? → `POPUP_CONSEQUENCE_AUDIT.md` §3.6.
**Requirements:** any save approaching a sol change.

### Rider — F38: tunnel-ruin routing (vanilla read) · Status: unrun · **mode: co-run** (routing 2026-08-04 — the pack-disable click is hands; the rest stages)
**Bug:** destroy a tunnel, save/load IN VANILLA, order a colonist or rover
across — does the route still use the ruin? → [F38](agent/bugs/F38.md)
**Requirements:** a vanilla control (pack disabled is fine for this read) / a
destroyed tunnel.

### Rider — F76/C41: depot-picker recurrence · Status: unrun — ONLY if a depot click-load misbehaves again; do NOT go looking
**Bug:** the picker is vanilla and was measured CORRECT — it opens ABOVE the
cursor by its own height, which is intended; do not report that as
displacement. If a Load click ever misbehaves, capture with the two read-only
hooks BEFORE touching anything — and if the symptom is *no picker at all*,
that is the different, never-reproduced C41 witness: say so explicitly.
→ [F76](agent/bugs/F76.md), [C41](agent/bugs/C41.md)
**Requirements:** the symptom recurring — an RC Transport/Dozer depot or heap
Load click that misfires.
**Setup:** the agent hands the two hooks (entry) and records the desktop box /
multi-display geometry alongside.
**Good to have:** the known-good workaround while capturing (verified command):
`rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`.
