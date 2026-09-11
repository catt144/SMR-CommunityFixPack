# Handoff — end of the 2026-09-10 night session → the next session (model-agnostic)

⛔ ONE-SHOT: read this first; `git rm` it once every item below is done, routed to its home,
or restated in its own prompt. The records win if they disagree. Written by `smr-bugfixpack-f0`
at the owner's stop. **Verify every specific against `git log` + the tree** (Claude AND Codex
sessions commit here; Codex sessions are invisible to `ListAgents` — foreign uncommitted files
with no live Claude peer ⇒ ask the owner).

## 0 · Orient — and STOP there unless the owner asks for work

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `agent/STATE.md` ·
`prompts/DISPATCH.md` §0–§3. Open a **live todo list**, one item per numbered task below.
⛔ The owner corrected this session: a handoff pasted with no other instruction = **orient,
summarise, ask** — do not start executing items (memory: handoff-invocation-means-orient-first).

## 1 · FIRST (owner-named): walk the owner through Astra's FR-1 options report

> ✅ **DONE 2026-09-10 night (`smr-bugfixpack-bd`).** The owner was walked through it and chose **M1 + M2**. The results
> supersede the ranking below: M1 is DEAD on the desk, and M2's top treatment is `SSRFullTile8x8:1` (the AMD path).
> Probe **v3** (`fr1-options-probe-v3.zip`) replaces v1 (which had a `%`/printf defect) and v2. v3 adds the owner's
> set-then-reload combination (Leg D). Evidence: `reports/FR1_LINUX_FINDINGS_2026-09-10.md` §8.
> Owner legs A–E (B = switch alone, D = switch + reload): checklist 145, "M1 + M2 bench". Read the returned dumps with
> `C:\Dev\SMR-FR1-Options-2026-09-10\variant-map\classify_dump.py`. §2's two asks, answered 09-11: POSTED; no dev response yet (FINDINGS §9).

**`agent/reports/FR1_OPTIONS_2026-09-10.md`** (`fb7c247`; the owner calls it "Astra's report").
Read §0 (evidence keys), §1 (shader proof + the cache correction), §2 (mod reach), **§3 ranked
register**, §4 recipes R1–R7, §6 (not explored), §7 (scope). Then give the owner, in plain words:
- **The goal they set:** put out a fix if one exists (Paradox is slow), preferring **mod-side**:
  (1) a pure mod that stops the bad shader being built → (2) a mod-assisted saved setting →
  (3) a Steam launch option → then shader rewrite / driver / iGPU / rollback.
- **The ranked routes** (§3): M1 clear `ForceShaderCacheReload` before map load (`Dlc.lua:406-414`);
  M2 a hidden SSR selector (`SSRDenoiserMode` etc., values unknown); M3 persistent setting; L1
  `PROTON_DISABLE_NVAPI=1`; L2 vkd3d `force_static_cbv` / another Proton; M4 mod-shipped
  `Reflections.fx` (cached copy may win); P1 pyroveil with the new hash (strongest precedent);
  P2 exact-hash `VKD3D_SHADER_OVERRIDE`; P4–P9 driver/iGPU/rollback/other routes; U1–U3 upstream;
  X1–X7 ruled out with reasons. **All NEVER RUN.**
- **The recommended next bench (checklist 145):** R1 — the read-only settings inventory on the
  Windows rig first (Astra's probe lives outside git at `C:\Dev\SMR-FR1-Options-2026-09-10\`;
  it changes nothing without a test marker; 7 desk checks passed; never run in-game), then R2 one
  hidden switch at a time on the laptop at 580, then the launch options (R5), then pyroveil/override
  (R6/R7). ⭐ An exact-hash override (R7) is ALSO the formal attribution proof.
- **Superseded in that report (read FINDINGS §7):** its "attribution remains a STRONG INFERENCE" —
  the dump run's Proton log shows thread **025c** dump `38121decbc3eee12` at 7537.824/.829 and fault
  at 7537.831 with only msvcrt noise between = direct log evidence. Override proof still owed.
