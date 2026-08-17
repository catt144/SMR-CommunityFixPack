# Rename to **Relaunched Fix Pack** — cosmetic only, no GitHub migration

**Owner ruling, 2026-08-17:** *"Make the prompt do everything visual / cosmetic,
but I don't want to migrate the github, thats more risk for little reward when we
can just do 99.9% of the visual without migrating it. We will go with Relaunched
Fix Pack."*

♻️ **SELF-CONSUMING.** Finish, commit, and **delete this file in the same
commit**, naming its grave
(`git show <sha>:docs/agent/prompts/RENAME_RELAUNCHED_FIX_PACK_fable.md`).

⛔⛔ **THIS BLOCKS ④.** Nothing uploads until it is done — the portal display name
and the mod id are semi-permanent once published, and today is the last cheap day.

---

## 0 · Staleness check
```
git log --oneline -10
git pull
git -C C:\Dev\SMR-CommunityMods log --oneline -5
```

## 1 · 🗒 Live todo list from your first action — one item per surface class.

## 2 · Why this is happening

`fredware`'s mod is **SMR Community Fixes**; ours is **Community Fix Pack**. Same
game, same purpose, and the shared token *Community* does no work — every mod
here is by a community member. Players would mis-route bug reports and reviews in
both directions.

⭐ **For the record, because it will be asked: we are not the copycat.** Our first
commit is **2026-07-24** (*"Scaffold Community Fix Pack… full bug tracker (29
findings)"*); their repository's first commit is **2026-08-04**. Two projects
independently reached for the same descriptive words. This rename is courtesy and
clarity, not concession — **say nothing publicly that implies otherwise**, and do
not mention their mod on any player surface.

**New name: `Relaunched Fix Pack`.** Swept 2026-08-17 — no hits on the web, Steam
Workshop, or in the known Surviving Mars mod set. ⚠️ **The Paradox Mods SM:R
catalogue is JavaScript-rendered and could not be enumerated**; the owner was
asked to confirm via in-game Mod Manager search. **If they have not, ask before
you commit the name.**

**The set becomes:**
> Relaunched Fix Pack · Relaunched Fix Pack: Opt-In Modules · Relaunched Fix Pack: Save Rescue

## 3 · ⛔ HARD FENCES — owner rulings, not suggestions

1. ⛔ **NO GitHub repo renames. NO remote URL changes. NO org moves.** All four
   repos keep their current names. Owner's reasoning: *"more risk for little
   reward."*
   ⚠️ **Consequence to handle gracefully, not hide:** repo URLs will still read
   `SMR-CommunityFixPack` while the mod is called *Relaunched Fix Pack*. That is
   normal and unremarkable — GitHub names and product names differ constantly.
   **Check `for-modders.md` still reads sensibly**, and ⛔ do not add an
   explanation nobody asked for.
2. ⛔ **DO NOT UNDO THE PARKING.** `SHIP_SOLO_PREP` just removed every opt-in
   reference from the player surfaces. You are editing the same files. **Verify
   the parked state is intact when you finish.**
3. ⛔ **Do not commit to the opt-in or rescue repos** beyond their own
   `metadata.lua` title strings, and only if the owner confirms those two should
   move now rather than when they publish. **Route it; do not assume.**

## 4 · The inventory — 72 occurrences, 26 files, in this repo alone

Measured 2026-08-17. **Confirm it; it is a starting point, not a census.** The
site repo and the other two mod repos are extra.

⚖️ **The central judgement: a LIVE surface renames, a HISTORICAL RECORD does
not.** This project already has the pattern — `CLAUDE.md` tells readers that
pre-restructure documents cite old paths and to *"translate mentally, do not edit
records."* Apply the same rule.

### 4a · RENAME — anything read as current

| file | n |
|---|---|
| `metadata.lua` `'title'` | 1 ⛔ **the one that ships** |
| `RELEASE_DESCRIPTION_FIXPACK.md` / `_OPTIN` / `_RESCUE` | 2 / 6 / 4 |
| `STORE_FIXPACK.md` / `STORE_OPTIN.md` / `STORE_METADATA_STRINGS.md` | 2 / 4 / 4 |
| `RELEASE_PORTAL_PREP.md` | 6 |
| `RELEASE_UNINSTALL_ASSEMBLY.md` | 1 |
| `docs/PLAYTEST_CHECKLIST.md` / `PLAYTEST_HELP.md` | 5 / 1 |
| `docs/agent/STATE.md` · `WORKFLOW.md` · `CLAUDE.md` · `README.md` | 2 · 1 · 1 · 2 |
| `Code/00_Core.lua` | 3 — ⚠️ see §5 |
| **site repo**: all 5 `content/*.md` + `README.md` + `mkdocs.yml` | sweep it |
| **opt-in / rescue `metadata.lua` titles** | ⚠️ routed, see §3.3 |

### 4b · DO NOT RENAME — records of past work

`docs/archive/**` (already off-limits, append-only) · `D13_EXPOSED_SET.md` ·
`D13_VERIFICATION.md` · `bugs/D13.md` · `bugs/F48.md` · `bugs/F35.md` ·
`bugs/_notes.md` · `facts/EF-054.md` · `SITE_BUILD_AUDIT.md` ·
`PUBLIC_DOCS_DESIGN.md`

