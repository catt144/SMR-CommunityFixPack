# FR-1 cache route, round 2 — the overlay worked; cover every RAYS record (one-shot, model-agnostic)

⛔ ONE-SHOT: consume this file (`git rm`) in your delivery commit. Written 2026-09-11 by `smr-bugfixpack-bd` (the orchestrator)
for **Astra** (the builder), after the owner's first bench of your `fr1-cache-probe-v1`. The records win if they disagree with
this brief. Verify every specific against `git log` and the tree; Codex sessions are invisible to `ListAgents`.

## 0 · Orient

`git pull` · `git log --oneline -10` · `git status --short` · `AGENTS.md` · `docs/agent/STATE.md` · `prompts/DISPATCH.md` §0–§3.
Open a **live todo list**, one item per task in §3, and update it immediately. Then read `reports/FR1_LINUX_FINDINGS_2026-09-10.md` **§10**
(this bench, recorded by the orchestrator) and your own `reports/FR1_CACHE_ROUTE_2026-09-11.md`.

## 1 · What your bench showed (MEASURED; evidence `C:\Dev\fr1-cache\fr1-cache\`, outside git)

The owner's first attempt used the markers `-fr1-cache-control` / `-fr1-cache-noop` (a dash, not `=`). Your probe logged `DECLINED`
and both legs ran untreated: menu reached, then the usual world-load crash on `38121decbc3eee12`. **The fail-closed gate worked.**
Second attempt, with the markers exactly right:

- **C1 (`control`)**: `ARMED Control` → `MOUNT_HELPER_OK` → `RELOAD_REQUESTED`; crash during boot, before the menu. The faulting
  thread's last dump is `271ec9634b1ab87b` (RAYS hyp+imp), 1 ms before the fault. That matches legs D/E, so the control reproduces them.
- **N1 (`noop`)**: `ARMED Noop` → `MOUNT_HELPER_OK` → `EXPECTED_DXIL_SHA256=516fc383…` → `RELOAD_REQUESTED`. **Your classifier
  matched the no-op DXIL in the dump** (`4f866e2c54fc9064.dxil`, sha256 `516fc3836f468850…`). So the directory overlay **won precedence
  and was consumed**; the priority risk you flagged did not bite. The game got past the stage that killed C1/D/E and built 260
  DXIL (C1: 123), including **REFLECT_FULL tile 16** (`c2aacc1919769303`, compiled fine on 580). It reached a pre-menu
  loading screen, hung several seconds, then faulted at the same NVVM site (`glvkspirv +0x157c88`) ~11 s after `RELOAD_REQUESTED`,
  still during the boot rebuild (no `ChangingMap` / LoadBinAssets yet).
- **The N1 faulting thread's last dump is `a26e0bbfe7751fbf`**: compute, cs_6_6, found in cache record `5519638363063710019`.
  `index.txt` names it **`Reflections.fx|USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS`**. It is a
  **debug** ray-queue build, absent from every earlier dump (A/B/D/E, the original dump run, C1).

## 2 · The gap (MEASURED desk, orchestrator)

`index.txt` `[k]` lines map `source|defines` → record key; that is the lookup your round 1 inferred. Filtering them for `Reflections.fx`
gives **54 records: 18 are REFLECT_RAYS; v1 covered 6.** The 12 missing are all `REFLECTION_DEBUG` builds:

```
17479759258806230241  REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
17686588521427011389  REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS
5865436634895424654   REFLECTION_DEBUG|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
5264869319203293582   REFLECTION_DEBUG|REFLECT_RAYS
8351999411133342628   TRACE_HIZ|REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
15937229215661096578  TRACE_HIZ|REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS
3797980553980650970   TRACE_HIZ|REFLECTION_DEBUG|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
8856374337229483367   TRACE_HIZ|REFLECTION_DEBUG|REFLECT_RAYS
15946777675723054662  USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
5519638363063710019   USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS   <- N1's crasher
17265521352967436427  USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECT_IMPORTANCE_SAMPLE|REFLECT_RAYS
9992072750089484426   USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECT_RAYS
```

`a26e`'s RTS0 (536 B) is **byte-identical** to the original default RAYS root signature (sha256 prefix `3ff5c9b85551833d`), so your
no-op DXBC should fit it. Its PSV0 differs (380 vs 452 B). The other 11 records are unchecked. Re-derive this list yourself;
the orchestrator's filter is a claim too.

## 3 · Tasks — leads, not a plan

1. **Probe v2 covering every REFLECT_RAYS record the index names** (18 by the count above, both `Control/` and `Noop/`), built the
   way round 1 was: preserve each record's metadata, validate each replacement, re-run the harness. Decide whether any
   REFLECT_FULL or other `Reflections.fx` records need touching (FULL tile 16 compiled fine in N1).
2. **Look past Reflections.fx.** The boot rebuild after a forced reload builds far more than a normal world load does (N1 built 260
   DXIL). Are there other ray-queue-style or loop-heavy compute programs in the cache that 580 might reject next? Can you tell, from
   the corpus or the vkd3d-proton #2701 history, what NVVM chokes on? A way to predict the next crasher beats finding it one bench at a time.
3. **Is the forced reload even needed?** If a mount made at mod load is read by the normal world-load pipeline creation *without*
   `ForceShaderCacheReload`, the boot mass rebuild (and its debug variants) disappears. Consider a `noop-noreload` treatment as its own leg,
   so the bench can answer that.
4. **Owner ergonomics.** The marker was mistyped twice in three sessions (`--fr1-options`, `-fr1-cache-noop`). Keep fail-closed, but
   make a mistyped marker impossible to miss: a clear log line naming the exact accepted strings, and copy-paste blocks in the steps. And/or
   a cheap first-screen witness: C1 must crash during the slides; if it reaches the menu, the marker didn't land.
5. Anything we're missing. Take a better route if you find one, and say why.

## 4 · Deliverables and bindings

- An addendum or new section in your cache-route report: verdict first, numbered claims graded MEASURED/SOURCE/INFERRED/NEVER RUN,
  and a "not opened" list. Put the probe v2 zip outside git, with a receipt JSON in `docs/archive/`.
- Plain-words owner steps in **checklist 145**, replacing the v1 steps, with **copy-paste launch lines** and the expected result per leg
  stated in advance.
- The same bindings as round 1: no game-dir, pack or archive writes; no game launch; no Mod Editor or portal; nothing into `Code/`; the scope
  decision (pack / opt-in mod / instructions) is the owner's. Commit by explicit pathspec with doccheck GREEN; push. The owner's
  standing rule: **the orchestrator reads and briefs, Astra builds.**
