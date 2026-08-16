# Coverage sweep — the seven leads from `smr-community-fixes` (model-agnostic)

Paste everything below into a fresh Claude Code session. **Start with
`git log --oneline -10` + `git pull`** — this file goes stale the moment
another session commits. Written 2026-08-16 from an owner ask: *"I would like
ours to be fully fledged, one mod fix all."*

> ⛔ **THIS LEG WRITES NO FIX CODE.** It produces `agent/bugs/` entries (or
> reasoned rejections) and nothing else. Building is a separate, later decision
> — see §6.

> ♻️ **THIS FILE IS SELF-CONSUMING** (`agent/reports/CHAIN_METHOD.md`). It is a
> one-off, not a chain: there is no successor to hand to. **You finish by
> integrating the findings into the standing docs, committing, and DELETING
> THIS FILE in the same commit**, with the close-out message naming its grave
> (`git show <sha>:docs/agent/prompts/COVERAGE_SWEEP_SMRCF.md`). See §7. The
> file's absence is the done-condition; a half-done sweep does not get to sit
> here looking like a plan.

> 🗒 **KEEP A LIVE TODO LIST FROM YOUR FIRST ACTION** — one item per lead, updated
> the moment each moves. The owner reads that list to decide whether to step in;
> a list updated at the end is useless to them.

---

## 0. Setup — five minutes, no subscription needed

**Clone their repo locally and read it from disk.** Do not investigate through
web fetches — it is slow, partial, and you will want to grep.

```
git clone https://github.com/SMR-community/smr-community-fixes \
          C:\Dev\_ref\smr-community-fixes
```

