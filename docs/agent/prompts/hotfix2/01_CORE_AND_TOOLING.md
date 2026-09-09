# 01 · Core and tooling — the spec every later link runs against

Chain: `prompts/hotfix2/README.md` (read its binding rules first — they are
yours, not background). You are FIRST. Links 02, 03 and 04 all consume what you
build here, so a wrong call here poisons the rest of the chain. Take the time.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents` (several smr-bugfixpack
sessions edit this tree; message any peer in your lane). Staleness anchor:
`033a9ae`. Build a todo list covering all four jobs before you touch anything,
one item per commit-and-verify unit.

**Read path:** `agent/STATE.md` · `agent/reports/VANILLA_FIX_QA.md` §0 ·
`agent/reports/PACK_1_1_0_REVERIFICATION.md` §4 (the whole section — it is the
design you are implementing) · `agent/FIX_POLICY.md` §1.4b and §2 ·
`Code/00_Core.lua` `:99-165` (`Require`) and `:266+` (`DataPatch`) ·
`tools/harvest_wrap_targets.py` (the harvest logic you are reusing) ·
`docs/PLAYTEST_CHECKLIST.md` item 116 (the owner's acceptance) and item 118.

## 1 · Job A — the `probe` form in `Require`

Report §4 item 1. `Require` already has `{ test = fn, reason = ... }`, and a
probe is a *specialisation* of it with three properties `test` does not have.
Add `{ probe = fn, reason = ... }`:

1. **It is error-trapped.** `c.test()` is called UNPROTECTED today
   (`00_Core.lua:120`). A probe's job is to call a real game function on a stub,
   and a throw is a legitimate answer — on 1.1.0, `LandscapeForEachUnit(stub, cb)`
   indexes `map.Landscapes` on a non-map and raises. Wrap the call in `pcall`.
   **A throw is a DECLINE, never a propagated error.**
2. **It fails CLOSED.** Three outcomes, and only one of them patches: the probe
   captured the 1.0.7 shape ⇒ apply; it captured anything else ⇒ decline; it
   threw, returned nil, or captured nothing ⇒ **decline**. "Nothing captured" is
   UNKNOWN, and UNKNOWN is not permission (QA §0.3 — `AddDomeColonistsModifier`
   returns silently when the stub's `GetPropertyMetadata` is nil, and reading
   that silence as "1.0.7" is exactly the bug F-1 is about).
3. **Its stub contract is written beside it.** Every probe carries a comment
   naming what the stub must provide and why the target is safe to call on one.

⛔ **Only for targets verified synchronous and side-effect-free on a stub.** If
you cannot show that from the 1.1.0 body, the module does not get a probe — say
so and leave it to its existing check.

⚠️ Follow the existing semantics: a `test` failure deliberately does NOT set
`update_suspect` (a content check owns its own meaning, `:160-163`). A `probe`
failure behaves the same way — it is a verdict, not patch rot. And reason
strings are an interface preserved byte-for-byte; do not reword existing ones.

⛔ **`00_Core.lua` is the file every fix depends on and it is byte-identical to
shipped v5 today** (hotfix-1 audit, ck110). You are about to change that, which
is correct and ruled — but it means the diff must be exactly this feature and
nothing else. No tidying, no drive-by renames.

## 2 · Job B — the `SRC:` / `DEFECT:` header manifest

Report §4 item 2. Two machine-readable lines per module:

```lua
-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=<hash of the shipped body at pin time>
-- DEFECT: <the literal shipped expression this module corrects, as a regex>
```

Write the **spec** — exact grammar, where the lines sit in the header, how a
body is delimited for hashing (`tools/luafn.py` already extracts function
bodies; reuse it rather than inventing a second extractor), what a module with
no single target does, and what a `DataPatch` module puts in `DEFECT:`.

Then **apply it to the KEEP set only** (the 35 rows of §1d) — those are the
modules that survive and whose current 1.1.0 body is the correct new pin. ⛔ Do
NOT stamp the REMOVE set: link 02 deletes it. ⛔ Do NOT stamp the FIX set: links
03 and 04 change those bodies and stamp their own, and a hash pinned before the
edit would be a lie.

⚖️ **The rule this earns, and it is the point of the whole exercise** (report §4
item 3): a module that cannot state the shipped expression it corrects cannot be
re-verified and should not ship. Where a KEEP module cannot state one, do not
invent one — record it in your outbox as a named exception with the reason.

## 3 · Job C — `tools/bodycheck.py`

Walks the live 1.1.0 tree and reports, per module:

- `BODY-CHANGED` — the `SRC:` hash no longer matches the shipped body (class b:
  F114, F116, F-6, F-7, F-9).
- `DEFECT-GONE` — the `DEFECT:` expression no longer appears in the target
  (class d: "vanilla fixed it", 32 modules this audit, and **the bucket no
  instrument the project owns could see**).
- `TARGET-ABSENT` — the function is gone (class e; `Require` already covers it).
- `NO-MANIFEST` — the module declares neither line. Not an error yet; a count.

Model it on `sigcheck.py`'s CLI and output shape so the three tools read alike.
Exit non-zero on `BODY-CHANGED` or `DEFECT-GONE`; `NO-MANIFEST` is a count, not
a failure, until the whole pack is stamped.

⛔ **Write a falsifier for it before you trust it.** Point it at a module whose
body you know changed under us (`Fix_TrainCargoDumping` / F114 is the worked
example) and confirm it says `BODY-CHANGED`; point it at one of the 32 and
confirm `DEFECT-GONE`. A tool that returns GREEN on everything is
indistinguishable from a broken one — that is how F114 shipped past three
instruments.

## 4 · Job D — pin the branch-guard design (ck118), do not build a detector

The chain rule: every module that gains a 1.1.0 body must DECLINE on 1.0.7.
Link 04 will ask you how. Write the answer here, once, as a short section in
`FIX_POLICY.md`:

⛔ **Do not build a game-version detector.** It would be a label check, and this
project's own rule is check the thing, not its label — the rule that made the
F115 gate correct. It would also be unbuildable from the mod's own fields:
`lua_revision`, `ModMinLuaRevision` and `ModRequiredLuaRevision` are ALL 350453
on both branches (`EF-077`), which is precisely why nothing warns a 1.0.7 player.

✅ **The per-module `probe` IS the branch guard.** A probe that confirms the
1.1.0 body shape the module was written for necessarily declines on a 1.0.7
body, per module, with no version arithmetic anywhere. Say this in `FIX_POLICY`
so link 04 does not re-invent it and a future session does not "improve" it into
a version check.

## 5 · Scope fence

**In:** `Code/00_Core.lua` (the probe form only), `tools/bodycheck.py`, the
manifest spec + its application to the KEEP set, the `FIX_POLICY` section.
**Out:** every module in the FIX and REMOVE sets; `items.lua`; `metadata.lua`;
any store text; `sigcheck.py`/`logscan.py` extensions (link 05 owns those).
Found something interesting out of fence? **File it, do not fix it.**

## 6 · Stop conditions — permission, not failure

- A KEEP module's target cannot be delimited for hashing, or has no statable
  defect expression ⇒ record the exception, move on. Do not force it.
- The probe form would require changing `Require`'s existing control flow or any
  reason string ⇒ **STOP AND ASK.** `00_Core.lua` is not a file to improvise in.
- `bodycheck.py`'s falsifier does not fire ⇒ stop and fix the tool before
  stamping anything. A wrong pin is worse than no pin.
- Any doccheck WARN ⇒ verbatim into your summary.

## 7 · What may NOT be claimed

- ⛔ Not "the pack is now update-proof". You built an instrument for classes a,
  b, d and e. Class c (semantics moved under a wrapper) is still seen by nothing.
- ⛔ Not "the KEEP set is verified". You pinned hashes of bodies that the
  re-verification read; you did not re-read them. Say which.
- ⛔ No status moves. A tool run is not a test.
- ⛔ Not "probes are safe" in general — only for the targets whose synchronous,
  side-effect-free character you actually demonstrated.

## 8 · Close-out

Green gates (README rule 9) — including your own `bodycheck.py` and its
falsifier. Then: append your outbox to `02`, `03`, `04` and `99`'s
`## Notes from upstream` (04 especially needs Job D's answer verbatim), strike
your row in the README, `git rm` this file, commit it all together, push.

Your outbox must carry: the probe form's exact signature and semantics; the
manifest grammar; `bodycheck.py`'s CLI and what its falsifier proved; every KEEP
module you could NOT stamp and why; and anything you filed out of fence.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- The handoff (`prompts/HOTFIX_2_HANDOFF.md`, consumed) is the origin document;
  its §4 is your job description in the owner's framing.
- ⚠️ `metadata.lua`'s comment claiming "`PackVersion` renders
  version_major.version_minor.version" describes something that **does not exist
  anywhere in the 1.1.0 tree** (grep: zero hits). Treat inherited comments in
  that file as claims. Filed here rather than fixed — not your fence.
- `sigcheck.py` rated `Fix_TrackSalvageWipe` OK both before and after F116's
  defect was found (from `smr-bugfixpack-a5`, which ran that leg). Your
  `bodycheck.py` is the instrument that should have caught it; use F116 as a
  second falsifier if the body pin makes that possible.
