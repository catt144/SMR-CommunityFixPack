# Link 5 — terminal audit: break this chain, then rule on the launch

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.
📋 Read `README.md` in this folder first — its binding rules govern you.
⭐ **Fresh context, top tier, and you are the last session before the upload.**

⚖️ **Default to refusing.** If you cannot decide, the answer is *do not ship these
two*. Reverting them costs an hour; a bad first impression costs the mod's only
first impression. ⛔ **But refusing is not free either** — the owner ruled these
two into 1.0.0 precisely so this repo could be **closed** rather than trailing a
1.0.1. Say plainly which cost you are choosing.

## 0 · Read path

```
git log --oneline -25 && git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
python tools/pack_predict.py .
```

Every commit of this chain, **bodies included** · both modules, read as code, not
as briefs · `C50.md`, `C51.md`, `EF-039`, `EF-014`, `EF-054` · link 4's logs in
`docs/archive/` · `RELEASE_PORTAL_PREP.md` · the site's two new fix-list entries ·
checklist items **34, 56, 57**.

⭐ **Read the links' own reports LAST.** Form your view from the artifacts first.

## 1 · 🗒 Live todo list — one item per challenge

## 2 · The challenges

### C1 · Did either fix regress the thing it was warned about?

`C50` had a documented way to fail that looks like success: mutating the preset
drops the render context and silently damages the **first** bullet
(`localization.lua:224-227`). ⛔ **Prove from the log or the owner's reading that
bullet 1 still resolves its cargo number** — and if the sitting did not look,
that is a gap, not a pass. Then satisfy yourself the built module truly does not
touch `preset.effect`.

### C2 · Is the evidence what it claims to be?

Both entries should now carry attended status. Check the **provenance of every
status word**: who watched what, on which screen, in which language, in which
log. ⛔ `C51` is invisible in English — an attended claim for it that rests only
on an English pass is **false**, however honestly it was written.

### C3 · `H-10`, the hazard this chain was most likely to trip

Two new `Code/*.lua` files. ⛔ Verify **yourself** — not from a report — that both
appear in `items.lua` **and** in `metadata.lua`'s `code` list, same names, same
order, and that `pack_predict` shows **82** files with both present. A module
missing here **ships absent**, which is the exact defect that nearly shipped on
2026-08-17.

### C4 · Did anything move that was frozen?

⛔ `metadata.lua`'s `version` must still be `0`. ⛔ `C52` must still be `parked`.
⛔ No parked opt-in passage may have been restored (`H-07`). ⛔ No player surface
may name the other mod (`EF-054`). ⛔ Nothing may have been published.

### C5 · What did this chain never ask?

⛔ **The question with the best track record in this project.** Every defect that
got through in this repo's history came from *the brief never asked*, not from a
session doing its brief badly. Name it. ⚠️ If your answer is "nothing", say
instead which question you are least confident was covered, and why.

## 3 · The verdict, and the two things only you do

1. ⭐ **SHIP or REVERT**, in one sentence, first line of your report.
2. ⛔ **THE TAG.** `fixpack-v1.0.0` currently marks bytes measured in a running
   game (run B). This chain invalidated that. **If your verdict is ship, move the
   tag to your close-out commit** — as the previous terminal audit did under the
   same authority (`H-01`) — and say in the commit what gate it now stands on:
   **an attended sitting, not run B**, because the owner ruled the gate one-time
   (checklist 57). ⛔ If your verdict is revert, the tag does **not** move and you
   say exactly what must come out.
3. **Update `H-01` in STATE** so the next session inherits the truth about what
   the tag marks now.

## 4 · Scope fence

**IN:** breaking the chain's claims · re-deriving anything you doubt · fixing a
launch-blocking defect **you find** (say so in your first sentence) · the tag ·
the verdict.

**OUT:** ⛔ re-running the pre-launch sweep or run B — **the owner ruled that
one-time; asking for it again is overruling them, and if you truly believe it is
needed, that is a STOP AND ASK, not a unilateral demand** · ⛔ `C52` · ⛔ new
fixes beyond a blocker · ⛔ publishing · ⛔ the opt-in build (you hand it off, you
do not start it).

## 5 · ⛔ What you may not claim

- ⛔ **"I agree with the links."** Agreement needs its own evidence; say what you
  checked.
- ⛔ **"The mod is clean."** ⛔ **"Compatible with other mods"** — nothing here
  tested a foreign mod.
- ⛔ Any count you did not emit · any screen reading not in link 4's report · bare
  `tested`.
- ⚠️ ⛔ **Do not manufacture a finding to look useful.** *"It holds, here is what
  I tried"* is a complete answer.

## 6 · Close-out — and the handoff that ends this repo's active work

One commit: your ruling · the tag if it moves · `STATE.md` (`H-01`, the artifact
line, the queue) · checklist entry for the owner · `doccheck` GREEN · `git rm`
this file **and** this folder's `README.md` if the folder is otherwise empty ·
push.

**Owner report — short, first line is the product:**

1. ⭐ **SHIP** or **REVERT**, one sentence.
2. What you tried to break, and what happened to each challenge.
3. Your C5 answer.
4. ⭐ **The upload sitting, restated in the owner's terms:** re-tick the mods ·
   ⛔ `IsDirty()` false and **1.0.0** on screen before anything is pressed · pack
   via **Mods Manager → Edit → File → Pack Mod** (no console) · ⛔ **Paradox
   first** · then §0.5(d) game version 350453, §0.5(e) the id writeback commit,
   §0.5(f) the delivered-bytes check against **the md5 recorded at pack time**.
5. ⭐ **The kickoff line for the opt-in effort** — the owner's stated next
   priority (*"shift resources and start working on the opt in"*). ⛔ Do not scope
   it here; name the first thing it must read, which is that repo's own STATE and
   its standing pre-upload obligation
   (`reports/PARKED_OPTIN_REFERENCES.md`, ~46 parked passages).
6. ⚖️ **Was this chain worth its cost?** Five prompts for two text fixes is a
   ratio worth judging out loud, and you are the only session positioned to.

## Notes from upstream

- *(links 1–4 append here)*
