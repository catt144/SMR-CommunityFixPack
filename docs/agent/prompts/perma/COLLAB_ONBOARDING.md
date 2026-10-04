# Collaborator onboarding — handoff and working prompt (temporary)

## Must_Read_Header
<!-- RULES -->
Rule: Close this prompt only when the owner says collaborator onboarding is closed. [A3: pass]
<!-- /RULES -->

Reader: a session the owner opens to bring fredware and James187 onto the Test Kit and the
fix-pack pipeline, or to troubleshoot a problem one of them hit. This file is both the handoff
and the working log. It is temporary: when the owner says onboarding is closed, `git rm` it and
delete its row in [`../README.md`](../README.md) in the same commit, after moving anything in
section 4 or 5 that is still owed to its durable home.

Authored 2026-10-04 at pack `1a6a5024`, kit `master` `b58ae18`. Start with `git pull` and
`git log --oneline -5` in both repos; every specific below is a claim to check once.

## 1 · The decision (owner, 2026-09-29) — settled, do not reopen

- The owner (catt144) is running a collaboration trial with two fellow modders, fredware and
  James187, who each maintain a bug-fix mod and work through coding agents (fredware: Codex and
  Claude Code; James187: mostly ChatGPT, some Claude).
- The aim is one owner per bug, so players who stack every fix mod stop getting two mods patching
  the same defect. Coordination first; shared code only through the pack's pipeline.
- The Test Kit is shared as the private repo `catt144/SMR-CommunityTestKit`. The pack, Opt-In Pack
  and Save Rescue repos are public.
- Merge and upload stay with the owner. A collaborator's instruction directs only that
  collaborator's own branch (`CLAUDE.md` header).
- The owner prefers a code-only trial (one fix each through the pipeline, shipped in the pack's
  normal release) over a new public mod. fredware proposed Paradox Mods as a test bed; the owner's
  conditions if that happens: only fixes that leave nothing in the save, an off-platform report
  route (Paradox Mods has no comments, `EF-067`), and no overlap with fixes the pack already ships.

## 2 · What is built

| piece | where | commit |
|---|---|---|
| Kit remote, MIT `LICENSE`, README "Install" and "Sharing this repo" | kit | `470ecbd`, `505d3d0` |
| `ONBOARDING.md` plus `CLAUDE.md` / `AGENTS.md` entry files | kit | `f30ba1b` |
| TestKit no longer local-only (WORKFLOW "Layout" and the other live docs, 10 files) | pack | `92e9418` |
| Authority rule names catt144 and scopes a collaborator's instruction | pack `CLAUDE.md` | `4517aa6` |
| `TESTKIT.md`: a probe with no verdict reports ERROR | pack | `a387818` |
| `aliascheck.py` reads the `SMRTest` constructor's fields (10 false rows gone) | pack | `19e774c` |

GitHub ruleset "Master" on the kit (owner-configured, 2026-09-29): pull request required, force
pushes and deletion blocked, merge commits only, repository admin bypasses. A direct push by the
owner's seat succeeds and prints `Changes must be made through a pull request`; that line is the
bypass notice, not a rejection. `gh` is not installed on this machine, so the ruleset, invitations
and pull requests cannot be read from here: ask the owner or have them paste what they see.

The collaborator's agent starts at the kit's `ONBOARDING.md`. Fix a wrong or missing instruction
there, not in a chat reply alone.

## 3 · The job

1. Use the todo tool before any write, one item per commit-and-verify unit.
2. When the owner relays a collaborator's problem (a message, a screenshot, a log), classify it
   before fixing: setup on their machine · the kit · a pack tool that assumes the owner's rig ·
   a rule or doc their agent misread · a real defect in a fix. Fix it in the repo that owns it and
   record it in section 5.
3. When the owner asks for a chat reply, write it for fredware, James187 and catt144's Steam group
   chat: casual, short, no internal ids. Lead the handover with the "Written for:" line.
4. Decide what you can within section 1. Ask the owner only for what is theirs: invitations,
   merges, uploads, rulings, and anything that changes what a collaborator may do.

In scope: onboarding, troubleshooting, the kit's collaborator docs, portability of pack tools a
collaborator needs. Out of scope: building fixes for bugs on a collaborator's list, any upload, and
the arming harness (`tools/arming/`), which stays bound to the owner's machine.

Kit commits: check `git -C ../SMR-BugFixPack-TestKit branch --show-current` first. The kit's working
tree is the folder the game loads and is often on a sitting branch with another lane's uncommitted
slots; commit collaborator docs to `master` through a separate worktree, never by switching that
tree. Skills: `doc-editing` before any document change, `subagents` before delegating.

Stops: a collaborator's push or pull request touches `master`, `Code/80_AgentSlots.lua` or an armed
`metadata.lua` line · a request would give a collaborator merge, upload or rules authority · a fix
needs a reading in the game on a collaborator's machine that no log can carry.

Claim limits: "it works on their machine" needs their log or output with the HEAD it ran on, not
the guide saying it should. Nothing below marked untested may be reported as working.

## 4 · Open items

- **Invitations.** Sending them is the owner's act (kit Settings → Collaborators). Whether they
  went out is unknown at authoring.
- **Untested on any machine but the owner's:** a fresh clone loading through a junction; the
  screenshot helper's fallback when `B:` does not exist (`Code/74_SMRTK_Agent.lua`); a published
  pack and a cloned pack enabled together (same mod id). The guide tells collaborators to
  unsubscribe; the first collaborator's run is the test.
- **Pack tools assume the owner's rig.** `tools/bodycheck.py` and `tools/sigcheck.py` hardcode
  `DEFAULT_SRC = A:\SteamLibrary\...\Project Spark\ModTools\Src` (both take `--src`). Not yet
  given an environment override.
- **Source archive parity.** Pins only agree across machines when everyone hashes the same archived
  game tree. Have each collaborator archive `ModTools\Src` for the current build and compare
  `MANIFEST.sha256` with `SMR-Shared\SMR-SrcArchive\<version>`; do not send the tree itself.
- **The pack-side route is not designed.** How a collaborator submits a fix to the pack (fork and
  pull request against the public repo, who runs doccheck, what the owner's review checks) has no
  written procedure. The hook is per-clone (`git config core.hooksPath tools/hooks`), so a
  collaborator's green is not evidence; the owner's seat reruns the gates on every pull request.
- **Trial bugs not chosen.** One each, disjoint modules, from their lists and not covered by the
  pack; a wrap or lighter (FIX_POLICY §1.1–§1.4), no game-time thread, log-demonstrable (Tier B/C).
- **Overlap list not verified.** From fredware's file names only (repo by `facazevedo`, interface
  `SMRCommunityFixes.lua`, one `smrcf_*` file per fix): Saint blessing, jumbo cave and track
  demolition look like `Fix_SaintBlessing`, `Fix_JumboCaveReinforcementWedge` and
  `Fix_TrackSalvageWipe`/`Fix_TrackSalvageRefund`. Their code has not been read; `bugs/C49.md` is
  the pack's earlier record of fredware's mod. Saint blessing is the one to raise first: vanilla
  fixed it in 1.1.0 and a second correction on top breaks blessings (F-1).
- **doccheck is left out of the collaborator's pull-request gates** in `ONBOARDING.md` §7, because
  it can go RED for pack-side reasons. The owner may want it back.
- **Branch protection on the pack repo** was not looked at; only the kit has a ruleset.

## 5 · Issue log

One block per problem, newest first: date · who · symptom · class (section 3) · cause · fix commit
or "open". This log is the trial's debrief; keep it even when the fix was one line.

_None yet._
