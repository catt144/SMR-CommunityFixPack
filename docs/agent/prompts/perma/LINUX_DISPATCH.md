# Linux dispatch — FR-1 (Linux/Proton + NVIDIA 580 crash) and its temporary workaround mod (standing, model-agnostic)

Paste into a fresh Claude Code or Codex session whenever the owner brings **anything about FR-1**: a player report (works or doesn't),
a log excerpt, a reply from the Paradox dev, a game patch, or a request to change or retire the workaround mod. Written 2026-09-11 by
`smr-bugfixpack-5d` at the owner's ask ("get the linux issue off your plate entirely"). ♻️ **STANDING: never `git rm` this file.**
Update §1 in place when the situation changes, and retire the prompt only per §5. The records (FINDINGS, checklist 145) win if they
disagree with this file.

## 0 · Orient

`git pull` · `git log --oneline -10` · `git status --short` · `ListAgents` · `docs/agent/STATE.md` (mandatory) ·
`prompts/perma/DISPATCH.md` §1–§3 (bindings, judgment rules, filing). Open a **live todo list**, one item per task, updated
immediately. Then read, in this order:
1. `reports/FR1_LINUX_FINDINGS_2026-09-10.md` **§11–§12**: the measured record, the field reports and the field tally.
2. `PLAYTEST_CHECKLIST.md` item **145**: the owner-facing state.
3. `reports/FR1_DEV_REPLY_2026-09-10.md`: every post, and whether it was posted.
4. `UPLOAD_WORKFLOW.md` → "FR-1 temporary workaround mod": the store text as shipped.

Deeper only when a task needs it: FINDINGS §1–§10, `reports/FR1_CACHE_ROUTE_2026-09-11.md` §1–§8 (Astra's route, record format,
validation), `reports/FR1_OPTIONS_2026-09-10.md`, `EF-088` (the shader cache), `EF-089` (mod timing; no Proton detector).

## 1 · The situation in one screen (as of 2026-09-11; verify against FINDINGS)

- **The crash.** On NVIDIA driver 580 under Proton, the **first world load** (New Game or any save) crashes in NVIDIA's shader
  compiler (`libnvidia-glvkspirv.so.580.x +0x157c88`, `_nv014nvvm`). 1.1.0 is building its `Reflections.fx` **REFLECT_RAYS** compute
  pipelines at that moment, **even with Reflections Off**. Three distinct RAYS programs are measured faulting: `38121decbc3eee12`,
  `271ec9634b1ab87b`, `a26e0bbfe7751fbf`. Not affected: Windows, driver 595 (595.84 measured loading), Intel, AMD.
- **The mechanism (MEASURED).** At mod load, the engine helper `DlcMountFolder` overlays the game's shader cache, replacing all **18**
  REFLECT_RAYS cache records with a root-signature-matched **empty compute shader** (DXIL sha256 `516fc383…`; vkd3d dump name
  `4f866e2c54fc9064`). Normal loading reads the overlay with **no forced reload**. The first world load then builds all 54 Reflections
  records (18 stand-ins plus 36 FULL, which all compile on 580) and none later in the process. Removing the overlay brings the crash
  back.
- **The mod, LIVE since 2026-09-11.** `SMR_FR1TempWorkaround`, "TEMPORARY - Linux NVIDIA 580 Crash Workaround". Steam Workshop
  **3799500849** (public), Paradox Mods **158711**. It is **not in the fix pack and has no GitHub repo** (owner ruling, ck145).
  - **MASTER copy:** the owner's Windows Mods folder, `%APPDATA%\Surviving Mars Relaunched\Mods\SMR_FR1TempWorkaround`. It holds the
    listing ids and is at `version` 3 after the upload saves.
  - **Source copy** (outside git, synced from the master) plus tools: `C:\Dev\SMR-FR1-TempMod-2026-09-11\`.
- **What its code does.** It gates on PC + `d3d12` + NVIDIA vendor `4318` + exactly `LuaRevision` 403908 / `AssetsRevision` 33006.
  - If a gate fails, it logs `[FR1 Temp Workaround] INACTIVE: <why>`. A game update gives "…version has changed… Please uninstall
    it."
  - Otherwise it mounts `Mod/SMR_FR1TempWorkaround/Noop` → `ShaderCache` and logs `ACTIVE: 18 reflections shaders replaced …`. It also
    mounts with Reflections On, adding a `WARNING` line.
  - It never sets an engine variable, and it is `optional_mod`, so saves don't require it.
  - It **cannot detect Proton** (EF-089): a Windows NVIDIA player who enables it gets it too. The page says not to use it on Windows.
- **Evidence that it works.**
  - MEASURED (P1, FINDINGS §12): the packed mod, New Game, Reflections High: `packed from appdata`, `ACTIVE`, the stand-in dumped 18×,
    0 faults.
  - Owner-witnessed: the Workshop-delivered copy loads a world; a cold boot straight into a colony works; Reflections Low, High and
    Ultra all load. Visuals with Reflections On are **untested**, and the page says they will very likely look glitchy.
- **Field tally (owner-stated, 09-11).** 3 working (one on a 10xx card); **1 not working**: field report 1, a GTX 1070 on
  Manjaro/Wayland, driver 580.178.04, Proton Hotfix. The "PLAYER LOG REQUEST" was sent to that player and was **UNANSWERED** when
  this was written.
  - H1 (the Workshop copy is broken) is FALSIFIED.
  - H2 (a setup-specific different crashing shader) and H3 (the mod didn't activate) are open.
  - A working 10xx card makes a Pascal-wide cause unlikely.
- **Posts (the owner posts; no agent posts).** The original dev post and follow-up 1 are POSTED. "CURRENT DEV NOTE" (it replaces
  posts 2 and 3) and "PLAYER REPLY" are drafted in the dev-reply doc; whether they were posted is **unknown, so ask**. No dev
  response as of 09-11.

## 2 · Playbooks — pick the one that matches what the owner brought

**P1 · "It works for me."** Add it to the FIELD TALLY bullet in FINDINGS §12, with the card, driver, distro and Proton version if
given, marked player-stated. Nothing else.

**P2 · "It doesn't work."**
- (a) If there is no log yet, hand the owner the "PLAYER LOG REQUEST" block (in the dev-reply doc) to post. It has six plain steps,
  the dump path is `/tmp`, and one grep line prints the result.
- (b) When the pasted lines come back, read them:
  - **No `[FR1 Temp Workaround]` line:** the mod never loaded (not subscribed, not enabled, or no restart). Reply with the five steps
    from the store page.
  - **`INACTIVE: not an NVIDIA GPU`:** not this crash.
  - **`INACTIVE: the game version has changed …`:** a game update landed, so go to **P3**.
  - **Any other `INACTIVE`:** quote it and investigate.
  - **`ACTIVE …` plus a crash:** find the `Dumping blob to …/<hash>.spv` line nearest before `handle_syscall_fault code=c0000005`
    **on the same thread** (the third `:`-separated field of a Proton log line is the thread id). Then run
    `python C:\Dev\SMR-FR1-TempMod-2026-09-11\tools\identify_dump_names.py <hash>`, after its `--selftest`.
    - **A cached compute program, NOT replaced:** a new crasher on that setup. Record it (a FINDINGS bullet) and put the option to
      the owner in checklist 145: extend the overlay with a no-op for that record. The owner decides. It needs new root-matched
      records built and validated; Astra's `build_v2.py` / `cache_records.py` in `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\` did
      that. The owner's rule: the orchestrator briefs and Astra builds, unless the owner asks directly.
    - **NOT a cached compute program:** a graphics or runtime-compiled shader, for which no mod fix is known. Report it to the
      owner, and to the dev with the owner's OK.
  - **A crash with no fault line:** a different failure. Ask for the whole log through a file host.
- A player's words are claims; only their log lines are measured.

**P3 · A game patch lands** (Steam build ≠ 24995074, or the game ≠ 1.1.0.403908). The mod is inert on it by design. Find out, from
the owner or a Linux 580 tester, whether the patch fixes the crash **with the mod disabled**.
- **Fixed ⇒ retire the mod.**
  1. Draft a banner and change note: "Paradox fixed the crash in <version>; please unsubscribe."
  2. Edit the MASTER `metadata.lua` and the UPLOAD_WORKFLOW blocks together, and confirm they match word for word.
  3. The owner re-uploads, and may hide or unlist the item.
  4. Draft a thank-you post to the dev.
  5. Move §1 of this file into SESSION_LOG and retire this prompt (§5).
- **Not fixed ⇒ the mod no longer protects anyone.** This needs an urgent owner decision: rebuild the 18 records against the new
  cache (new keys and bytes) and update the revision gate.

**P4 · The Paradox dev replies.** Record the reply verbatim, with its date, in the dev-reply doc. Draft an answer in the same doc;
the owner posts it.

**P5 · Text or store-page changes.** Edit the MASTER `metadata.lua` (then re-sync the source copy) and the UPLOAD_WORKFLOW blocks
together. Verify the match: the description must equal the Paradox block once whitespace is normalised. Leave the code unchanged
unless the owner asks; the shipped code is the P1-tested bytes.

## 3 · Tools and evidence (outside git unless stated)

| what | where |
|---|---|
| desk harness (21 cases; Astra's mocks + the real `DlcMountFolder`) | `C:\Dev\SMR-FR1-TempMod-2026-09-11\tools\tempmod_harness.py` |
| dump name → shader (FNV-1 of the DXBC) | `…\tools\identify_dump_names.py` (`--selftest` first) |
| preview card generator | `…\tools\make_preview.py` |
| dump classifier (needs the `.dxil` files) | `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\classify_dump.py` |
| list or reconcile a `.fpk` (in the repo) | `tools/pack_list.py <fpk> --tree <mod folder>` |
| Steam item status (public API, read-only) | POST `https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/`, body `itemcount=1&publishedfileids[0]=3799500849` |

Evidence is read-only and never edited:
- `C:\Dev\SMR-FR1-Evidence\`: the original bench.
- `C:\Dev\fr1-mm-complete\`: legs A/B/D/E.
- `C:\Dev\fr1-cache\fr1-cache\`: C1/N1.
- `C:\Dev\Success\`: C2/Q2/R2 and `fr1-packed-proof`.
- `C:\Dev\SMR-FR1-CacheRoute-2026-09-10\` and `…-V2-2026-09-11\`: Astra's rounds.
- `C:\Dev\SMR-FR1-Options-2026-09-10\`.

## 4 · Bindings

- **The owner posts and uploads.** No agent posts, uploads or touches a portal API (H-03), and no agent opens the Mod Editor.
- **The mod lives outside git.** It never goes into `Code/` or the fix pack. The Windows Mods-folder copy is the master; re-sync the
  source copy from it after any owner upload.
- **Read-only:** the evidence folders. The game directory and the source archives are never modified (DISPATCH §1).
- **Say which kind of claim a line is:** MEASURED (a log or dump you read), owner-stated, player-stated, or INFERRED.
- **Scope decisions are the owner's:** extending the overlay, retiring the mod, or changing its behaviour. They go in checklist 145,
  never only here.
- **Where results go:** FINDINGS §12 (one bullet per field report, verbatim), checklist 145 (owner-facing), the dev-reply doc
  (posts), SESSION_LOG (the leg). Commit by explicit pathspec with doccheck GREEN, then push.

## 5 · Retiring this prompt

When Paradox's fix ships and the mod is retired (P3, "fixed"), or when the owner says so. Until then it is standing.
