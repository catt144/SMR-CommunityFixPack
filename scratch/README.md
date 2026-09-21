# scratch/

Working space for any session or subagent. Write freely here — no permission
needed. This folder is never committed (see `.gitignore`) and never cited from
a committed document: nothing here is evidence or a record.

If a committed document needs to cite a file, that file belongs in the repo
instead. The case that proves it: a 133 KB fan-out gate-evidence file was
written to `C:/Dev/smrtk_gate_evidence.md` — outside the repo entirely — and
then cited by command lines across `docs/agent/reports/SMRTK_FANOUT_REPORT.md`.
The citations survive; the file itself does not, because nothing outside the
repo is durable. Put evidence a report depends on under `docs/` instead.

The eviction prompt (`docs/agent/prompts/perma/STATE_EVICTION.md`) sweeps
files here older than 14 days. `README.md` itself is never swept.

Durable material that must not be committed — the case above is a *working*
file, not durable evidence — belongs in `../local/` instead, which is never
swept and is entry-gated by `local/README.md`.
