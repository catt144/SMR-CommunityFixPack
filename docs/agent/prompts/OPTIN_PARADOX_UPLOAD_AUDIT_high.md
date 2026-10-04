# Audit — why the Opt-In mod's first Paradox upload fails where the fix pack's succeed

**Authority.** Owner, 2026-10-04: *"I want an audit before we do anything else, and a fix pack
agent is going to run it."* No further upload of the Opt-In mod is attempted until this audit
reports. The fix pack has 15+ successful uploads; its route is the reference.
Authored at fix pack `30dacada`, Opt-In `26d795d`. Start: `git log --oneline -5`, `git pull`
and `git status --short` in **both** `B:\Dev\SMR\SMR-BugFixPack` and `B:\Dev\SMR\SMR-OptInPack`.

## Outcome

A report at `docs/agent/reports/OPTIN_PARADOX_UPLOAD_AUDIT_<date>.md` in this tree that gives:

1. **The cause**, or a short ranked list of candidates. Each candidate gets its evidence and a
   falsifier the owner can run in one upload attempt.
2. **Every difference** between the Opt-In's upload inputs and route and the fix pack's
   proven ones. Mark each difference harmless (with evidence), suspect or wrong. Cover
   `metadata.lua` field by field, the editor workflow, the package and the link/junction setup.
3. **The exact corrections** for the Opt-In's next attempt, each with its owner. The Opt-In
   session applies them; this audit does not.
4. **A capture method that works** if the next attempt still fails. The first one printed
   nothing (see evidence).

The verdict is "the next attempt is set up the same way as the fix pack's proven upload,
except for these listed differences". It is not "it will upload".

## Evidence (claims; clear each one with the stated check)

- **Two failures, both on the Paradox leg.** The dialog said "Upload failed: Unknown error".
  The log lines are in `%APPDATA%\Surviving Mars Relaunched\logs\MarsDebug.exe-20261004-00.19.10-*.log`
  and `...-00.32.43-*.log`: `Mod Relaunched Fix Pack: Opt-In Modules (id SMR_CommunityOptInPack, v1.00-000) was not uploaded! Error: table: ...`.
  Check with `Select-String 'was not uploaded'` on both logs.
- **Each pack logged `blkPageCompress.cpp(35): ASSERT(!m_bPageChanged && !m_bHeaderChanged)`.**
  The first attempt logged it twice and the second once. The owner saw them as dialogs and
  pressed Ignore.
- **No listing exists.** The owner checked Paradox Mods and found nothing. The version stayed
  at 1.00-000. This is the mod's first publish: it has no `pdx_id`. The fix pack's uploads
  are updates to `pdx_id` 156049. Its first publish is recorded in
  `docs/agent/reports/RELEASE_PORTAL_PREP.md` and `V10_RELEASE_RECORD.md`.
- **The upload source.** The first attempt packed the Opt-In working repo, because the Mods
  junction still pointed there. The second packed the launch tree
  `B:\Dev\SMR\SMR-OptInPack-launch` (batch `2026-10-04-01`).
  `python tools/pack_list.py "%TEMP%\Surviving Mars Relaunched\ModUpload\Pack\ModContent.fpk" --tree B:\Dev\SMR\SMR-OptInPack-launch`
  was run in the Opt-In repo. It reported 75/75 files, all byte-identical, EXACT MATCH, with
  the package at 22,606,788 B. The package may since have been rebuilt or deleted, so re-run
  it only if it is still there.
- **Package size is ruled out** (owner: mods around 150 MB packed exist in the wild). Don't spend
  effort on it.
- **The capture attempt printed nothing.** Before the second attempt, a console wrapper was
  meant to replace the globals `AsyncPdxGetModDetails`, `AsyncPdxSetupModForPublish`,
  `AsyncPdxUploadModAsset`, `AsyncPdxUploadModContent`, `AsyncPdxPublishMod` and
  `AsyncPublishNewModVersion` with versions that print `[PDXDBG]`. No `[PDXDBG]` line appears
  in the 00.32.43 log. Settle whether the paste failed to run or the upload code holds local
  references the wrapper could not reach.
- **An earlier agent read the source** (archived 1.1.1.406343,
  `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.406343\Src`). Re-derive every line with `grep -n`
  before citing it:
  - `CommonLua/Libs/Paradox/ParadoxMods.lua` turns an empty SDK error string into
    "Unknown error".
  - `CommonLua/Classes/GedModEditor.lua` logs the dialog table, not the error.
  - Its candidates, all unverified: `RecommendedGameVersion` 350453 against the running
    build 406343, a long description of 6,212 characters, and a server rejection on the
    create step.
  - Not causes: login, missing fields and image sizes.
- **Rig.** DNS sinkholes Braze telemetry (`sdk.iad-01.braze.com` resolves to `::`), while
  `mods.paradoxplaza.com` and `login.paradoxinteractive.com` resolve normally. Decide
  whether this applied to the fix pack's successful uploads too.

## Scope and stops

In: read both trees, the archived source and the rig's logs, and write this report and its
records in this tree. Out: any upload, any edit to the Opt-In tree or its launch tree, and
any change to either mod's behaviour. Report findings about the Opt-In tree; don't fix them.

1. The cause needs a live upload attempt to separate the candidates: stop with the falsifier
   steps for the owner. Give about five steps at a time, starting with the capture method.
2. A difference needs an owner ruling (for example, changing the Opt-In's release procedure):
   file it on `B:\Dev\SMR\SMR-OptInPack\docs\PLAYTEST_CHECKLIST.md` and finish the rest.
3. The evidence can't settle a claim: state that limit and don't substitute a PASS.

## Close

Skills: `smr-orientation`, `doc-editing`, `smr-bug-library` (file an engine fact here if the
upload path yields one). House rules: `CLAUDE.md`, `docs/agent/WORKFLOW.md`. Run
`python tools/doccheck.py`, commit the report with a pathspec (peer hunks are in this tree),
`git rm` this brief and its row in `docs/agent/prompts/README.md` in the same commit, and push.
End with a short paste for the Opt-In orchestrator: the cause or candidates, the corrections
and the owner's next step.
