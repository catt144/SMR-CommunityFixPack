# Public-facing docs checkup — accuracy, completeness, readability, flow

**Owner ask, 2026-08-16:** *"just a checkup of our public facing docs to see if
we forgot to update anything, make sure our wording is accurate. Review it for
readability and if everything makes sense and flows together well."*

♻️ **SELF-CONSUMING.** You finish by fixing what you find (or routing what is not
yours), committing, and **deleting this file in the same commit**, with the
close-out naming its grave (`git show <sha>:docs/agent/prompts/PUBLIC_DOCS_CHECKUP_fable.md`).
The file's absence is the done-condition.

⛔⛔ **THIS IS A PRE-UPLOAD SWEEP AND IT IS THE LAST THING BETWEEN THESE PAGES
AND REAL PLAYERS.** Step ④ (upload) is one owner action away. Everything here
either ships as written or gets fixed now.

---

## 0 · Staleness check, before anything else

```
git log --oneline -10
git pull
```

Also `git -C C:\Dev\SMR-CommunityMods log --oneline -5` — **the site is a
separate repo** and moves independently.

## 1 · 🗒 Live todo list from your first action

One item per surface below, updated the moment each moves. The owner reads that
list to decide whether to step in.

## 2 · The surfaces — all of them, named

**Player-facing, will be read by strangers:**

| surface | path |
|---|---|
| site — landing | `C:\Dev\SMR-CommunityMods\content\index.md` |
| site — installing | `…\content\install.md` |
| site — fix list | `…\content\fix-list.md` |
| site — FAQ | `…\content\faq.md` |
| site — for modders | `…\content\for-modders.md` |
| site — nav/config | `…\mkdocs.yml`, `…\README.md` |
| store card — fix pack | `docs/agent/reports/RELEASE_DESCRIPTION_FIXPACK.md` |
| store card — opt-in | `docs/agent/reports/RELEASE_DESCRIPTION_OPTIN.md` |
| store card — rescue | `docs/agent/reports/RELEASE_DESCRIPTION_RESCUE.md` |
| in-mod description ×3 | `metadata.lua` in `SMR-BugFixPack`, `SMR-OptInPack`, `SMR-CommunitySaveRescue` |

**Supporting records that must stay in step:**
`STORE_FIXPACK.md` · `STORE_OPTIN.md` · `STORE_METADATA_STRINGS.md` ·
`RELEASE_PORTAL_PREP.md` (the ④ sheet) · `RELEASE_UNINSTALL_ASSEMBLY.md` ·
`SITE_BUILD_AUDIT.md` · `STORE_BUILD_AUDIT.md`

⛔ **`docs/archive/MOD_DESCRIPTION.md` IS FROZEN AND IS NOT YOUR JOB.** It holds
**≥6 known-false claims** on purpose — including bullets promising DELETED fixes
(`F24`/`F28`) and an inverted sensor-tower causation. It is a historical record,
rebuilt at prep, **never corrected in place.** Do not touch it. Do not cite it.

## 3 · ⭐ Three seed findings — proof the sweep is needed, NOT the whole job

Found in ten minutes while writing this brief. **Treat them as a demonstration
that the surfaces have drifted, then go and find the rest yourself.**

1. ⛔ **`content/faq.md:174` says "Six fixes are judgment calls."** The number is
   **FIVE** — and **`faq.md:189`, fifteen lines further down in the same file,
   says "Five" and lists them.** The fix list carries five. This is F85's
   removal sweep (six → five, 2026-08-15) missing one instance, and the page now
   contradicts itself where a player can see it.
2. ⛔ **"suite of 95 checks"** — `RELEASE_DESCRIPTION_FIXPACK.md:148` **and**
   `STORE_FIXPACK.md:77`. The measured suite is **96** (`80/0/16/0 of 96`,
   `archive/c47suite4_*`, 2026-08-15). 95 was a *prediction* made when F85 was
   removed; the real re-measurement came back 96 because the `C47` wave-11 probe
   landed. `STORE_FIXPACK.md:273` even records an earlier correction of the same
   number — so this claim has now been wrong twice.
3. ⚠️ **Both cards and the site were swept for F85's removal on 2026-08-15** —
   judgment calls, suite count, module count, packaging counts, portal character
   counts, site coverage and entry counts all moved at once. **Finding #1 proves
   at least one instance survived the sweep.** Assume others did. The counts that
   moved are listed in `STATE.md`'s item-31 block; check every one on every
   surface, not just the ones named there.

## 4 · The job — four passes, in this order

### Pass A — accuracy of every checkable claim
- **Every count** re-derived from `python tools/doccheck.py --emit-counts` or a
  measured log, **never hand-typed and never inherited from another doc.**
  Current: 76 `Code/*.lua`, **75 registered modules**, **96 probes**,
  103 F + 12 D + **52 C** rows. Suite `80/0/16/0 of 96`, gates `75/75` + `8/8`.
- **Every behavioural claim** traced to an entry. A card that describes a fix we
  removed, or promises behaviour a module does not have, is the `F24`/`F28` class
  of failure and it has happened here before.
- ⚠️ **Achievements wording.** Mods block achievements on exactly
  playstation / xbox / **windows_store** (`Achievement.lua:61-63`). Say **"Steam
  and other PC versions"**, ⛔ never bare "PC" — a line said the wrong thing until
  2026-08-16. `STATE.md` claims the public pages are already correct: **verify
  it, do not inherit it.**
- ⚠️ **The item-29 strike.** The claim that a player *"will see a notice"* about
  missing mods was STRUCK from both cards, the rescue card, the assembly, the
  site FAQ and the source records on 2026-08-14 — because `GetMissingMods` skips
  `optional_mod` mods and no retail screen event exists. **Confirm it stayed
  struck everywhere.**