⛔ **Outside our repos on purpose.** `C:\Dev\_ref\` is a reference clone, not a
working tree: never add it as a submodule, never copy files out of it into
`Code/`, never let a path to it appear in a doc we ship.

⛔⛔ **DO NOT INSTALL OR ENABLE THEIR MOD ON THE RIG.** Subscribing gets the
same code the clone gets, but enabling it changes the rig's mod set — and the
rig's baselines are measured against a known set (`STATE.md` gates: pack
`75/75` + opt-in `8/8`, SKIP set BY NAME, load order `1:TestKit 2:FixPack
3:OptInPack`, `EF-054`). A third mod invalidates those readings and, worse,
would wrap or be wrapped by our modules mid-release. **The clone gives you
everything this leg needs; the subscription gives you a confound.**

⭐ Their set as of 2026-08-16: 15 modules, `Code/smrcf_restore_*.lua` plus a
core, matching the portal listing exactly — no hidden extras. If the count has
changed since, re-do the comparison in §3 before trusting it.

## 1. What this is

`fredware`'s **SMR Community Fixes** (Paradox Mods id 153410, GitHub
`SMR-community/smr-community-fixes`) ships **15** toggleable fixes for the same
game we patch. A description-level comparison against our 103 F / 12 D / 48 C
rows was done 2026-08-16 and is recorded below. **Eight overlap us. Seven do
not, and those seven are this leg's whole subject.**

⚠️ **The comparison was TITLE-TO-TITLE, not verified.** Their store text is
marketing copy. A "gap" below may turn out to be something we already cover
under a different framing, or not a real defect at all. **Each lead is a
question, not a finding.** Rejecting one with a written reason is a full,
successful outcome for that item.

## 2. The method — owner's framing, 2026-08-16

> *"The only thing I am proposing is we look at his fixes, compare it to game
> code, and determine ourselves if it's a bug we missed."*

That is the whole method, and it is the ordinary one: **their mod is a list of
claims about Paradox's code; we adjudicate each claim against Paradox's code.**
A defect's existence and location are facts about the game, not anyone's
property, so reading their repo to find out *where to look* raises nothing.
**The verdict must be ours** — reached from the shipped tree, the same way every
other entry in `agent/bugs/` was reached.

Two working rules follow from our own standards, not from a legal reading:

- **Derive from `ModTools/Src`, verified against `Packs\Lua.fpk`**
  (`FIX_POLICY` §8). This is not a special rule for this leg — a fix we could
  not derive ourselves could not be written up honestly in an entry, and would
  carry assumptions we never checked. If a lead cannot be reached from vanilla
  alone, that is a finding to report.
- ⭐ **Credit prior art.** If we ever ship a fix for a defect their mod
  identified first, say so — the treatment `FIX_POLICY` §8 already gives
  ChoGGi.

⚠️ One fact worth knowing rather than acting on: **their repo has no LICENSE
file.** It does not affect the method above. It would only matter if someone
proposed lifting their implementation, which nobody has — and if it ever comes
up, it is an OWNER question, not yours. ⭐ The cheaper route is to ask the
author directly; the org is named `SMR-community` and a missing licence is more
often an oversight than a stance.

## 3. The seven leads

**Five have NO entry anywhere in our corpus** (swept 2026-08-16: zero hits in
`agent/bugs/INDEX.md` for each keyword):

| # | Their name | Their one-liner | Our state |
|---|---|---|---|
| 4 | Repair Mod Manager Browser | mod thumbnails/screenshots; description formatting — HTML/Steam markup, Unicode, emoji, clickable links | nothing |
| 7 | Restore Soil Overlay | keeps the soil overlay tied to the surface map when another map is active | nothing filed — ⭐ **but see below** |
| 9 | Restore SpaceY Description | SpaceY's missing +20 max Drone Hub capacity in its description | nothing |
| 13 | Restore Localized UI Text | official translations for the terraforming heading + Universal Rocket action | nothing (`F98` is adjacent but is OUR defect about a re-used translation id) |
| 15 | Restore Clustered Lights | night lights on in one step so fast day↔night transitions do not trip the clustered-light assertion | nothing |

⭐ **Lead 7 has an owner sighting already.** `STATE.md` carries an unfiled rider
from the 2026-08-14 combined sitting: *"a vanilla stale landscaping overlay
(owner lead)"*. **Start here** — it may be the same defect, observed by the
owner and never written up, which would make it ours independently of their
mod. Check the sitting's logs (`archive/cs_*`) before anything else.

**Two we already know about and never built:**

| # | Their name | Ours |
|---|---|---|
| 10 | Restore Jumbo Cave Reinforcements | **C25** `cand` — "Jumbo Cave reinforcements stuck on unreachable waste rock". Our rider is *unrun*: we were waiting for a stuck site to appear organically. They shipped something. |
| 12 | Restore Asteroid Lander Cargo Safety | **C35** `cand` — "Edit Payload confirmed while units are on the cargo ramp tears down the rocket's command-centre connection with no wait" |

**Already covered — do NOT re-investigate:** 1 → `F78`+`F89`+`F81` · 2 → `F81` ·
3 → `F01` · 5 → `Fix_DustDevilSpawnGate`+`Fix_DustDevilsDescrMap` · 6 → `F94` ·
8 → `F92` · 11 → `F74` · 14 → `F64`+`F91`+`90_SaveSanitizer`.

## 4. Per-lead procedure

Run the same five steps on each. **Do them one lead at a time and update the
todo list after each** — the owner reads that list to decide when to step in.

1. **Re-check our corpus properly.** The sweep was keyword-based. Search the
   entry bodies, not just the index, and the module headers in `Code/`. A lead
   that turns out covered is closed with a pointer, no entry.
2. **Locate the defect in vanilla** — `ModTools/Src`, by symbol, not by
   citation inherited from anywhere. Name the function/data field and the
   lines. If you cannot find it, say so; do not assume it exists because
   another mod claims it.
3. **Decide whether it is a defect at all** under `FIX_POLICY` §4's
   intent-first bar (a self-contradiction, a dead branch, a stated intent the
   code misses) — versus a design choice someone dislikes. `C47`'s "unset field
   is not a self-contradiction" reasoning is the worked example.
4. **Check the player route.** Twice-learned here (`F85`, `idQuickSave`): a
   mechanism in source is not a player experience. If no player can reach it,
   it is `P3`/LATENT at best.
5. **File or reject, in writing.** New entry in `agent/bugs/` per
   `WORKFLOW.md`, with evidence tier stated honestly and ⛔ **no fix proposed**
   — or a rejection recorded on the same page with the reason. Regenerate the
   index the tool's way, never by hand.

## 5. What "done" looks like

- Up to 7 new `agent/bugs/` entries or written rejections, each SOURCE-VERIFIED
  or explicitly marked as not reachable.
- One `STATE.md` line (it is at its 60-line cap — extend an existing line).
- A checklist entry ONLY if something needs an owner call.
- ⛔ Zero changes under `Code/`. ⛔ Zero player-facing text.
- `python tools/doccheck.py` GREEN before commit.

## 6. ⚠️ The thing to say to the owner before anyone builds

**The ship line is FROZEN pre-release** (owner ruling 08-12, checklist 14:
`fixed` + suite + self-checks + verified save-safety IS the bar), and the only
step left is ④ upload. **Adding five to seven modules is not a small
addition** — each needs source verification, an entry, a probe, a save-safety
pass under `FIX_POLICY` §3a, a suite re-measure, and card + site + `metadata.lua`
updates. That is a release-delaying body of work, not a tidy-up.

⇒ **Recommend to the owner: investigate now (records only, cheap, no code),
build after launch.** "One mod fixes all" survives as the trajectory without
holding the release, and post-launch each lead can be un-parked one at a time
the way every other family in this project is. **The owner decides; this
paragraph exists so nobody quietly starts building.**

⚖️ **And before ANY filed lead becomes code, a fresh-context QA reviews the
batch** (house rule: heavy investigation gets an adversarial read before
implementation). That QA is not this leg's job — note it in the close-out so
whoever builds knows the gate exists.

## 7. ♻️ Close-out — how this file disappears

Do all of it in ONE commit:

1. **Integrate.** Findings live in `agent/bugs/` entries, not here. Anything
   reusable about the GAME goes to a new `agent/facts/EF-###.md` (regenerate
   the index with the tool, never by hand). Anything needing an owner call goes
   to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you" — never only in
   agent docs.
2. **Extend one `STATE.md` line** (it is at its 60-line cap): what was swept,
   what was filed, what was rejected and why, and that no code was written.
3. **Delete this file.** `git rm docs/agent/prompts/COVERAGE_SWEEP_SMRCF.md` in
   the same commit. The close-out message must name the grave —
   `git show <sha>:docs/agent/prompts/COVERAGE_SWEEP_SMRCF.md` — so the full
   brief stays recoverable at zero cost.
4. **`python tools/doccheck.py` GREEN**, then commit and push (pushing is
   standing-allowed).

⚠️ **If you cannot finish all seven leads in one session**, do not leave this
file half-worked. Self-split at a clean commit boundary: file what is done,
rewrite this brief to contain ONLY the remaining leads plus what the finished
ones concluded, and commit that as the continuation. A shrinking file is
progress; a stale file with a mental note is not.

⛔ **The reference clone (`C:\Dev\_ref\smr-community-fixes`) is not ours to
maintain.** Do not commit it, do not reference its path in any shipped doc, and
say in the close-out whether you deleted it or left it.
