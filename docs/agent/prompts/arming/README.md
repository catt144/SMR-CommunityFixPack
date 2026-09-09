# Arming — one harness, one set of rules, for unattended in-game legs

**What this folder is.** Everything needed to arm the game with a measurement
payload and take it back off again. The harness is `tools/arm_leg.ps1`; a leg is
a JSON manifest in `legs/`; the Lua it installs lives in `payloads/`.

```
python -c ""                                   # nothing to install
powershell -File tools\arm_leg.ps1 -Manifest docs\agent\prompts\arming\legs\c48-brake.json -Mode arm
#   ... launch the game, let the payload run, copy the log AFTER the process exits ...
powershell -File tools\arm_leg.ps1 -Manifest docs\agent\prompts\arming\legs\c48-brake.json -Mode disarm
powershell -File tools\arm_leg.ps1 -SelfTest  # 20 legs, the falsifier
```

`-Mode verify` runs the gates against whatever is on disk and writes nothing.

---

## Why this exists at all — three generations of the same script

Created 2026-09-09 by consolidating a copy-forward lineage that kept being
resurrected from graves rather than kept:

```
d13-rescue/RS_ARM.ps1  (grave 6b75e11) -> combined-sitting/CS_ARM.ps1
c47-farm/C47_ARM.ps1   (grave fd1102a) -> c48-brake/C48B_ARM.ps1 -> c48-pairing/C48P_ARM.ps1
```

Each generation re-derived the same hard-won rules, and each carried its own
copy of the gate logic. `97_C47Common.lua.txt` was stored **twice, byte for
byte** (sha256 `a9ffc646…`, 19,449 B). Same shape as `tools/parsecheck.py`,
which exists because three sessions in a row hand-rolled a block-balance
checker. ⛔ **The graves are `git show 49e32bf:<old path>`** — the cell-matrix
logic in particular was NOT carried forward (see `legs/combined-sitting.json`).

## The rules, and the failure each one is made of

| | rule | the failure behind it |
|---|---|---|
| **C11** | Arming is a script FILE, never an inline one-liner. | An inline edit's quoting was mangled once and **the game launched UNARMED** — a full sitting that measured nothing. |
| **C11a** | Never pipe the harness's output through `Select-Object`. | A piped consumer terminates the upstream pipeline and can kill the script **before its write executes**. |
| **G5** | After writing, every piece is read BACK OFF DISK. Missing **or listed twice** is a failure. | d13-rescue cell r1 was armed on top of armed-r0, metadata listed the payload twice, **it executed twice and two legs raced**. |
| **S3** | Payload bodies are ASCII-only; metadata is written with no BOM and LF endings. | Windows PowerShell 5.1 decodes a `.ps1` as the ANSI codepage unless it has a BOM, so a single em-dash becomes three characters and **breaks string parsing mid-file**. This bit the rewrite itself on its first run. |
| **110** | Payloads go in the TEST KIT, never in the fix pack. | Owner ruling: *"the pack ships ZERO diagnostic code."* The harness only ever writes under the kit repo. |

## ⛔ An armed tree cannot be committed, and that is the point

Every payload must carry a `TEMPORARY` marker. `tools/doccheck.py`'s
`temporary_sweep()` returns `not hits`, so a `TEMPORARY` marker anywhere in
`Code/` or the kit's `Code/` makes doccheck **RED** and the pre-commit hook
blocks. Arm, measure, **disarm**, then commit. If doccheck is RED and you cannot
see why, you are still armed.

## ⭐ Two bugs the consolidation found in its ancestors

Both were live in all three hand-written scripts, and both are the project's own
recurring lesson — check the thing, not its label.

1. **A false GREEN on "is the payload armed?"** The ancestors asked with a raw
   substring match over the whole metadata file:
   `$m -match [regex]::Escape('"Code/98_C48Brake.lua"')`. That **also matches a
   commented-out line** — and commenting a line out is the kit's own disarm
   convention (see `97_ForceInactive` in the kit's metadata). So the gate could
   confirm a payload was armed when it was inert and would never load. The
   harness now parses the code list line by line and ignores any line whose
   first non-whitespace is `--`.
2. **Every arm and disarm silently rewrote the kit's `metadata.lua` as CRLF.**
   `[System.IO.File]::WriteAllLines` joins with `Environment.NewLine`, which is
   CRLF on Windows; the kit's file is LF. Any inexplicable whole-file diff on the
   kit's metadata came from this. The harness writes through one LF-only writer
   and a self-test leg holds it there.

## What the gates check

Per payload: on disk · **actively** listed exactly once · `TEMPORARY` marker ·
ASCII-only body · banned patterns absent (comment-stripped, so a name in prose
is not a false positive) · the driver calls the boot symbol at file scope **and**
`quit()` · a library payload does **not** call the boot symbol (two flows at file
scope race, and the loser's measurements interleave with the winner's).

Per leg: everything in `permanent` survives on disk and in the list ·
everything in `mustNotBeListed` stays inert · every string in `requiredPresent`
appears (the declared-mutation gate — a leg that mutates must SAY what it
mutates and be able to restore it; an inert payload that still launches the game
is the expensive failure) · **every `<namespace>.Name` used anywhere in the leg
is defined somewhere in the leg.**

⭐ That last one is the class no parser can see: the Lua compiles, then indexes a
nil at run time and the leg dies mid-measurement. `parsecheck.py` proves a file
PARSES and nothing more. The same defect class was found independently in the
kit on 2026-09-09 by link 07, in probes calling `SMRTest` helpers their file
never aliased — one instance had been committed and was live in history.

## ⚠️ Before you run any of these on 1.1.0

- **`EF-079`: 1.0.7 saves cannot load on 1.1.0.** Every payload here was written
  against 1.0.7 fixtures, so its colony assumptions are unreachable and a 1.1.0
  leg needs a colony provisioned from scratch (hours). `EF-080`'s override is
  triage-only and does not buy that back. **The harness is version-independent;
  the payloads are not.**
- ⛔ **`Mars.exe` must not be running when you arm or disarm.** You share one
  game with other sessions and with the owner.
- ⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** Re-copy after
  the process exits before quoting any count or rate — this produced two wrong
  counts on 2026-09-08 (a "1" that was 6; a "30" that was 157).
- The kit is `C:\Dev\SMR-BugFixPack-TestKit`, **local-only with no remote, by
  design and settled** — never raise a push there as owed.

## Writing a new leg

Copy the nearest manifest and change it. Required: `leg`, `kit`, `park`,
`payloads[]` (`src`, `dst`, `selfDrives`). Optional but usually wanted:
`stripPattern` (a NARROW family regex — it is what stops an arm-on-top-of-armed
double listing; `Code/9[78]_C4[78]` matches the C47/C48 family and deliberately
not `97_ForceInactive`), `anchorAfter` (a metadata line to insert after, because
Lua load ORDER is semantic — omit it only if the payload genuinely may load
last, in which case the harness anchors after the last active entry),
`bootSymbol`, `symbolNamespace`, `permanent`, `mustNotBeListed` +
`mustNotBeListedWhy`, `bannedPatterns` (regexes), `requiredPresent` (literals).

⛔ **Add a self-test leg for any gate you add**, both directions — seen to fire
on a rigged case and seen NOT to fire on a clean one. The 20 legs in
`-SelfTest` are the standard; two of them exist because they caught the two
bugs above.
