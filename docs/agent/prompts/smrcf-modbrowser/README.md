# Chain C — `smrcf-modbrowser` · `C52`, standalone because it is complex

Three defects on one path, one of them needing a **§1.5 full replacement** and
one of them a **re-enable that may reinstate the fault it was working around**.
Map: `agent/prompts/SMRCF_CHAIN_SET.md`. ⛔ **Gated on chain A.**

## Manifest

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_SPEC_fable.md` | top tier | **decision routed** | re-derives all three; decides what may be built; routes the §1.5 call |
| 02 | `02_BUILD_opus.md` | volume tier | no | builds only what 01 approved |
| 03 | `03_SITTING_owner.md` | volume tier | **YES — ~15 min** | the browser on screen; the only place these are observable |
| 04 | `04_AUDIT_fable.md` | top tier | no | adversarial backward QA; empties the folder |

⚠️ Top tier on 2 of 4 is at `CHAIN_METHOD` §4.0's ceiling — justified here because
the spec makes a call that poisons everything downstream if wrong. **The owner may
re-route; bodies are model-neutral.**

## The three defects

**1 — screenshots can never download.** `WaitDownloadModScreenshots`
(`ParadoxMods.lua:213-276`) declares `local mod_prefix` inside `if thumbnailUrl
then` (`:222`), closes that block at `:245`, then reads `mod_prefix` at `:257` —
a global read, therefore `nil`, therefore *"attempt to concatenate a nil value"*
on the first image, every time. The developers' own `-- todo: this is not
working` sits at `:247`, and again at `ModManager.lua:786`. **§4 tell 5.**
⛔ The bug is *inside* the function, so a wrapper cannot reach it — **this is a
§1.5 full replacement**, the pack's patch-rot exposure category, and 01 decides
whether that is acceptable.
⛔ **Gated on chain A job 2**: `AsyncPopsDownloadFile` (`:260`) has zero
definitions in all of Src. If it does not exist at runtime, repairing the concat
moves the failure one line down and the fix is pointless.

**2 — description hyperlinks are disabled.** `HTMLParser`'s `A` branch returns
inert `label [URL]` with the clickable form commented out at `:118`. **Two
tells**: `GetRGBA(self.HyperlinkColor)` at `:109` is consumed by nothing (§4 tell
2), and `MarkdownParser.lua:49` ships the identical line **live** (§4 tell 3).
The consuming UI already handles `OpenUrl` (`ModsUIModDetails.lua:683`).
⛔⛔ **Deferred is not safe.** The line may have been commented out *because it
misbehaved* — fredware's own spec has a clause about XText's `<fallback_font>`
mode returning font id `-1` after a successful preflight. **The shape is
"re-enable and observe", never "uncomment it".**

**3 — the thumbnail cache never revalidates.** `:221-225` keys the cache on
`ModID` + `PreferredVersion` and skips the fetch `if not io.exists(file_path)`.
Replace a preview without bumping the version and existing players keep the old
image forever. **Weakest of the three** — no dev comment, no sibling, and
arguably a deliberate simplification. 01 decides whether it clears §4 at all.
⚠️ **Release-relevant to us either way**, and already on checklist item 34 as
awareness.

## ⚠️ What makes this chain hard, stated up front

1. **First-of-kind UI work** (shared with chain B): the pack has never patched
   Mod Manager internals.
2. **A §1.5 replacement** of a 63-line function — every game patch can silently
   diverge it. `WORKFLOW`'s fpk discipline exists for exactly this.
3. **Observation requires the live browser** — Paradox Mods reachable, a mod with
   screenshots, and eyes. `FIX_POLICY` §348-351: UI behaviour is the one class
   where source reading gives confident answers with **no validity**.
4. **A circularity worth noticing**: this is the screen players use to install
   *our* mod.
5. ⛔ **fredware's remedy is a feature reimplementation** — six spec clauses, its
   own HTML/BBCode formatter, a runtime-discovered private font cascade. **We are
   not doing that.** Minimal repair of located defects, or nothing.

## Binding chain rules

As `smrcf-verify/README.md` §"Binding chain rules", plus:

10. **`FIX_POLICY` §3a on every module**; a §1.5 replacement additionally carries
    a byte-verified target check and goes on the fpk re-verification list.
11. ⛔ **No behaviour beyond repair.** Restoring a disabled path is repair;
    adding formatting, fonts or caching policy is not.
12. **Nothing here is a release gate.** If it is not ready, it does not ship.

## Stop conditions

- Chain A found `AsyncPopsDownloadFile` absent → **defect 1 is not buildable.**
  Record it on `C52` and drop it; the other two may still proceed.
- The owner declines the §1.5 replacement → drop defect 1, build what is left.
- Re-enabling hyperlinks destabilises XText in any observed state → **revert and
  record.** The comment was a workaround and we have learned why.
