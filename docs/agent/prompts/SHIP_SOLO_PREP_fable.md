# Ship the fix pack ALONE — park the opt-in, settle the versions, tag

**Owner ruling, 2026-08-17:** *"I am launching the bug fix mod before the opt in
mod, its not ready imo to be launched. And I don't want to gate it on the bug fix
mod. But in all our public documentation it makes it seem like that mod is
already there. The documentation is great so I don't want to actually lose it,
but if we can, make that a coming soon or just hide the portions and references
until we are ready for them?"*

♻️ **SELF-CONSUMING.** Finish, commit, and **delete this file in the same
commit**, naming its grave
(`git show <sha>:docs/agent/prompts/SHIP_SOLO_PREP_fable.md`).

⛔⛔ **THIS IS THE LAST THING BEFORE ④.** The public-docs checkup already ran and
declared the pages ready — **that verdict was for a two-mod launch and it no
longer holds.** Nothing ships until this is done.

---

## 0 · Staleness check
```
git log --oneline -10
git pull
git -C C:\Dev\SMR-CommunityMods log --oneline -5
```
The site is a **separate repo** with its own remote. So are the opt-in and rescue
repos. ⛔ **This prompt touches the fix pack and the site. It must not commit
anything to the opt-in or rescue repos.**

## 1 · 🗒 Live todo list from your first action — one item per surface.

## 2 · The situation, precisely

**Shipping now: the fix pack alone.** The opt-in mod is not ready by the owner's
judgement and **must not be a prerequisite for anything**. The rescue mod was
already ruled contingency-only (checklist 17) and does not publish.

⇒ **Every player-facing surface must describe a product that stands completely
on its own**, with no reference to a mod nobody can install.

⭐ **And here is the fact that makes this cheap: no player has ever seen any of
this.** This is a first release. The `D01`–`D07`/`D09`/`D12` behaviours that
"moved to the opt-in mod" were never in a shipped pack, so a first-time player has
nothing to miss and no expectation to manage. **Removing a reference loses
nothing; it does not create a gap.** Verify that claim before you rely on it.

## 3 · ⭐ The survey, already done — 22 references across 8 surfaces

Measured 2026-08-17 while scoping this. **Confirm it yourself; it is a starting
point, not an inventory.**

| surface | hits | shape |
|---|---|---|
| `content/index.md` | 2 | `:7` prose positioning the opt-in; **`:66` a whole content tab** `=== "Community Fix Pack: Opt-In Modules"` |
| `content/install.md` | 1 | `:65` its options page |
| `content/faq.md` | 1 | `:127` what the opt-in is |
| `content/fix-list.md` | 1 | `:938` *"…which you do not need to install. Seven of its eight modules…"* |
| `content/for-modders.md` | 4 | `:39-40` a `SMROptInPack_Disabled` code example · `:56` a link to the opt-in repo · `:88` `SMROptInPack.ListFixes()` |
| `RELEASE_DESCRIPTION_FIXPACK.md` | 6 | the store card |
| `metadata.lua` | 7 | ⛔ **`:33` `last_changes` — see below.** The rest are Lua comments |
| `mkdocs.yml` | 0 | — |

⛔⛔ **THE ONE THAT MATTERS MOST — `metadata.lua:33`:**

```lua
'last_changes', "Initial release: the bug fixes. The optional modules moved to their own mod, Community Fix Pack: Opt-In Modules.",
```

**That string ships INSIDE the mod**, is shown to players, and **cannot be
changed without a version bump and a re-upload.** It names a mod that will not
exist. Fix it here or it is wrong for the life of version 1.

⚠️ Also sweep `RELEASE_DESCRIPTION_OPTIN.md`, `RELEASE_DESCRIPTION_RESCUE.md`,
`STORE_FIXPACK.md`, `STORE_METADATA_STRINGS.md`, `RELEASE_PORTAL_PREP.md`,
`RELEASE_UNINSTALL_ASSEMBLY.md`, `SITE_BUILD_AUDIT.md` and the site `README.md`
— several are source records the shipped text is diff-proven against, so they
move together or the VERBATIM pairing breaks.

## 4 · Job A — park the references, reversibly

### A1 · The mechanism, and it differs by surface type

⛔ **`<!-- -->` in markdown is NOT hiding on the site.** MkDocs passes HTML
comments through to the served page, so the text stays readable in page source.
For the site, parked text must **leave the page** and live in the park record.

| surface | mechanism |
|---|---|
| site pages | **remove from the page**, verbatim into the park record |
| store cards | remove from the shipped body; the source record keeps it with a marker |
| `metadata.lua` player strings | rewrite; original verbatim into the park record |
| `metadata.lua` Lua comments | ✅ **leave alone** — engineering context, not player-visible |

### A2 · The park record — this is the deliverable that answers "don't lose it"

Create `agent/reports/PARKED_OPTIN_REFERENCES.md`, modelled on
`SHELVED_F85_DISTRESS_PAUSE.md`, which exists because *"it's in git history"* was
explicitly rejected as an answer. It must hold:

- **every removed passage VERBATIM**, byte-compared before deletion
- its exact source: file, line, and enough surrounding context to put it back
- the **restore trigger**, in one sentence: *the opt-in mod publishes*
- a **restore checklist**, step by step, surface by surface
- an **already-proven table** — what was verified at parking time (counts
  re-measured, VERBATIM pairs re-proven, `mkdocs --strict` green)

⇒ Restoring must be a mechanical job for a session with no memory of today.