These describe measurements taken and decisions made when the product carried the
old name. **Rewriting them falsifies the record.** Instead: add **one line** to
`CLAUDE.md` beside the existing 2026-08-03 restructure note — *"2026-08-17: the
pack was renamed Community Fix Pack → Relaunched Fix Pack; earlier records use
the old name, translate mentally, do not edit records."*

⚠️ **Borderline cases exist and you must rule each in writing.** If a "record"
is actually a live instruction someone will follow, it renames.

### 4c · ⚠️ The trap — `PARKED_OPTIN_REFERENCES.md` (12 occurrences)

That file holds **parked text verbatim, for restoration when the opt-in ships.**
If you leave the old name in it, whoever restores it later re-introduces
*Community Fix Pack* onto a live page under the new brand.

⇒ **Update the parked text to the new name, and record in the park record that
you did** — with the original wording preserved beside it, so the verbatim claim
stays honest. **The park record's own integrity is the deliverable here; do not
quietly rewrite a "verbatim" block.**

## 5 · ⚖️ Two small calls — RECOMMEND, then route; do not decide alone

**The mod `'id'` (`SMR_CommunityFixPack`) and the log tag (`[CommunityFixPack]`).**
Both contain "Community". Neither is a discovery surface.

⭐ **Recommend: KEEP BOTH.** The reasoning is the owner's own GitHub logic — risk
without reward:
- every archived log and every gate baseline greps the **full bracketed token**;
  change it and no future suite reading is comparable to any past one
- the rescue mod removes objects **BY NAME**
- `EF-054` documents load order using these identifiers
- no player finds a mod by its log tag

⚠️ **Counter-argument, stated fairly:** a log reading `[CommunityFixPack]` under a
mod called *Relaunched Fix Pack* is mildly confusing to a bug reporter. If the
owner wants it changed, it is doable **today** (nothing published, no stored
settings) — but it is the single riskiest edit in this job and it must be its own
decision, not a side effect.

## 6 · The rest of the job

1. **Re-measure every count the text moves.** *Community* (9) → *Relaunched* (10)
   is **+1 character per occurrence**, so the ④ sheet's character/word cells, the
   12 metadata string counts, and any "N characters" claim all shift. `STATE.md`
   records a ④ cell that was wrong once because a deletion was not subtracted —
   ⛔ **do not repeat it.**
2. **Re-prove STORE ↔ RELEASE VERBATIM with an actual diff**, both pairs, after
   every edit.
3. **Fix a factual error while you are in there:** `SMRCF_COVERAGE_SWEEP.md` and
   any other record citing fredware's mod as **id 153410** are wrong — 153410 is
   his older *Bug Fixes* mod; *SMR Community Fixes* is **154004** (owner
   screenshot, 2026-08-17). Correct it wherever it appears.
4. **Read every edited page end to end.** The test is not "the string changed" —
   it is **"does this page read naturally under the new name."** Sentences built
   around the old name may need rephrasing, not substitution.
5. `mkdocs --strict` and `doccheck` GREEN.

## 7 · Scope fence

**IN:** display name across all live surfaces, both repos (fix pack + site), the
park record, the counts, the verbatim proofs, the mod-id correction, the
`CLAUDE.md` translation note.
**OUT:** ⛔ GitHub repo/remote/org changes · ⛔ `docs/archive/**` · ⛔ historical
records per §4b · ⛔ the mod `'id'` and log tag unless §5 is ruled · ⛔ any
`Code/` behaviour change · ⛔ the four `smrcf-*` / `jumbo-cave` chains · ⛔
performing the upload.

## 8 · Stop conditions

- The owner has not confirmed the name against the in-game Mod Manager → **ask
  before committing the name.** It is 30 seconds of their time and it is the one
  check nobody could run for them.
- A rename would falsify a record → leave it, note it in §4b's list, move on.
- The VERBATIM pairing cannot be re-proven → **do not ship.**
- `mkdocs --strict` or `doccheck` red → fix before committing.

## 9 · ⛔ What may not be claimed

- ⛔ **"Renamed everywhere"** without a fresh grep across both repos, including
  the site, and including the two sibling titles.
- ⛔ **"Nothing was lost"** — the park record's verbatim blocks were edited; say
  exactly how, and show the originals are still readable.
- ⛔ **Any count you did not re-measure.**
- ⛔ **"The pages read naturally"** without having read them end to end. Name what
  you rephrased for flow rather than substituted.
- ⛔ **Any public statement about the other mod, its author, or why we renamed.**
  The rename is ours; the reason stays internal.

## 10 · Close-out

One commit in this repo, one in the site repo (**pushed separately**): all live
surfaces renamed · park record updated with its integrity note · `CLAUDE.md`
translation line added · counts re-measured · both VERBATIM pairs re-proven ·
mod-id corrected · §5 call routed to `docs/PLAYTEST_CHECKLIST.md` → *"Decisions
waiting on you"* (R10) · `STATE.md` extended, not grown (60-line cap; evict
resolved material to `archive/SESSION_LOG.md`, never an obligation) · doccheck
GREEN · `mkdocs --strict` GREEN · `git rm` this file · grave named · push.

**End with a plain-language owner report**: what changed, what deliberately did
not and why, what you need from them, and — in one sentence — **whether the pack
is ready to upload as *Relaunched Fix Pack*.**
