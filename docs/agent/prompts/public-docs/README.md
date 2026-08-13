# Chain — public-docs (the player-facing surfaces; NOT yet kicked off)

**Status: AUTHORED 2026-08-13, NOT STARTED.** Nothing in `STATE.md` points here
yet, deliberately — the owner asked what starting would look like, and this is
the answer, not a commitment. Prompt 1 wires it into STATE if and when it runs.

## Why this chain exists

Owner question, 2026-08-13: *"Can I start working on public documentation build?
FAQs, what we should screenshot, how to explain everything without triggering
people's TLDR. Do we need something like this… can GitHub do that in a clean
unconfusing way?"* — asked while the D13 chain is mid-flight, explicitly looking
for work that runs BESIDE it.

## ⭐ The answer to "can it run beside D13": MOSTLY YES, and the seam is exact

**Unblocked today** — every one of these is frozen or measured already:
* the 74 fixes' player-facing copy (ship line ruled 08-12; the evidence campaign
  is FROZEN, so the entries are not moving),
* the 8 opt-in modules' copy (built, verified, audit-sustained 08-12),
* surface architecture, platform choice, tone, the whole TL;DR problem,
* the screenshot/asset plan,
* the FAQ, minus the two questions below,
* the **relabel wording** (checklist "mod-page relabel package": ADOPTED
  2026-08-04, wording still owed by the owner, explicitly a launch-prep
  instruction). ⭐ Drafting it here would close a decision that has been open
  nine days.

⛔ **Blocked, and the chain must NOT guess at them:**
1. **The save-safety / uninstall section.** D13 owns the disposition table, and
   the rescue artifact's very existence in a store is a release-time call —
   checklist 17 decided the artifact's SHAPE (option (c), 2026-08-13) but
   recorded ⛔ **"build ≠ publish"** in the same breath. Write the section's
   skeleton; leave the artifact's name, link and publish status as a marked hole.
2. ~~**Anything downstream of checklist 19** (the 3 ungated GT bodies).~~
   ✅ **UNBLOCKED 2026-08-13, same day this chain was authored:** the owner ruled
   GO and the three gates were built in-pack (`Fix_CrystalMysteryHang`,
   `Fix_ExtenderFlapChurn`, `Fix_TrackConnectorPingPong`), with the four
   modules' save-footprint disclosure rewritten and counts unchanged. ⚠️ **Do not
   inherit that summary** — re-read the entries and the checklist item before
   any uninstall sentence rests on it.
⚠️ Also note `STATE.md` sequences MOD_DESCRIPTION as release item ③, AFTER D13
(①) and the combined sitting (②). This chain does not overturn that: it does the
work ③ needs so ③ becomes assembly rather than authoring. **It may not lift the
`MOD_DESCRIPTION.md` freeze** — see stop conditions.

## ⛔ WHY `docs/` IS NOT THE SITE — and the correction that produced this section

⚠️ **An earlier draft of this README said "`docs/` must never become the
published site" in a way that implied SECRECY. That was wrong and the owner
caught it** (2026-08-13): *"its already on a public repo. Part of the reason to
do these big mods on github is so people can be sure they aren't adding anything
sketchy."* They are right, and the corrected framing is load-bearing for this
whole chain:

⭐ **`docs/` being public is a FEATURE, not a leak.** It is the receipts behind
every claim the mods make, and the working notes — corrections included — are a
*stronger* trust signal than a polished page. **Nothing in this chain should try
to hide it, and no future session should read this folder as "docs/ is
sensitive".**

**The reason the site is separate is AUDIENCE and JOB, and there are exactly
three:**
1. A player searching *"is my bug fixed"* must not land in agent workflow docs.
2. A generated site reads as **published documentation**. Working notes carry
   superseded numbers and in-progress wrong answers — fine as receipts, bad as
   something people quote back at you.
3. A site adds search-engine indexing and implied endorsement that a repo folder
   does not.

⇒ **Player-facing content is WRITTEN for players in its own tree**, never
generated from agent docs. ⚠️ `docs/` root is separately doccheck-enforced
against `docs/README.md`'s map, which is why the scaffold sits at repo root.

### ✅ The public-exposure audit RAN 2026-08-13 — inherit the result, re-derive before acting

