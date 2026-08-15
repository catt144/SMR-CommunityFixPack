# Portal prep — the sheet for the launch sitting (④)

**Built 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`, Job 3.**
Read top to bottom. Everything below was measured or re-derived this session;
⛔ nothing was copied from `STATE.md`.

⛔ **No agent publishes anything** (chain rule 5). Every action on this sheet is
yours.

---

## 0. ⛔ READ THIS BEFORE YOU BOOK THE AFTERNOON

**Two things can stop ④ from finishing, and one of them is not a decision.**

### (a) ✅ The preview art EXISTS and is CHOSEN — the blocker is cleared

You ruled the floor (checklist 24: text-on-image), the agent painted six
candidates without opening the game (designed Mars backdrops, no screenshot
needed), and **you picked C1 for both mods, 2026-08-14**. The files to upload:

* `docs/agent/reports/preview_art/FINAL_fixpack_preview.png` (40 KB)
* `docs/agent/reports/preview_art/FINAL_optin_preview.png` (37 KB)

Both 1024×1024, far under the recorded limits (**Paradox Mods ≤ 2 MB, Steam
≤ 1 MB**). The four unchosen candidates stay in the same folder as alternates.
ℹ️ The floor stays replaceable: if a capture sitting ever produces real vistas
(Pass G), the same lettering drops onto one and the portal image is swapped —
costs nothing, touches nothing else. No rescue-mod art exists or is needed
(17 hold-off); if the contingency fires, the C1 template makes a third in
minutes.

### (b) + (c) ✅✅ ALL FIVE CALLS RULED 2026-08-14 AND APPLIED — nothing here waits on you any more

| item | ruling | applied |
|---|---|---|
| **29** the notice paragraph | **STRIKE** | ✅ deleted from both cards, the rescue card, the assembly and the site FAQ; source records corrected |
| **17** Save Rescue publish | **HOLD OFF** — reserve; launch only if post-release reports show players stuck with dial residue | ✅ fill-in marker + assembly section deleted per defaults; card kept as the ready contingency draft |
| **28** the rescue dialog | closes with 17: **ship as built** — re-decide (incl. the save-step line) before upload if the contingency fires | ✅ recorded on item 17 |
| *cleanliness sentence* | **Reading A — the pack alone** | ✅ no text change; the card's deliberate absence stands |
| *opt-in version* | **1.0** | ✅ `metadata.lua` set to 1.0.0 |

⇒ **④ is now decision-free AND art-complete: upload two mods (with their FINAL
previews from §0(a)) → links → Pages.**

---

## 1. The order of operations — links only exist after the step that creates them

⛔ **Do not reorder these.** Each step's output is the next step's input, and
doing them backwards means going back to edit a live page.

| # | step | what it creates | who |
|---|---|---|---|
| 1 | **Upload both mods** (⛔ not Save Rescue — held in reserve, item 17) | ⭐ the **store URLs**. They do not exist until now | you |
| 2 | **Put the store links into the site pages** | the site stops saying "no store links yet" | ⛔ **agent work, ~10 min, already filed** — see §5 |
| 3 | **Switch GitHub Pages on** | ⭐ the **site URL**. GitHub prints it on the Pages settings screen — copy it from there, do not type it | you |
| 4 | **Fill the site links into the store cards** and re-save them | the cards' FILL-IN markers close | you |

⚠️ **Step 4 means editing a store page you have already published.** That is
normal and expected — it is why every site link in both cards is a marker with a
delete-instead answer, so a card is complete and honest at step 1 and merely
*better* after step 4.

ℹ️ The **store cross-links between the two mods** (each card pointing at the
other) become available at the end of step 1, not step 4.

---

## 2. What to paste, per product

| product | paste this | into |
|---|---|---|
| **Community Fix Pack** | `RELEASE_DESCRIPTION_FIXPACK.md`, everything between the two `═══ PLAYER TEXT ═══` rules | the mod page body |
| **Opt-In Modules** | `RELEASE_DESCRIPTION_OPTIN.md`, same block | the mod page body |
| ~~Save Rescue~~ | ✅ 17 ruled **hold off** — nothing pasted; the card waits as the contingency draft | — |

⛔ **Search each pasted block for `>>> FILL-IN` before you save the page.** Every
marker sits on its own line and every one tells you how to delete itself. **Six
markers across the two cards: 4 in the fix pack, 2 in the opt-in** (the opt-in's
third was the Save Rescue sentence, deleted with the 17 ruling; the 08-14 strike
of the notice paragraph also shortened both bodies below).

**Body sizes, re-measured 2026-08-15 by the `unattended-3` terminal audit**
(markers excluded; the fix-pack card grew by that chain's two modules — the
Automation-policy disclosure paragraph, the sixth judgment-call bullet, and the
five→six / 94→96 count edits, all diff-proven VERBATIM against the audited
STORE file after the change):

| card | characters | words |
|---|---|---|
| Community Fix Pack | 11,581 | 2,018 |
| Opt-In Modules | 15,907 | 2,774 |
| ~~Save Rescue~~ *(contingency draft, not pasted)* | 4,202 | 792 |

---

## 3. The `metadata.lua` strings — state, counts, and what to check at the paste

**State: applied and live in all three files.** The fix-pack and opt-in strings
were corrected and applied on your instruction 2026-08-13 (`1ac1187`). ⭐ **Two
more defects were found and corrected 2026-08-14** under your standing 22b word
(*"change any wordings to their accurate versions"*) — text only, no behaviour,
no version bump:

1. ⛔ **The fix pack's changelog still sent players to the wrong name.** It read
   *"…their own mod, the Community Opt-In Pack"* — the dead working title. The
   08-13 pass corrected that name in the `description` and missed it four lines
   below in `last_changes`, in the same file, under a comment saying it had been
   corrected. A player told to look for that name finds nothing on any store.
2. ⛔ **Save Rescue's changelog quoted a repository file path** — and the folder
   it names is on that mod's own exclusion list, so the document it invited a
   reader to consult was never inside the download. Rewritten in plain words.

### ⚠️ Character limits — counted, but NOT checkable from here

**Every string is counted below. ⛔ No portal's limit could be verified from any
local source, and none is asserted from memory** — that is a claim about a
website neither of us can check without an account, and this project does not
ship those. **Treat every row as check-at-paste**: the portal will either show a
counter or refuse the field, and both answers arrive in two seconds.

| mod | `title` | `short_description` | `description` | `last_changes` |
|---|---|---|---|---|
| Community Fix Pack | 18 | 184 | 843 | 112 |
| Opt-In Modules | 34 | 177 | 884 | 100 |
| Save Rescue | 11 | 147 | 732 | 442 |

*(fix-pack `description` re-measured 2026-08-15: "Five of the fixes are
judgment calls" → "Six", 844 → 843 — the only string the `unattended-3` chain
moved; the other cells were re-measured unchanged.)*

*(characters, re-measured 2026-08-14 by the terminal audit from the three
`metadata.lua` files. ⛔ Two corrections to the original table: the Save Rescue
`description`/`last_changes` cells were TRANSPOSED as first written, and the
rescue strings then grew — the audit added the missing save step and fixed the
stand-down sentence, per its record in `RELEASE_DESCRIPTION_RESCUE.md`.)*

⭐ **The one thing worth eyeballing at the paste**, and it is measurable locally:
**the Opt-In Modules `description` is the only string carrying characters beyond
plain text** — an arrow (`→`) and a warning sign built from two code points
(`⚠` plus an invisible modifier). Its **card body carries the same three**. If
any field renders as boxes, question marks or a stray character, that is what
happened, and the fix is to retype those few characters in the portal's own
editor. Every other string and both other card bodies use nothing but ordinary
text and an em dash.

---

## 4. Packaging — what actually lands in a player's download

⭐ **Checklist item 23 is DONE, 2026-08-14** — your ruling was *"yes, add the
missing patterns, at launch prep"*, and this is launch prep. Measured over the
real trees, before and after:

| mod | files shipped BEFORE | AFTER | what stopped shipping |
|---|---|---|---|
| Community Fix Pack | **90** | **78** | `CLAUDE.md`, `.gitattributes`, all **10** files of `tools/` |
| Opt-In Modules | **22** | **12** | `CLAUDE.md`, `.gitattributes`, all **8** files of `tools/` |
| Save Rescue | **4** | **4** | nothing — it was already clean, built after the lesson |

The 78 and 12 reconcile to the emitter exactly: 75 + 9 code files, plus
`items.lua`, `metadata.lua` and `LICENSE` each.

⭐ **2026-08-15 (`unattended-3` audit): the fix pack now ships 80 files** — the
chain's two new modules (`Fix_DistressPopupPause.lua`,
`Fix_AutomationLawCompensation.lua`) land in `Code/`. Re-simulated over the
real tree with the shipped `ignore_files` (the same method as the table above):
**80 = 77 `Code/*.lua` (emitter-matched) + `items.lua` + `metadata.lua` +
`LICENSE`**, nothing else. The opt-in and rescue packages are untouched.

⚠️ **`LICENSE` still ships, deliberately.** Item 23 listed it among the misses,
but the rescue mod — built later — states *"LICENSE ships on purpose"*, and a
licence inside the package is right. All three now agree. **Say the word if you
want it out and it is one line each.**
✅ **Item 23's one unverifiable sub-case is moot**: whether `.github/` slips past
the `.git` pattern does not matter, because **no mod repo has a `.github/`
directory** (checked in all three). Only the site repo does, and it is not a mod.

### ⚖️ The version numbers are yours, and one of them contradicts its own changelog

| mod | ships as | its changelog says | note |
|---|---|---|---|
| Community Fix Pack | **1.0** | "Initial release" | ✅ consistent, nothing to do |
| Opt-In Modules | **1.0** | "Initial release" | ✅ **RULED 2026-08-14 ("we go 1.0, especially with the amount of QA we have done") and APPLIED** — `metadata.lua` now 1.0.0 |
| Save Rescue | **0.1** | "Initial pre-release" | ✅ consistent; not publishing at launch (item 17 hold-off) |

---

## 5. Filed for the agent side, so you do not do it by hand

| item | what | when |
|---|---|---|
| **Store links into the site** | `content/install.md` opens with *"No store links yet — this page gets the links when they exist."* One admonition to replace, plus store buttons on the landing page if wanted | step 2, after upload |
| **Save Rescue's repo README is stale** | its "Status" section still says nobody has watched the dialogs and *"that sitting is scheduled"* — it ran 2026-08-14 and passed. It understates rather than overstates, so nothing is misleading a player, but it is a public page contradicting the record | any time; routed to this chain's audit |
| **`Opt_DroneOverhaul.lua`'s header comment** names the old *"Mod Options → Community Fix Pack"* path | a code comment in the other repo, never seen by a player | any time |

⛔ **The site's five pages are terminal-audited and are not edited in passing.**
Anything found in them is filed, which is why the first row above is a filed task
and not something already done.

---

## 6. Save hygiene at the sitting — `EF-051`, and whether it touches you

**It does not touch ④ as scoped.** Uploading a mod page, pasting text and
switching Pages on never open the game and never touch a savegame.

⚠️ **It touches ④ the moment the capture sitting rides along** (§0(a) — and it
probably should, since the preview art needs the game anyway). In that case, both
standing rules are live:

* ⛔ **`EF-051` — Steam Cloud is ON**, at your own request and temporarily, so a
  save deleted with the game closed comes back on the next launch. Nothing is
  called *gone*; close-outs say **"deleted, listing verified"**. `CP60RT` and
  `Autosave Sol 311` are **HELD** and must survive the day.
* ⛔ **`EF-056` — a byte copy of an autosave is still an autosave**, and its
  rotation deletes real ones. It ate `Autosave Sol 306` for good and took
  `Sol 311` twice more during the last sitting. **Pre-copy every autosave before
  any launch, and reconcile after every launch** — not after the one you think
  will do it.

---

## 7. What is ready, in one line each

| | state |
|---|---|
| Fix-pack card | ✅ **paste-ready** (item-29 strike applied), 4 fill-ins, every one deletable |
| Opt-in card | ✅ **paste-ready** (item-29 strike + 17 marker deletion applied), 2 fill-ins, every one deletable |
| Save Rescue card | ✅ **held in reserve** (17 hold-off) — audit-corrected contingency draft, nothing pasted at launch |
| Uninstall story | ✅ reconciled; **four** defects in the inherited draft found and corrected — three by assembly, the missing save step by the audit (`RELEASE_UNINSTALL_ASSEMBLY.md` §2) |
| `metadata.lua` ×3 | ✅ applied, counted; 2 defects corrected by prompt 1, 2 more (rescue) by the audit; opt-in version set 1.0.0 |
| Packaging | ✅ item 23 done, measured; ✅ versions ruled and set |
| Site | ✅ built + audited + item-29 strike applied, ⛔ **nothing on the web**; needs step 2 then step 3 |
| Preview art | ✅ **chosen 2026-08-14 — C1 for both mods**, FINAL files named in §0(a), sizes verified under both limits |
| Decisions owed by you | **0** — all five ruled 2026-08-14 (§0(b)), art chosen |
