# 05 · Tools tail — make the next update a tool run, not a week

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Needs 01 only;
independent of 02, 03, 04 — run it whenever. Small, low-risk, and it lands in
**this** patch cycle rather than after it (owner acceptance, ck116).

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first.

**Read path:** `PACK_1_1_0_REVERIFICATION.md` §1c (the AUGMENT rows) and §4
items 4–5 · `tools/sigcheck.py` · `tools/logscan.py` · `Code/00_Core.lua`
`:99-165` · `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log`
(the canonical boot log you test against) · your inbox.

## 1 · A-4 — `sigcheck.py` over `SetGlobal` sites

`sigcheck.py` reads `function Name(...)` definitions only. The pack has **15
`SetGlobal` sites** and anonymous function literals that it cannot see at all.
Extend it to resolve the local named in `SetGlobal("Name", <expr>)` and check
that function's signature like any other.

⚠️ Remember what `sigcheck` is and stays: an **arity** bound. It never clears a
body. Do not let the extension's wording imply otherwise — that implication is
how F114 shipped.

## 2 · A-3 — `logscan.py` counts heals

"Last verdict wins" misses a `DataPatch` heal. `SaintBlessing` logs `inactive` at
`:166`, then `corrected …` at `:186`, and **ends the boot ACTIVE**. So the
headline "17 inactive" is really **16**, and the module that was actively
breaking the Saint blessing was hiding inside the number that was supposed to
reassure us.

Make `logscan.py` heal-aware: a module that logs a later `corrected`/applied line
ends ACTIVE regardless of an earlier `inactive`. Re-run it against the canonical
log and report the corrected census.

⛔ **Verify against the archived log, not a fresh one.** A log copied while
`Mars.exe` is running is a PARTIAL log and has already cost this project two
wrong counts.

## 3 · A-2 — the benign latch is a RETIRE signal

Today a `DataPatch` pass that finds data "already correct" is filed as HEALTHY.
R-13 (`LastTransmissionStorage`) shows that is exactly backwards: **it is the
REMOVE signal.** The pack had no bucket for "vanilla fixed it", which is why 32
modules survived an audit they should not have.

- Rename it in the boot log: `inactive (already correct — RETIRE candidate)`.
- Have `logscan.py` list benign latches as retire candidates.
- Have `bodycheck.py`'s `DEFECT-GONE` output feed the same bucket, so the two
  instruments agree on one list.

## 4 · A-1 — `GeneForging` reads the legacy map

The module works (K-4) but reads `TechDef.GeneForging.param1` — the **legacy stub
map**. Prefer `Techs.GeneForging:ResolveValue("param1")`.

⚠️ This is the one code change in this prompt. It is a KEEP module, so it already
carries 01's `SRC:`/`DEFECT:` manifest — **re-stamp it after the edit**, and run
`bodycheck.py` before and after so the change is visible to the instrument.

## 5 · Scope fence

**In:** `tools/sigcheck.py`, `tools/logscan.py`, `Fix_GeneForging.lua`, and the
log-line wording in `00_Core.lua` **if and only if** the rename requires it —
if it does, keep that diff to the string alone.
**Out:** `bodycheck.py` (01 owns it — extend only its *output consumption* here,
not the tool); every other module; `items.lua`; store text.
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- The heal-aware change would alter a count this project has already published
  or cited ⇒ report the delta explicitly rather than quietly correcting it. A
  silently-corrected number is destroyed evidence (chain rule 5).
- The `00_Core.lua` log-string rename turns out to touch control flow ⇒ **STOP
  AND ASK.** That file is not yours to improvise in.

## 7 · What may NOT be claimed

- ⛔ Not "the tooling now catches game updates". It catches classes a, b, d, e.
  Class c — semantics moving under a wrapper — is still seen by nothing, and 6 of
  the 10 FIX rows this audit were class c.
- ⛔ Not "the log census is verified" beyond the one archived boot log you ran
  against.
- ⛔ No status moves.

## 8 · Close-out

