# fixtoggles 06 — the save-state four

Link 06 of `fixtoggles`. README binding rules 1–18 are yours. Runs after a 03 PASS; independent of 04 and 05. This is
the link where an error lands in players' SAVES, which is why it sits on the top tier. `FIX_POLICY` §3a binds every line.

## The set

1. **SaintBlessing (F92)** — rewrites `TraitPresets` data on the 1.0.7 path and re-bases saves on load (research `:269`,
   `:329`). On 1.1.0 it is save-repair only. Decide, from the shipped bodies on BOTH trees, what a switch can honestly
   do: live, next-load, or not switchable on 1.0.7 (the branch rule 10 keeps you from building for; state it for 09).
2. **TrackTunnelPowerBridge (F65)** — bridged tracks keep a power tunnel in the save and the `Done` teardown must stay
   on while any exist (`:56-69`); its `StationsConnected`/`PostLoadGame` handlers are installed in apply and **not
   gated** (`:160`, `:166`). ⇒ Split: gate only the bridging; the teardown is an always-on part the panel shows as such.
3. **ExoticDepositSign (F102)** — the value is baked into the built class (`:81`) and a live re-sign on an asteroid
   touches the suspected freeze trigger ⇒ **next-load** (restart-required), shown as such.
4. **90_SaveSanitizer (F35, F48, F95)** — decide per pass: is each switchable, always-on, or not exposed? A repair pass a
   player turns off must never leave a save worse than vanilla would; say what each pass protects.

## Job, per module

Open the module and the shipped bodies. For each, the spec §7 row gets CONFIRMED or CORRECTED with the evidence; then
build the disposition (gate / next-load / split / not exposed), the header (both directions + what stays in the save),
and a desk case for **off → save → load → on** as well as on/off. Any disposition that leaves a switch unable to do what
a player would expect → ck148 (plain language, a recommendation). One module per commit.

## Scope fence

IN: the four module files, the harness, ck148 appends. OUT: core (route changes through the README), other modules,
text, version work.

## Stop conditions

A switch that could leave a save harmed (a stranded state, a leak, a thread with no orphan gate) with no layer-3/2
route → stop, route it; the owner decides whether that module is exposed.

## What may NOT be claimed

That a save is clean after any switch sequence (rule 8). "Tested" for anything a desk harness showed.

## Close-out

Green gates, `Mars.exe` closed. Outbox to 06b and 99 (and every 1.0.7-only consideration to 09's inbox); strike your
row; `git rm` this file; push.

## Notes from upstream

- (links 01–03 append here)