Scanned both public repos. **Credentials / tokens / API keys / passwords: ZERO.
Emails: only `…@users.noreply.github.com`, GitHub's own privacy address. Git
author: the project identity, not a real name. Personal / health / financial:
none.** Game source is **cited, not reproduced** — ~1,478 fenced lines across all
of `docs/`, only three blocks over 25 lines and two of those are false positives;
real excerpts run 17–27 lines inside a bug entry, and the house discipline is
`file:line` citation. Machine paths survive in 12 files but carry no username
since the scrub. ⇒ **No emergency, and no reason to change the repo's public
posture.** Two items remain, both DECISIONS not defects: the SteamID64 still in
git history (checklist 20) and the third-party roster wording (Job 9).

## ✅ Platform: DECIDED 2026-08-13 — GitHub Pages

Owner ruling, after the alternatives were priced against the peer GitBook site.
⚠️ **UPDATED 2026-08-13 evening — the scaffold has MOVED OUT OF THIS REPO.**
Checklist 21 was ruled the same day: the site lives in its own public repo,
**`catt144/SMR-CommunityMods`** (local clone `C:\Dev\SMR-CommunityMods`), with
`mkdocs.yml` and `content/` at its root and the publish workflow beside them.
The `public-site/` folder and `.github/workflows/publish-site.yml` are **deleted
from the fix pack**. ⛔ Still nothing on the public web. The paragraph below is
the pre-move record; translate its paths, do not edit it.

A working scaffold was committed: **`public-site/`** (MkDocs + Material —
sidebar tree, `Ctrl K` search, right-hand page TOC, dark/light, callouts) with
`.github/workflows/publish-site.yml` to build it. ⛔ **The workflow is
`workflow_dispatch` only and Pages is not enabled**, so nothing is on the public
web; the four pages in `public-site/content/` are LAYOUT SPECIMENS that say so
on their own face. ⚖️ **Still open: which repo hosts it** — prompt 1 Job 2.

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` + `git pull`
   in all three repos (all three now have or share remotes; the opt-in pack went
   public 2026-08-13). A live todo list, updated per item.
2. **Inbox/outbox in writing**; each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same commit.
   Folder emptiness is the terminal prompt's done-condition.
3. **Recorded facts are claims** — including every number in this README.
   Re-derive from the entries and `--emit-counts`, never from prose.
4. **PLAYER LANGUAGE IS A HARD GATE.** No file paths, no function names, no
   `F##`/`D##` ids in anything a player reads, no internal jargon (`gate read`,
   `probe`, `co-run`, `disposition`). The existing `MOD_DESCRIPTION.md` already
   sets this tone — read it before writing a line.
5. **Nothing is published by an agent.** Drafts land in the repo; the owner
   posts to Paradox Mods and flips any site live. Creating an external account
   (GitBook, a Pages domain) is an owner act, never an agent's.
6. ⛔ **No claim about the mods that is not already earned.** The evidence
   campaign is frozen at `fixed` + suite + self-checks + the verified
   save-safety tier — a store page may not upgrade that to "tested" or "proven"
   by word choice. If a sentence needs evidence we do not have, cut it.
7. **Doc-facing changes still run `python tools/doccheck.py`; red blocks.**

## Scope fence

**In:** audience + surface architecture; platform recommendation; the store
descriptions ×2; a searchable fix list; the FAQ; the screenshot/asset plan; the
relabel wording draft; the information design that solves TL;DR.
**Out:** publishing anything; creating external accounts; new fixes or code;
re-opening frozen evidence; overturning STATE's release sequencing; touching
D13's deliverables; lifting the `MOD_DESCRIPTION.md` freeze; preview-image ART
(a commission/asset problem, not a writing one — name it and route it).

## Stop conditions

- A surface needs a fact the project does not have → mark the hole, keep going,
  route it. Never invent the fact.
- The chain finds itself wanting to publish `docs/` → STOP, re-read the exposure
  hazard above.
- D13 lands a ruling that changes uninstall behaviour → the save-safety section
  is re-derived, not patched.

## Manifest (proposed; prompt 1 may re-shape it and should say why)

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_DESIGN.md` | No — decisions routed, none blocking | audience + surfaces + platform + inventory + TL;DR strategy + screenshot plan + FAQ seed. Outbox = prompt 2 |
| 2 | `02_QA.md` | No | fresh-context adversarial review: is the architecture right, is any claim unearned, is anything exposed |
| 3 | `03_BUILD_STORE.md` | No | the two store descriptions + the relabel wording draft, to the owner for approval |
| 4 | `04_BUILD_SITE.md` | No | the fix list + FAQ + site scaffold, unpublished |
| 5 | `05_AUDIT.md` | No (routes decisions) | read every surface as a player would, re-check the exposure gate, empty the folder |