### A3 · ⚖️ "Coming soon" or silence? — RECOMMENDATION, owner may override

**Recommend: silence.** Say nothing about the opt-in on any player surface.

- A "coming soon" is a **promise with no date**, on a mod the owner just judged
  not ready. If it slips it ages badly and is on a store page they must edit.
- The owner's own framing was that the fix pack must not be **gated** on it — a
  teaser re-couples them in the reader's mind.
- The park record makes restoring cheap, so silence costs nothing later.

⛔ **If the owner prefers "coming soon", it goes in ONE place** (the site FAQ),
never on the store card, never in `metadata.lua` — because those two are the
expensive ones to change.

### A4 · ⚠️ The trap — check for holes, do not just delete

Removing a reference can leave a **question a page no longer answers**:
- `fix-list.md:938` exists to explain a boundary. Remove it and does the fix list
  read as *complete*, or as *missing things*?
- `for-modders.md` loses a worked lever example. Is the page still coherent?
- `index.md:66` is a whole tab. **Does removing one tab leave a lopsided tab
  group, or does the layout need adjusting?**

⇒ **Read each page end to end after editing.** The test is not "is the reference
gone", it is **"does this page still make sense to someone who has never heard of
a second mod."**

### A5 · Verify the fix pack actually stands alone in CODE, not just in prose
- Does anything in `Code/` behave differently by the opt-in's presence or
  absence? (`STATE.md` says opt-in wrappers are OUTERMOST and the fix pack does
  not depend on them — **verify, do not inherit**.)
- Does any player-facing string promise behaviour that now lives in the opt-in?
  That is the `F24`/`F28` class — *promising deleted fixes* — and it has shipped
  in this project before.
- Does the uninstall assembly still read correctly for a **one-mod** install?

## 5 · Job B — versions, then the tag

Do this **after** Job A, because removing text changes the ④ sheet's character
counts and they must be re-measured.

### B1 · The version call — ROUTE IT, it is the owner's
`metadata.lua` currently reads `version_major=1, version_minor=0, version=1` ⇒
`PackVersion` renders **1.0.1** for a first public release. Opt-in is a clean
1.0.0; rescue is a deliberate pre-release 0.1.0.
**Ask: is 1.0.1 intended, or should the first release be 1.0.0?** Harmless either
way — no player ever saw a 1.0.0 — but it must be deliberate. Put it on the
checklist with a recommendation and **do not change it unilaterally.**

### B2 · Re-measure everything Job A moved
Character and word counts on the ④ sheet · the 12 metadata string counts ·
STORE ↔ RELEASE **diff-proven VERBATIM again** after every edit. `STATE.md`
records that a ④ cell was wrong once because a deletion was not subtracted —
**do not repeat it.**

### B3 · Tag — last, on the final tree
Per the new `WORKFLOW.md` §"Release marking":
```
git tag -a fixpack-v<major>.<minor>.<version> -m "uploaded <portal> <date>"
git push origin <tag>
```
⛔ **Tag only when the tree is final and doccheck is GREEN.** If anything changes
before the upload, move the tag. Record portal version → commit sha on the ④
sheet in the same pass.
⛔ **Do NOT tag the opt-in or rescue repos.** Nothing is shipping from them.

## 6 · Scope fence
**IN:** the fix pack repo, the site repo, the park record, the version routing,
the tag.
**OUT:** ⛔ committing to the opt-in or rescue repos · ⛔ `archive/MOD_DESCRIPTION.md`
(frozen, holds known-false claims on purpose) · ⛔ any `Code/` change beyond what
A5 proves is required · ⛔ the four `smrcf-*` / `jumbo-cave` chains · ⛔
publishing the site (Pages OFF, `workflow_dispatch` only) · ⛔ performing the
upload — that is the owner's.

## 7 · Stop conditions
- A5 finds the fix pack genuinely depends on the opt-in → **STOP.** That is a
  release-blocking finding, not a copy edit.
- Removing a passage leaves a hole you cannot fill without a promise → route it
  to the owner rather than inventing a commitment.
- `mkdocs --strict` or `doccheck` red → fix before committing.
- The VERBATIM pairing cannot be re-proven after edits → **do not ship**; the
  cards and their source records must agree.

## 8 · ⛔ What may not be claimed
- ⛔ **"All references removed"** without a fresh grep across every surface in §3
  **plus** the ones §3 tells you to sweep.
- ⛔ **"Nothing was lost"** unless the park record holds it verbatim,
  byte-compared before deletion.
- ⛔ **"The pages still read well"** — a judgement. Say what you read, and name
  anything you changed for flow rather than accuracy.
- ⛔ **Any count you did not re-measure.** Inheriting a number is how "95 checks"
  survived two corrections.
- ⛔ **"Ready to upload"** unless doccheck is GREEN, `mkdocs --strict` is GREEN,
  both VERBATIM pairs re-proven, and A5 answered.

## 9 · Close-out
One commit in the fix pack repo, one in the site repo (**pushed separately**):
park record created · all surfaces edited · counts re-measured · version question
and any "coming soon" call on `docs/PLAYTEST_CHECKLIST.md` → *"Decisions waiting
on you"* (R10) · `STATE.md` extended, not grown (60-line cap; evict resolved
material to `archive/SESSION_LOG.md`, never an obligation) · doccheck GREEN ·
`mkdocs --strict` GREEN · `git rm` this file · grave named · push.

**End with a plain-language owner report**: what was parked, where it went, how
to bring it back, what you need from them, and — in one sentence — **whether the
fix pack is ready to upload on its own.**