Green gates. Outbox to `06` (if any wording changes) and `99` — 99 needs the
corrected census number and what changed to produce it. Strike your README row,
`git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- `tools/logscan.py --build <id>` is the safe read; a hand-rolled grep
  undercounted throws 30 vs 157 on 2026-09-08 because the engine writes the
  `[LUA ERROR]` header in two forms and only one carries the file path.

### From link 01 — core, tooling and the manifest

⚠️ **For you specifically:** item 8's first bullet is routed to you — `bodycheck.py --selftest` is a manual gate today and wiring it into `doccheck.py` beside `harvest --check` is your fence, not mine. Item 4 has the CLI and exit codes; `sigcheck.py` was left untouched, as your prompt requires.

*(From link 01, `smr-bugfixpack-25`, 2026-09-08. Commits `6d452a3` probe form ·
`401f8a0` bodycheck.py · `6db7457` FIX_POLICY §2a/§2b · `e2490f3` KEEP set
stamped. ⛔ Nothing was run in a game; no status moved.)*

**1 · The `probe` form — exact signature and semantics** (`00_Core.lua`,
`SMRFixPack.Require`). `{ probe = function() … end, reason = "…" }`, a sibling of
`test`:

* The probe takes **no arguments** and runs under `pcall`.
* **ONLY the literal boolean `true` applies.** A throw, `nil`, `false`, or any
  other value (a captured table included) **declines**. "Captured nothing" is
  UNKNOWN and UNKNOWN is not permission.
* A throw is a DECLINE, never propagated. It is logged as
  `<id>: behaviour probe declined (threw: …)` so an authoring error in the probe
  cannot hide inside a silent decline.
* A probe failure returns `c.reason`, exactly like every other form, and does
  **NOT** set `update_suspect` — it is a behaviour verdict, not patch rot, and on
  the other branch a decline is the CORRECT outcome.
* Write the **stub contract beside it**: a comment naming what the stub must
  provide and why the target is safe to call on one. ⛔ Only for targets you can
  show, from the shipped 1.1.0 body, to be **synchronous and side-effect-free on
  a stub**. If you cannot show both, the module gets no probe and keeps its
  existing check — that is a permitted outcome, not a failure.
* Two shared lines were touched and both are identity for every existing form:
  `local ok, name` → `local ok, name, why`, and the return → `c.reason or why or
  (name .. " not found …")`. No existing reason string was reworded.
* `Require` is a plain function, so a `DataPatch` module may call it from inside
  its pass, after `DataLoaded`, for a preset-bound probe.

**2 · The branch guard, and it is not negotiable** (`FIX_POLICY §2a` — link 04,
this is Job D's answer verbatim). ⛔ **Do not build a game-version detector.** It
would be a LABEL check, against the rule that made the F115 gate correct; and it
is unbuildable anyway, because `lua_revision`, `ModMinLuaRevision` and
`ModRequiredLuaRevision` are ALL 350453 on both branches (`EF-077`) — which is
precisely why nothing warns a 1.0.7 player. There is no field to read. ✅ **The
per-module `probe` IS the branch guard**: a probe confirming the 1.1.0 body shape
a module was written for necessarily declines on a 1.0.7 body, per module, with
no version arithmetic anywhere and nothing global to keep in sync.

**3 · The manifest grammar** (`FIX_POLICY §2b` has the authoring rule;
`tools/bodycheck.py`'s docstring has the machine half). Header-block comments:

```lua
-- SRC: <path> <selector> sha256=<64 hex>      -- or:  -- SRC: none <reason>
-- DEFECT: <python regex>                      -- or:  -- DEFECT@<path>: <regex>
```

* `<path>` slash-separated, relative to `ModTools/Src` (`\` accepted).
* `<selector>`, no spaces: `Class:Method` (separator is a hint — both declaration
  forms and `Class.Method = function(` match), a bare `Name` for a global or
  `local function`, or `L<first>-<last>` for a literal span where there is no
  function to name.
* Body = declaration line → first bare `end` at the same indentation. The
  delimiter is `luafn.py:find_bodies`, **imported** by `bodycheck.py`, so there is
  never a second extractor. Line endings normalised, trailing whitespace stripped
  per line; indentation and comments kept; sha256 of the utf-8.
* `-- DEFECT:` searches the body of the `SRC:` above it. `-- DEFECT@<path>:`
  searches that whole file — the **DataPatch shape**: no body to hash, so declare
  `SRC: none` and state the defect against the shipped DATA.
* Several `SRC:` lines per module are fine; each `DEFECT:` binds to the nearest
  above it. Regexes are Python `re`, ONE line, **not** `re.MULTILINE` (`^`/`$`
  will not do what you want — use `\s+` to cross a line break). Shipped Lua
  indents with **tabs**: write `\s+`, never a literal space.
* ⛔ **State the DEFECT, never the PHRASING.** See item 5.
* ⛔ Never hand-type a hash: `python tools/bodycheck.py --pin <path> <selector>`
  emits the line and the range it hashed.

**4 · `tools/bodycheck.py` — CLI and what its falsifier proved.**

```
python tools/bodycheck.py                 # the pack against the live 1.1.0 tree
python tools/bodycheck.py --src <path>    # another ModTools/Src
python tools/bodycheck.py --code <path>   # another Code/ tree
python tools/bodycheck.py --all           # also print OK / NO-MANIFEST rows
python tools/bodycheck.py --module NAME   # one module
python tools/bodycheck.py --pin <path> <selector>
python tools/bodycheck.py --selftest      # ⛔ the falsifier
```

Exit 1 on `BODY-CHANGED`, `DEFECT-GONE`, `TARGET-ABSENT`, `TARGET-MULTI`,
`MALFORMED`; counts only for `NO-MANIFEST`, `NO-DEFECT`, `SRC-NONE`, `OK`.
⚠️ Deviation from the prompt, stated: `TARGET-ABSENT`, `TARGET-MULTI` and
`MALFORMED` also exit non-zero, not just the two named. A stamped module whose
target vanished, resolves ambiguously, or whose manifest does not parse cannot be
re-verified, and a manifest that merely *looks* like coverage is worse than none.

`--selftest` asserts ten legs, permanently, because a tool that returns GREEN on
everything is indistinguishable from a broken one. **Two legs are real game-side
events**: `DEFECT-GONE` fires on one of the actual 32 (`MinDaysFoodSupply
BeforeNotification` is gone from the whole 1.1.0 tree while
`ResourceTracking:GatheredResourcesOnHourlyUpdate` still exists with our arity —
invisible to `Require` and to `sigcheck`), and `TARGET-ABSENT` fires on
`Colonist:UpdateSatisfaction`, which 1.1.0 deleted. `BODY-CHANGED` fires on a
**real body edit** — F116's in-body repair at `add94b3`, pinning the pre-repair
body against the repaired tree — plus a hash negative control and the converse
leg, so it cannot pass by being always red.
⛔ **ONE HONEST LIMIT, in the file itself:** the 1.0.7 tree is GONE from disk
(`EF-075`), so no true 1.0.7-vs-1.1.0 **game** body pair exists to hash. The
mechanism is proven on a pack-side edit and a negative control, not on a
game-side branch pair.

**5 · The finding that will bite you if you skip it.** Writing the tool's OK
control walked straight into the trap. F46's 1.0.7 phrasing was
`station.demand[res]:GetTargetAmount()`; 1.1.0 hoisted it to
`local demand = station.demand and station.demand[res]` / `demand:GetTargetAmount()`
(`Train.lua:794-795`) — a pure **refactor**, defect untouched. A `DEFECT:` pinned
to phrasing therefore reports `DEFECT-GONE` for a bug that is still shipped: a
FALSE "vanilla fixed it", the direction that **retires a live fix** (R-15's
shape). The right expression states the fault — `Min\(carried,\s*station_cap\)`,
the unload computed from the cap alone. Locked in as fixture `Fix_Selftest
RefactorTrap`. ⚠️ **A `DEFECT-GONE` is a REMOVE candidate, never a verdict.**

**6 · What is stamped, and what "verified" means here.** All 35 KEEP rows (§1d),
76 manifest rows, 73 `OK` / 1 `NO-DEFECT` / 2 `SRC-NONE`, exit 0. ⛔ The FIX and
REMOVE sets are deliberately **unstamped** — 46 `NO-MANIFEST`, which is a count,
not a failure, until the pack is whole. Every hash was taken from the live tree,
so "the hash matches" is true by construction and proves nothing; its value is
future. What IS evidence: each target was resolved in the shipped tree and its
DEFECT expression written against the 1.1.0 body and confirmed to match there.
Three targets had moved far enough that the module's own 1.0.7 header no longer
describes them (`GetRareTraitChance` is now 5 lines through
`Techs.GeneSelection:ResolveValue`; `TunnelBase:AddPFTunnel` guards
`self.linked_obj`; `AlienDigger:GameInit` sits at `:87-96`).
⛔ **NOT a claim that the KEEP set is verified** — I pinned bodies the
re-verification read and re-read only what a defect expression needed. No KEEP
verdict was re-derived; K-9 and K-10 stay "on record, not re-read".

**7 · The named exceptions — a defect that is an ABSENCE cannot be stated
directly**, because a regex matches what is present:

| module | why | what was pinned instead |
|---|---|---|
| `Fix_SinkholeIndestructible` | missing `indestructible` / `disasters_strike_immunity` on a generated class table | the whole classdef by span (`L4-25`), so vanilla ADDING the flag reads as `BODY-CHANGED`. The one `NO-DEFECT` row |
| `Fix_BrokenTrackSalvage` (1st target) | `node_idx` missing from the parameters copied onto the repair site | the consequence, against the sort that raises (`a.node_idx < b.node_idx`) |
| `Fix_GeneForging` | `GeneForging` is unknown to `GetRareTraitChance` | the half that IS present. `DEFECT-GONE` will not fire if vanilla adds the tech alongside `GeneSelection` |
| `Fix_FreedHousingNotice` | `RemoveResident` wakes nobody | its tail (`ResetFreeSpace` as the last act), so adding the wake call stops the match |

**8 · Filed, not fixed (out of my fence).**
* **→ link 05:** `bodycheck.py --selftest` is NOT wired into `doccheck.py`; it is
  a manual gate today. Wiring it (alongside `harvest --check`) is the tools-tail
  fence, not mine.
* **→ link 06:** the inherited `metadata.lua` comment claiming "`PackVersion`
  renders version_major.version_minor.version" describes nothing that exists in
  the 1.1.0 tree (zero grep hits). Passed on from link 01's own inbox, still
  unfixed.
* `sigcheck.py` rated `Fix_TrackSalvageWipe` OK both before and after F116's
  defect was found. `bodycheck.py` is the instrument that closes that, and F116
  is now one of its falsifier legs — but only pack-side (see item 4's limit).

**9 · Drift caught in my own work (chain rule 5 — evidence, not shame).**
* The first block-balance checker counted a `for … ipairs({` whose `do` sits on a
  later line as **two** openers and flagged `Fix_RocketInteractGuard`, which is
  byte-identical at HEAD. Caught by checking HEAD before believing it. Fixed to
  pair each loop head with its own `do`, re-falsified against a deliberately
  broken copy; all 81 `Code/*.lua` balance 0. ⚠️ There is no Lua binary on this
  rig — block balance is the whole desk syntax check, so a wrong checker is a
  wrong gate.
* My first `EXPECT` sets in `--selftest` were wrong twice (a stamped fixture
  yields a row per manifest LINE, not one per module). The tool was right both
  times; I corrected the assertions, not the tool.
* Stamping wrote the 35 files LF where the working tree is CRLF. Content in git
  is unaffected (`git diff` = 35 files, 353 insertions, 0 deletions), but the
  repair pass converted **39 files I had not touched**; they had zero content
  diff and were restored with `git checkout --`. ⚠️ If you see EOL-only churn in
  `Code/`, that is where it came from, and it is not in any commit.

⛔ **What may NOT be claimed from this link.** Not "the pack is update-proof" —
class (c), semantics moving under a wrapper, is still seen by **nothing**. Not
"the KEEP set is verified". Not "probes are safe" in general. No status moved: a
tool run is not a test.

### From link 02 — a doccheck gap that `H-10` says matters

*(Link 02, `smr-bugfixpack-11`, 2026-09-08, CLOSED. Routed here rather than left
in 99's inbox: 05 owns the tools tail, and this is a tools defect, not an audit
observation.)*

**`doccheck` reported GREEN while `items.lua` held 45 entries and
`metadata.lua`'s `code` list still held 81.** I deleted 36 modules, updated
`Code/` and `items.lua`, and doccheck passed. The only reason I caught the
`metadata.lua` half was that its own output line prints the number —
`LOAD ORDER: … 81 file(s) in the code list` — and I happened to read it against
the 45 I expected.

⛔ **Why this is worth a gate rather than a note.** `H-10` is the hazard about
exactly this inconsistency, and it is the one whose failure mode is silent: both
portals force a `SaveDef` on upload that rebuilds `metadata.lua`'s `code` list
**solely from `items.lua`** (`Mod.lua:816-840`, `:973`). So a mismatch does not
lint — it decides what ships. doccheck already computes both numbers and simply
never compares them to each other.

**Suggested shape, not a specification** — 05 owns the call:
* Assert `set(Code/*.lua) == set(items.lua entries) == set(metadata.lua 'code')`,
  and report the SYMMETRIC DIFFERENCE by filename rather than a count mismatch. A
  count check would have passed a same-size swap.
* Make it RED, not a warn. There is no legitimate state in which the three
  disagree.

⚠️ **A second one, smaller and adjacent** (link 01 filed the first half of this;
this is the confirming instance): `bodycheck.py --selftest` is still a MANUAL
gate. During this link, `bodycheck`'s NO-MANIFEST count going 46 → 10 was the
single most valuable cross-check I had — it confirmed the right 36 modules left
without re-reading a row — and nothing in `doccheck` would have noticed if the
number had come out wrong.

**One drift datum from my own work, for whoever wires the desk gates.** There is
no Lua binary on this rig, so block balance IS the syntax check. My first
balance checker flagged **16 byte-identical files** — the same trap link 01 hit,
reached by a different route: regex comment/string stripping merged lines. The
replacement lexes properly and carries a 12-leg falsifier (keywords inside
strings and long comments, `for`/`do` double-counting, `repeat`/`until`,
`elseif`). ⇒ If a balance check ever becomes a committed tool, **it needs its
falsifier committed with it** — a checker that cannot go red is indistinguishable
from a broken one, and this one silently accused clean files twice in two links.
