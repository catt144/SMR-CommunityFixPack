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
2. **Anything downstream of checklist 19** (the 3 ungated GT bodies). If the
   owner rules that they get exits, that is a code change to the fix pack, and
   until then no doc may describe those threads' uninstall behaviour.
⚠️ Also note `STATE.md` sequences MOD_DESCRIPTION as release item ③, AFTER D13
(①) and the combined sitting (②). This chain does not overturn that: it does the
work ③ needs so ③ becomes assembly rather than authoring. **It may not lift the
`MOD_DESCRIPTION.md` freeze** — see stop conditions.

## ⛔⛔ THE EXPOSURE HAZARD — read before proposing any platform

**`docs/` MUST NEVER become the published site.** It holds the entire agent
corpus and `PLAYTEST_CHECKLIST.md`, which carries the owner's personal notes,
open decisions, save names and session history. On 2026-08-13 a hard-coded save
path carrying the owner's Windows username and SteamID64 was scrubbed from three
files in this repo and one in the opt-in repo — **and it is still in git history
on both public repos** (104 of 828 commits here; checklist decision 20 has the
options priced). A docs site generated from `docs/` would republish all of it,
prettier and more findable.

⇒ **Player-facing content lives in its own tree**, written for players from the
start, never generated from agent docs. ⚠️ And `docs/` root is doccheck-enforced
against `docs/README.md`'s map (folder contract), so a new player-docs folder
CANNOT simply be dropped in `docs/` — placement is prompt 1's Job 2 to propose.

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
