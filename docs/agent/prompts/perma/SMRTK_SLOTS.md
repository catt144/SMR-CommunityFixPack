# SMRTK slots — preload a sitting

Standing prompt, authored by smrtk 07 on 2026-09-14. Home: local TestKit
`C:\Dev\SMR-BugFixPack-TestKit`. Use before a sitting, with its brief supplied
in the invoking task. This tool is not a fix; it never ships.

## Read and scope

Read `docs/agent/STATE.md`, the sitting brief and upstream notes, WORKFLOW's
Cheats on playtest saves/Writing in a shared tree sections, PLAYTEST_HELP's
toolkit/console sections, and the TestKit README. Inspect 70's dispatch and
74's Bind/Trigger APIs plus the current `80_AgentSlots.lua`; a prior binding is
a claim, not today's sitting. Read the installed source for every new mutation
leaf; inherit matching build identity with `python tools/doccheck.py --emit-fingerprint`.

IN: sitting-owned `Code/80_AgentSlots.lua`, its predictions and the brief's
handoff. OUT: pack runtime/version/metadata, toolkit build files, portal APIs,
achievement/account state, live UI prototyping. Route defects to the brief's
report and fixing link. Never touch a peer's unstaged work. No delegation needed.

## Progress and construction

Create and maintain a todo list, one item per commit-and-verify unit: fixture
and leaf reads; slot bindings/predictions; gates/commit/handoff. Recheck log,
pull/status and active sessions in both repos (TestKit has no remote). Run
`tasklist /FI "IMAGENAME eq Mars.exe"` separately before any Code write. If
running, finish independent document preparation and wait for the game to close.

Rewrite 80 for this sitting using real `SMRTK.Bind(n, label, fn, opts)` functions,
slots 1–6 and optional `SMRTK.BindScratch`. No strings compiled at runtime, load-
time mutation, automatic arms or detached mutation threads. Every leg follows
**MARK → set up → act → DUMP → MARK**. Validate fixture/map/selection/pins before
mutation; a refusal must be `false, reason`, not a success-shaped no-op. Give each
slot a plain label and named prediction. More than six legs can share a slot
only through an explicit documented stage; do not silently overwrite bindings.

`ctx.sel` is current selection, `ctx.pin` holds A/B/C refs, `ctx.cursor` is the
current/captured map point, `ctx.state` survives armed phases, and `ctx.mark`
writes a distinct MARK. Validate IsValid on each use. Use registered Run/Arm/Fire
inside the executing thread; the dispatcher writes the primary result and checks
taint. Auxiliary DUMP fields go through `ctx.log("DUMP", fields)`. Return useful
after-state fields; never print your own primary result. Register triggers
disarmed; predicates are read-only, nonyielding and unlogged. Lua's effect field
is `["do"]`, not bare `do`. Document game-time cadence/paused limitations.

For armed clicks use 74's shared listener contract and `on_click`/`on_disarm`,
with explicit once-click vs repeat behavior. Right-click cancels; save/load/map
change disarms, load/map change clears pins. Rebinding an armed slot refuses.
Callbacks and pin refs are not saved. Save/load operations need real-time context;
native stamp/completion requires running game time. Do not invent a fit-test flag.

## Predictions and handoff

Write numbered predictions **before boot**: exact SMRTK verb/action/status and
expected fields, first-screen witness, normal time and 3× abort time. Generated
ids, handles, session nonces and game time are variables, never invented literals.
Preserve numeric MARK return indices for copying across later marks/screenshots;
string CopySince accepts only the current label. A truncated ring copy cannot
replace the complete archived boot log.
Declare clean-fixture needs and resource provisioning cost. No-taint is necessary
but eligibility stays `UNAVAILABLE:sandbox` on build 24995074. Toolkit lines are
intentional and attributed; never ask the owner about one. Stop on unexpected
taint, engine errors or mutation; do not rerun to obtain a preferred verdict.
End EVERY boot with a `taint_read` and an `eligibility` dispatch, so each boot's
negative is a sample and not an absence (smrtk 99: the 08b World boot had none).

If probes are needed, run the exact desktop stale-probe sweep before trusting
them; every hit must be declared needed or made unavailable. Preload its actual
command/output/exit/hit names, full pack/TestKit HEADs, check time and brief in
the slot's real function. At invocation set session/sitting/game from live state,
then use `SMRTK.ProbePreflight`; no stale or empty invented attestation. Any
load/map change expires it. Inspect 76 for the current evidence schema.
The gate cannot see the tree's HEAD, so the sweep's own freshness is what keeps the
stamp honest. A desktop sweep is fresh for 24 hours, or until a change that warrants
one: something since the last sweep touched a probe, a module a probe reads, or the
kit's registration. A stale sweep is satisfied at the next playtest, owed there before
the probes run in it and never owed between sittings. An agent may recommend a sweep
outside playtesting only if it can give the reason and name the harm; recommending is
all it may do. No agent, gate or kit code refuses a boot, a RunAll, an upload or any
other work over a sweep's age, and none overrides the owner (ck184 a, ruled 2026-09-15;
the owner's framing is a gate, not a hard rule). A stale attestation did pass once —
08b, five hours, a different tree — and the 24 hours is calibrated against it.

The first sitting after TestKit `f5fa650` (smrtk 99's Code link, 2026-09-15, desk-only)
also witnesses its four changes, each a prediction: a mechanized depot's fill/empty
record carries `before`/`after` numbers; the field editor on Selected and Run reads
dark text on a light box; a watch on a field the object lacks is REFUSED naming the
field, and 08b item 9's unrun leg then arms on a field it HAS and fires; no console
log overlay appears at boot. Record each as witnessed or NOT RUN by name.

Parse 80 with `python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet`;
run `python tools/doccheck.py` GREEN. Check rule 6 using `rg -n 'NetSyncEvent|LogCheatUsed'
C:/Dev/SMR-BugFixPack-TestKit/Code -g '7*_SMRTK*.lua' -g '80_AgentSlots.lua'`
and rule 7 using `rg -n '^\s*print\('` on those same files: zero matched lines,
rg exit 1; errors are not a negative gate. Include a positive installed-source
control. Recheck diff/status, stage exact paths and commit with `-F` plus pathspec
(shared hunks follow WORKFLOW). TestKit has no remote; push pack docs if changed.
Quote doccheck WARNs verbatim in the handoff. Keep predictions separate from
play evidence; no status promotion without witnessing the leg.

Give the owner one line after gates pass: **"start the game; the Agent tab is loaded"**.
Relay the slot labels, predictions path and HEADs to the attending agent; that
agent reads/logs results and archives evidence. Do not ask the owner to paste
commands already provisioned in slots. This standing file is updated in place,
never consumed with git rm.
