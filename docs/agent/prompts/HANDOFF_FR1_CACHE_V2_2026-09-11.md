# Handoff — 2026-09-11, FR-1 cache-probe v2 bench → the next session (model-agnostic)

✅ **§1 DONE 09-11 (`smr-bugfixpack-5d`):** evidence `C:\Dev\Success\`; legs C2/Q2/R2 (Q2 loaded; F2 skipped); FINDINGS §11. §2 records
written (ck145 block, dev POST 2 drafted). **Still open:** the owner's answers (POST 1 posted? scope? the 01:47:24 launch), Astra round 3 if
productized, and §5. `git rm` this once those are answered or restated.

⛔ ONE-SHOT: read this first. `git rm` it once every item below is done, routed to its home, or restated in its own prompt.
The records win if they disagree. Written by `smr-bugfixpack-bd` at the owner's request ("get you on a fresh context before
you examine these"). **Verify every specific against `git log` and the tree:** Claude and Codex sessions both commit here, and
Codex (Astra) is invisible to `ListAgents`. It supersedes `HANDOFF_FR1_OPTIONS_2026-09-10.md` (consumed in this commit;
its open items are restated in §5).

## 0 · Orient, then do §1 (owner-named)

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `agent/STATE.md` · `prompts/DISPATCH.md` §0–§3.
Open a **live todo list**, one item per numbered task. The owner asked for §1 explicitly, so do it without re-asking. For anything
past §1, orient, summarise and ask (memory: handoff-invocation-means-orient-first).
**Owner rule (09-11): the orchestrator (you) reads, attributes, records and briefs; Astra builds.** Anything that needs Astra's probe or
tooling rebuilt goes back to Astra as a prompt (memory: orchestrator-hands-builds-to-astra).

## 1 · FIRST: read the owner's v2 bench evidence

**Where:** the owner is zipping `~/fr1-cache-v2` on the laptop and will give you a Windows path. The recipe is checklist
**145** (legs C2 / Q2 / F2 / R2); the probe is `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\fr1-cache-probe-v2.zip` (Astra, `9031634`).

**What the owner told this session, before the evidence was read (owner-stated, NOT yet measured):**
- A world loaded on NVIDIA 580: "I am in game". **Which leg is UNKNOWN**: Q2 (`-fr1-cache=noop-noreload`) or F2 (`-fr1-cache=noop`).
  Ask, and confirm from the log's `ARMED Noop reload=false|true` line.
- In that session the **Intel-made 1.1.0 save loaded** too (a second world load, same process).
- The owner's **Windows colony save** (synced to the laptop) loaded **"fully functional"**, with missing-mod warnings because it had
  TestKit + the fix pack ⇒ it ran as vanilla + the probe. The owner was told not to save it.
- C2's outcome and whether R2 ran are not yet reported.

**How to read it** (the tools exist; don't rebuild them):
- Per leg: in the Proton log, check `[FR1Cache v2]` lines: `ARMED <mode> reload=<bool> records=18`, `MOUNT_HELPER_OK`, then
  `RELOAD_REQUESTED` or `NO_RELOAD_REQUESTED`, and any `MARKER ERROR` (a typo applies nothing). Also the game log's `Command line:`.
- Treatment witness: the dump contains the no-op DXIL (the probe logs `EXPECTED_DXIL_SHA256`; v1's was `516fc383…`, so re-read v2's).
  Use Astra's `analysis/classify_dump.py <dumpdir> --log <steam-X.log>` from the v2 zip, which covers all 228 cached compute programs.
  Also `C:\Dev\SMR-FR1-Options-2026-09-10\variant-map\classify_dump.py` for the RAYS/FULL variant names.
- Faulting-thread attribution for any crash: the last `vkd3d_shader_dump_blob` on the faulting thread (FINDINGS §9 method).
- Expected shapes: **C2** crashes during the boot slides (the control). **Q2 / F2**: worlds load, no RAYS program built from original bytes.
  **R2** (no marker): the original crash returns. A Q2 success means normal world loading reads the overlay **without** the forced
  reload, which is the cleanest shipping shape. Report the unexplained lines verbatim (DISPATCH §2).
- Mind the precision rules: "loaded" is owner-witnessed; "used the stand-in" needs the dump; "reflections look equivalent to Off"
  has NOT been measured.

## 2 · Then record and route

- **FINDINGS §11** (`reports/FR1_LINUX_FINDINGS_2026-09-10.md`): leg table, witnesses, verdicts, graded as in §9–§10.
- **Checklist 145:** a plain-words result block above Astra's v2 steps.
- **Dev reply** (`reports/FR1_DEV_REPLY_2026-09-10.md`): "FOLLOW-UP POST 1" (the partial swap) is drafted; **ask whether it was
  posted**. If v2 proves the full swap, draft **FOLLOW-UP POST 2**: the swap makes the crash go away, plus the R2 reversal. The owner
  posts; the original post is POSTED, and there is no dev response yet as of 09-11.
- **Owner decision, now live (ck145):** does a working stand-in ship in the fix pack, as a separate opt-in mod, or as player
  instructions? `FIX_POLICY` §1: it's a driver workaround, not a shipped-Lua defect. The recommendation on record is a separate opt-in mod.
  Never decide it for the owner.
- **If the owner wants to productize, brief Astra** (round 3). Open questions to give it: what the overlay does on Windows / AMD if
  installed with Reflections ON; whether a mod can gate itself (no Proton detector exists, EF-089 / options report §2.3); what happens
  if a player turns Reflections on; packed-mod delivery (`ModContent.fpk`) vs this unpacked bench; and the STATE hazards (H-02/H-03/H-10)
  for anything that touches `metadata.lua` or a portal.

## 3 · Where FR-1 stands (verify)

`reports/FR1_LINUX_FINDINGS_2026-09-10.md` §6–§10 and `reports/FR1_CACHE_ROUTE_2026-09-11.md` §1–§8 hold it all. In short:
- The crash is NVIDIA 580's NVVM compiling a `Reflections.fx` **REFLECT_RAYS** (ray-queue) compute program. It happens at world load
  even with Reflections Off (measured, §9). Three RAYS programs have measured faults: `38121decbc3eee12`, `271ec9634b1ab87b`, `a26e0bbfe7751fbf`.
  REFLECT_FULL tile 16 compiled fine (§10). Same-thread attribution holds in every crashing run.
- Dead routes: M1 (on two counts), the `hr` SSR switches (bench-refuted), and the blank push alone (a boot crash).
- Live route: Astra's directory overlay via `DlcMountFolder`, replacing all **18** REFLECT_RAYS cache records with a root-matched
  no-op. v1 (6 records) was proven consumed; v2 (18 records) is §1.

## 4 · Outside git (never commit; never edit the evidence)

`C:\Dev\SMR-FR1-Evidence\` (original bench) · `C:\Dev\fr1-mm-complete\` (probe-v3 legs A/B/D/E) · `C:\Dev\fr1-cache\fr1-cache\`
(cache v1 legs C1/N1) · the v2 zip coming from the owner · `C:\Dev\SMR-FR1-Options-2026-09-10\` (Astra round 0 + `variant-map\`,
my probes v2/v3) · `C:\Dev\SMR-FR1-CacheRoute-2026-09-10\` (Astra v1) · `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\` (Astra v2) ·
`C:\Dev\SMR-FR1-DevPackage.zip` (redacted, offered to the dev).

## 5 · Carried from the consumed 09-10 handoff (still open)

- **ck144** (a) the owed v6 checks on a v7 boot (STATE "OWED" line); (b) the Steam sounds thread: a "still checking" follow-up is
  drafted in `reports/FIELD_REPORT_REPLIES.md`, to post only if the owner's reply said "still checking". · ck142 / 135 / F60 are minor.
- STATE's desk NEXT after FR-1: `prompts/DLC_DEEP_CHECK.md` (bounded; the owner's framing is in its banner).
- `FIELD_REPORT_REPLIES.md`: the Hydroponic Farm stub (a design question, the owner's) and Metatron `End1..7` particles (fixable, untimed).
- Unexplained, verbatim, attribute only if asked: `Failed activating D3D12 Dred`; the `OptionsData.Options.Antialiasing` / duplicate
  `hr.ResolutionUpscale` warning (FR-1 bench logs); `Missing spot 'Top' in 'ElectricityGridElement' state 'idle'`.
- Upstream drafts (options report §5.1 vkd3d/pyroveil, §5.2 Paradox) are unposted; the owner's call.

## 6 · Practice learned this session (also in memory and the SESSION_LOG lookback)

- **The dump is the witness, never the setter's readback.** `SSRFullTile8x8` read `CHANGED` and held, and it changed nothing (legs B/D).
- **Read the whole body of a function before routing through it.** I proposed the fake-DLC route while `Dlc.lua:410`
  (`UnmountByPath`) was on screen; Astra caught it.
- **Owner-typed markers fail**: `--fr1-options` and `-fr1-cache-noop` in two of three sittings. Give copy-paste blocks and a
  first-screen witness ("C must crash at the slides") stated in advance.
- **Grade "family" claims by count:** first two, then three RAYS programs measured, never "all" (Astra's precision note).

## 7 · Close-out

Route results to their homes (FINDINGS, checklist 145, dev reply, SESSION_LOG; STATE only if the kernel changed, ≤ its byte cap).
doccheck GREEN; `git commit -F <msg> -- <paths>`; push; `git rm` this file when §1–§5 are done or restated.