- **One cheap owner run (checklist 145):** Reflections **Off** + `VKD3D_SHADER_DUMP_PATH`, New Game —
  the dump run was Low OR Off (owner), so "built while SSR is disabled" is not yet measured.
- **Scope (ck145, owner's):** fix pack vs separate opt-in mod vs player instructions. `FIX_POLICY` §1:
  a driver workaround is not a shipped-Lua defect ⇒ needs the owner's ruling. Never decide it.
Then route the owner's choices: checklist 145 (decisions), a bench prompt if they pick a sitting.

## 2 · Where things stand (verify, don't inherit)

- **v7 LIVE on both stores** and fully closed out (`6dd98d2`, `98647a1`): writeback with comments,
  outbox cleared, owner receipt (pages pasted for formatting; Steam shows no version number).
- **FR-1:** `reports/FR1_LINUX_FINDINGS_2026-09-10.md` (§1 bench matrix, §6 Astra's correction, §7
  same-thread attribution); owner's reports verbatim `FR1_LINUX_BENCH_REPORT_2026-09-10.md`; EF-088
  (shader byte-identity + it IS in `ShaderCached3d12.fpk`), EF-089 (mods run after renderer init,
  before world load). Film grain + `VK_NV_raw_access_chains` REFUTED with the condition sampled.
- **Developer reply:** `reports/FR1_DEV_REPLY_2026-09-10.md` — the owner said they would post it in
  the Steam discussion a Paradox dev tracks. **Ask: posted? any dev response?** Record the answer in
  the FINDINGS file. Files offered to the dev: `C:\Dev\SMR-FR1-DevPackage.zip` (redacted, SHA256SUMS).
  A public link to it is the owner's call. The vkd3d/pyroveil draft is Astra's report §5.1 (unposted).

## 3 · Outside git (never commit; never edit the evidence)

`C:\Dev\SMR-FR1-Evidence\` (168 MB: both bench sets, 243-shader dump, full Proton log, extracted
1.1.0 shaders, `tools/spvscan.py`, film-grain test mod) · `C:\Dev\SMR-FR1-DevPackage\` + `.zip` ·
`C:\Dev\SMR-FR1-Options-2026-09-10\` (Astra: rebuilds, dxc, cache extract, probe, pyroveil JSON) ·
`C:\Dev\SMR-FR1Test\` + `.zip` (diagnostic only; never ships).

## 4 · Owner items (checklist)

145 (FR-1 bench + scope, above) · 144 (a) the owed v6 checks on a v7 boot; (b) the Steam sounds
thread — a "still checking" follow-up is drafted in `reports/FIELD_REPORT_REPLIES.md` · 142/135/F60 minor.

## 5 · Loose ends (homed)

- STATE's desk NEXT after FR-1: `prompts/DLC_DEEP_CHECK.md` (bounded, owner framing in its banner).
- `FIELD_REPORT_REPLIES.md`: Hydroponic Farm stub (design question, owner's) and Metatron `End1..7`
  particles (fixable, untimed). The two C74 sound leads are CLOSED (`b7e7cbb`).
- Unexplained, verbatim, attribution only if asked: `Failed activating D3D12 Dred`; the
  `OptionsData.Options.Antialiasing` / duplicate `hr.ResolutionUpscale` warning (FR-1 bench logs);
  `Missing spot 'Top' in 'ElectricityGridElement' state 'idle'` (SESSION_LOG 09-10 lookback).

## 6 · Practice learned this session (also in memory + the SESSION_LOG lookback)

- A negative byte search over a compressed/packed container proves nothing — decode first (my
  cache-absence claim was refuted by Astra, EF-088).
- Zips for Linux: build with Python `zipfile` (PS 5.1 `Compress-Archive` stores backslash paths).
- In `PROTON_LOG`, the thread-id column attributes a pipeline fault where timestamps cannot.
- Say conditional verdicts with their condition ("no KNOWN setting reaches it"), or the owner
  hears "impossible".

## 7 · Close-out

Route results to their homes (checklist 145, FINDINGS, SESSION_LOG; STATE only if the kernel
changed). doccheck GREEN; `git commit -F <msg> -- <paths>`; push; `git rm` this file when §1–§5
are done or restated.