- ⛔ **Load order must NOT appear as player advice.** Owner ruling 2026-08-16:
  *"lets note this and see if it ends up being a problem before we create new
  problems"* — ⛔ no player instruction, ⛔ no for-modders edit. If any public
  page has grown load-order guidance, **that is a violation and it comes out.**

### Pass B — what did we forget to update?
Walk everything that changed since these pages were last audited and ask whether
a public surface should have moved with it:
- **F85 removed and shelved** (08-15) — the counts sweep above.
- **The suite re-measured at 96** (08-15).
- **`C47`/`C48` handed to the opt-in repo** (08-16) — ⛔ no public surface may
  imply this pack fixes seed logistics or drone routing.
- **`C49`–`C52` filed by the coverage sweep** (08-16) — ⛔ **nothing shipped**, so
  ⛔ **nothing public should change.** Verify nothing did.
- ⭐ **One thing genuinely new and operational** — `C52` established that the mod
  browser's thumbnail cache is keyed on mod id + version with no revalidation
  (`ParadoxMods.lua:221-225`). ⇒ **if a preview image is ever replaced after
  publication without a version bump, existing players keep the old one
  permanently.** That is not player-facing text — it belongs as a note on the ④
  sheet (`RELEASE_PORTAL_PREP.md`), where the owner will actually be standing
  when it matters. Add it there.

### Pass C — readability and flow (the owner asked for this explicitly)
Read the five site pages **as a player who arrived from a Paradox Mods link and
knows nothing**:
- Does the landing page orient them in ten seconds — what is this, is it safe,
  what do I do next?
- Do the five pages read as **one voice**, or five sittings stitched together?
- Does the FAQ answer what a real player would actually ask, in the order they
  would ask it — or the order we happened to write it?
- Is the fix list navigable at its size, or a wall? Can someone find *their* bug?
- Are there dead internal links, orphan pages, or nav entries pointing nowhere?
  (`mkdocs --strict` catches some of this; your eyes catch the rest.)
- Do the three store cards and the site tell the **same story in the same voice**,
  or do they contradict each other in tone?
- ⚠️ **Flag redundancy AND gaps.** Six near-identical paragraphs across three
  cards is a maintenance trap; a question no page answers is worse.

⚠️ **Readability is a judgement.** Say so, keep the changes conservative, and
⛔ **never trade an accurate sentence for a smoother one.**

### Pass D — cross-surface consistency
- **STORE ↔ RELEASE verbatim.** The cards were diff-proven byte-identical to
  their audited sources. **Re-prove it with an actual diff** after any edit —
  this pairing has been broken by a well-meaning edit before.
- `metadata.lua` description strings vs the cards vs the site.
- Character counts on the ④ sheet vs what the fields actually hold.
- ⭐ **"You can X" needs a route check.** For every instruction telling a player
  to do something, verify a real user **on each platform** can walk those exact
  steps. A citation proving the mechanism exists is a *different* check — the
  owner overturned a line three reviews had passed on exactly this.

## 5 · Scope fence

**IN:** the surfaces in §2; corrections to them; the ④-sheet note; readability
edits that do not cost accuracy; routing anything that needs an owner call.

**OUT:** ⛔ `archive/MOD_DESCRIPTION.md` (frozen) · ⛔ any `Code/` change · ⛔ any
new fix, entry or engine fact unless you trip over a real defect (then file it
properly) · ⛔ the four `smrcf-*` / `jumbo-cave` chains — those are queued work,
not yours · ⛔ publishing anything to the web (Pages is OFF, `workflow_dispatch`
only, and it stays that way).

## 6 · Stop conditions

- A claim is wrong and you cannot determine the true value → **do not guess.**
  Mark it, route it to the checklist, keep going.
- A fix would change what the mod promises rather than how it is described →
  **STOP.** That is an owner decision, not a copy edit.
- `mkdocs --strict` or `doccheck` goes red → fix before committing; red blocks.
- You find a real defect in shipped code → file it as an entry, do not fix it
  here.

## 7 · ⛔ What may not be claimed

- ⛔ **"The public docs are accurate"** on the strength of a read-through. Say
  what you *checked*, how, and what you did not reach.
- ⛔ **Any count you did not emit or measure.** Inheriting a number from another
  doc is how "95 checks" survived two corrections.
- ⛔ **"STORE ↔ RELEASE still verbatim"** without an actual diff in this session.
- ⛔ **"Reads well"** as though it were a finding. It is a judgement — label it,
  and name the alternative you rejected.
- ⛔ **A player-route claim** without walking the steps for each platform.
- ⛔ Blanket verification over a table — provenance per row, and the ROUTE
  sentence tagged separately from its citations (`WORKFLOW` R3).

## 8 · Close-out — how this file disappears

One commit: corrections applied across every surface · the ④-sheet note added ·
anything owner-shaped on `docs/PLAYTEST_CHECKLIST.md` → *"Decisions waiting on
you"* (R10 — an ask recorded only in an agent doc **is not asked**) · the site's
own repo committed **and pushed separately** (it is not this repo) ·
`python tools/doccheck.py` GREEN · `mkdocs --strict` GREEN if the site moved ·
`STATE.md` extended, not grown (60-line cap; evict resolved material to
`archive/SESSION_LOG.md`, never an obligation) · `git rm` this file · commit
naming the grave · push.

**End with a plain-language owner report**: what was wrong, what you fixed, what
you left and why, and — in one sentence — **whether these pages are ready to
upload.** That last sentence is what the owner is actually buying.
