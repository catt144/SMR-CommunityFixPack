# Chain prompt 2 — the terminal audit: read the release surfaces as the owner will use them, empty the folder

**Read `README.md` first — binding chain rules apply.** Staleness check across
all four repos, live todo list updated per item. This is the **last** prompt in
the chain: folder emptiness is your done-condition (rule 2).

## The job

* **Job 1 — the control, house question, firewalled.** ⛔ Run **"which shipped
  module delivers this?"** over every sentence prompt 1 wrote that is not
  verbatim audited card text — before reading prompt 1's own reasoning about
  those sentences. This chain's two predecessors were each wrong in exactly
  this way and each control found it; the streak is the argument.
* **Job 2 — read every deliverable the way it will be used**: the owner at the
  launch sitting, pasting under time pressure. Does the portal-prep sheet
  actually sequence the links right; does a hole look like a hole or like
  finished text; does anything assume a page is live before its step says so.
* **Job 3 — the two hedges, still hedged.** Verify at source that the console
  question and the toggle-flip remain open (or have since been settled — check,
  don't assume in either direction), and that no assembled text upgraded them.
* **Job 4 — route ④ to the owner and close.** The launch checklist goes to
  `PLAYTEST_CHECKLIST.md` "Decisions waiting on you" as the ④ kickoff; anything
  unresolved is routed, never absorbed. Delete this file AND `README.md` in the
  closing commit; the folder is empty when you are done. Update STATE's ③ line
  to ✅ and point NEXT at ④ (owner) — keep STATE at its checked line count.

## ⛔ What you may not do

- Publish anything, enable Pages, create an account, or paste to a portal.
- Upgrade any claim past the frozen evidence bar by word choice.
- Edit the site's pages in passing — a defect found there is FILED.
- Resolve an un-adjudicated finding just to leave a tidy note.

---

# Notes from upstream

**Written 2026-08-14 by `01_BUILD_DESCRIPTIONS.md` as its last act.** Staleness
check ran first: all four repos clean and `Already up to date`.

## DONE, by file

| file | state |
|---|---|
| `agent/reports/RELEASE_DESCRIPTION_FIXPACK.md` | ✅ complete. Player text **VERBATIM** from `STORE_FIXPACK.md` — proven by diff, the only differences are the card's three `⛔ HOLE` notations removed. 4 fill-in markers |
| `agent/reports/RELEASE_DESCRIPTION_OPTIN.md` | ✅ complete. Player text **VERBATIM** from `STORE_OPTIN.md`, same diff proof. 3 fill-in markers |
| `agent/reports/RELEASE_DESCRIPTION_RESCUE.md` | ✅ complete, ⛔ **publish-gated on checklist 17**. Assembly-only; ⚠️ **all of it is non-card text** |
| `agent/reports/RELEASE_UNINSTALL_ASSEMBLY.md` | ✅ complete — Job 2 |
| `agent/reports/RELEASE_PORTAL_PREP.md` | ✅ complete — Job 3, the ④ sheet |
| `D13_EXPOSED_SET.md` §10.5 | ✅ correction block + the authoritative built text |
| `agent/bugs/D13.md` | ✅ resolution recorded under the gap section |
| `docs/PLAYTEST_CHECKLIST.md` | ✅ **item 28 added**; the "open decisions stay at 3" note amended to 4 |
| `metadata.lua` ×3 | ✅ 2 string defects fixed + item 23's `ignore_files` patterns |
| `docs/agent/STATE.md` | ✅ ③ line updated, still 60/60 lines |

## NOT started — yours

* **Everything in `02_AUDIT.md`'s own four jobs.** Nothing was pre-run.
* ⛔ **The ④ launch checklist has NOT been routed to the owner** — that is your
  Job 4. What exists is the *sheet* (`RELEASE_PORTAL_PREP.md`); the checklist
  entry that points the owner at it is yours to write. **Three owner-facing
  items must reach `PLAYTEST_CHECKLIST.md` and currently live only in that
  sheet**: the preview-art blocker, the opt-in version number, and the
  cleanliness-sentence fork. (A short pointer to the first two was added under
  item 28 as insurance — expand it, do not duplicate it.)

## ⭐ Job 0 — the §10.5 gap: RESOLVED, and it was four gaps

Both sides re-derived at their sources (`D13_EXPOSED_SET.md` §10.5 vs
`10_SaveRescue.lua:508-537`). The eyes found one divergence; re-derivation found
**four**:

1. the missing drone-dial gloss — SUBSTANTIVE;
2. ⛔ **ordering** — `join()` sorts the already-formatted `"N noun"` strings as
   TEXT, so groups queue by the digits of their counts read as characters.
   ⭐ **Confirmed by the witnessed dialog, not by reading code**: D13's recorded
   `1 + 1533 + 2 + 22 + 4 + 4 = 1566` is exactly that sort over this save's noun
   sums ⇒ **"2 drone stat dials" printed THIRD of six** on the night;
3. `35–115` (spec, en dash) vs `35-115` (build, hyphen) — cosmetic;
4. `(one re-roll)` vs `(one re-roll each)` — cosmetic, and **the build is right**;
   the design text is wrong in the plural.

**Resolution: SPEC-AMEND, marked PROVISIONAL.** Reasoning, in full, at
`D13_EXPOSED_SET.md` §10.5's correction block. The load-bearing part: a code fix
leaves the *new* string unsampled on a gamepad-native `WaitMessage`, the gloss
makes exactly the line that would wrap ~60 characters longer, wrapping is a
screen-only property **no log can adjudicate**, and the sitting's screenshot of
that dialog was partly covered by Test Kit output — so it prices an owner
re-witness (floor: one visit, per `EF-055`'s measured limit) on an artifact whose
publish is unmade. ⛔ **`tested` is NOT disturbed** — the reading that carries it
was *"text matching `report_text()` exactly"*, still true of the build as it
stands. Routed as **checklist item 28**, bundled with 17.

⭐ **Nothing this chain built quotes either dialog text**, deliberately, so item
28 cannot invalidate any surface whichever way the owner rules.

## Every count to re-emit at your moment (rule 3 — none of these are load-bearing from prose)

| count | what prompt 1 measured, 2026-08-14 | where it appears |
|---|---|---|
| TestKit probes | **94** (`--emit-counts`) | fix-pack card: *"a suite of 94 checks"* |
| suite verdict | **`78 PASS, 0 FAIL, 16 SKIP, 0 ERROR`**, read out of `archive/rs_r0_Mars.exe-20260813-11.42.08.log` directly. 78 + 16 = 94 | agent-side only |
| opt-in modules | **8 registered, 1 default-active, 7 optional** (`--emit-counts` in the opt-in repo) | opt-in card: *"eight … seven off … two dials at base"* |
| judgment calls | **5**, re-derived at the shipped fix list (`content/fix-list.md:95, 283, 323, 344, 669`), independently of the card | fix-pack card |
| exposed sites | **12 + 15 = 27**, re-counted at §2a/§2b's tables | ⛔ agent-side only, never a player surface |
| metadata string lengths | table in `RELEASE_PORTAL_PREP.md` §3 | agent-side |
| packaged file counts | **90→78** fix pack, **22→12** opt-in, **4→4** rescue | `RELEASE_PORTAL_PREP.md` §4 |

⚠️ **`94` is the only number that reaches a player, and the card says "a suite of
94 checks is run", never "94 passing".** 78 pass, 16 skip in that cell; a skip is
not a pass. Check that nothing drifted.

## Routed / filed, not fixed

1. **`C:\Dev\SMR-CommunitySaveRescue\README.md`'s "Status" section is stale** —
   still says nobody has watched the dialogs and *"that sitting is scheduled"*.
   It ran 08-14 and passed. Understates, so it breaches no rule. **Your call
   whether a status paragraph belongs in a shipping repo's README at all.**
2. **Store links into the site** (`content/install.md:3`'s "No store links yet")
   — step 2 of the ④ link order. ⛔ Filed, not touched: the site is
   terminal-audited.
3. **`Opt_DroneOverhaul.lua`'s header** names the old Mod Options path. Comment,
   other repo, never seen by a player. Carried forward from `STORE_OPTIN.md`.
4. ⚖️ **The opt-in mod ships as `0.1` while its own changelog says "Initial
   release."** Recommendation on the sheet: 1.0. ⛔ Not changed by an agent.

## Two things you should re-check hardest

* ⛔ **`RELEASE_DESCRIPTION_RESCUE.md` is entirely non-card text**, plus the
  drafted Save Rescue sentence in `RELEASE_DESCRIPTION_OPTIN.md`'s FILL-IN 2.
  Prompt 1 ran the shipped-module control over both and wrote the tables — **run
  yours firewalled from them, per your Job 1.** These are the only new player
  sentences this chain produced.
* **The route-check of D13's frozen uninstall draft found three defects**
  (`RELEASE_UNINSTALL_ASSEMBLY.md` §2): no restart step, the only remedy being a
  possibly-unpublished tool, and an "update first" step that is inert at launch.
  The corrections were taken from the already-audited site page where it had them
  right. ⚠️ **Check that the reconciled text did not import a site claim the
  cards contradict** — that direction was checked, but by the same session that
  wrote it.

## Verified route-checks you can reuse (or attack)

* All four site anchors quoted in the fill-in tables were checked against the
  **built HTML**, not inferred from headings:
  `install/#what-it-puts-in-your-save`,
  `faq/#will-it-fix-a-save-that-is-already-broken`,
  `faq/#i-dismissed-a-building-not-working-warning-and-it-came-back`,
  `faq/#my-retirement-domes-hotel-is-filling-up-with-jobseekers` — each `id=`
  present exactly once in `site/`.
* ⛔ **The site root URL is NOT asserted anywhere.** `mkdocs.yml` sets no
  `site_url`; every mention says to copy the address GitHub prints on the Pages
  settings screen. Do not let a plausible-looking URL creep in.
* **No portal character limit is asserted.** None was verifiable without an
  account; all rows are marked check-at-paste. If you can verify one locally,
  that is an improvement — but do not supply one from memory.
