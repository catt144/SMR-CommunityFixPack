---
name: smr-bug-library
description: Read or file a defect entry or engine fact in the Relaunched Fix Pack repo — the cheapest-first route into docs/agent/bugs/ and docs/agent/facts/, which front-matter fields are load-bearing, and the filing procedure that passes doccheck first time. Use when looking up a bug ID (F/D/C), checking whether a defect is known, or recording a new one.
---

# The bug library — reading and filing

187 entries in `docs/agent/bugs/` (`F` fixes, `D` tombstones, `C` candidates) and 92 engine
facts in `docs/agent/facts/` (`EF-NNN`). Both carry a **generated** `INDEX.md`.

## 1 · Reading — cheapest first, stop when you have the answer

0. **Ours-or-vanilla check:** `rg -l -F -- <keyword> Code/` searches this pack's runtime code first; hits inspect ours, while an empty literal search is only a cheap vanilla lead and does not rule out aliases or indirect effects.
1. **`docs/agent/bugs/INDEX.md`** — 222 rows of ~229 chars. One row usually answers "is this
   known, and what is its status". Read the row, not the entry.
2. **The entry's own section, by heading** (`### Control`, `### Repair`, `### Attended
   check`). Never read a whole entry for a narrow question, and **never read a file to prove
   a negative** — one grep settles absence; a read never does.
3. `docs/agent/facts/INDEX.md` is 43 KB — **grep it, never read it whole**. To ask whether a
   fact still holds, use §3 rather than opening the fact at all.

## 2 · Front matter — load-bearing or not

| field | read it? |
|---|---|
| `status` + `status_source` | **yes** — `fixed`, `tested-attended`, `cand`, `wontfix`, `parked`… |
| `derived_at:` (facts) | **yes** — the sha or game build it was derived against |
| `seq` / `row` | ordering; `seq` must stay contiguous |
| `updated` / `verified` | dates, not evidence |
| `row_status:` | **no. Read nothing from it.** |

`row_status:` is a frozen copy of the index row the 2026-08-03 migration deleted. doccheck
reads **only its first word** and deliberately tolerates that word disagreeing with
`status` — a status that has advanced must be free to leave it behind, so those `warn` lines
are expected, not defects. Long cells were moved to the end of the entry body under
`#### Frozen migration row (2026-08-03)`.

**Authoring warning:** `split_bugs.render_entry` emits only `FRONT_FIELDS`; an invented
front-matter key such as `issue:` is silently dropped on render. Put durable context in a
supported field or the entry body, and do not repurpose `row_status` as a general field.

## 3 · Is this fact still true?

`python tools/doccheck.py --emit-fingerprint` groups facts by `derived_at:` and says whether
each still describes what is installed. **HOLDS** needs no re-read. **MOVED** means the
citations point into a tree that is not on disk — re-derive against the archived tree the
entry names, never the live one. A fingerprint reading `(inferred from updated:)` was
back-computed from a date, so it is weaker evidence than a bare one.

## 4 · Filing

No scaffold command exists yet — copy the shape of a recent same-letter entry.

1. New `docs/agent/bugs/<ID>.md`: `id` matches the filename, `seq` continues without a gap,
   heading tag and `status` agree.
2. State the **control** — what would falsify the claim — not just the story. A cause without
   a control is a plausible story; this project files controls.
3. `python tools/doccheck.py --regen`, then `python tools/doccheck.py` until GREEN. `--regen`
   builds `INDEX.md` from **every entry on disk**, a peer's uncommitted ones included — check
   `git status docs/agent/bugs/` first and commit only your own paths.
4. `git add <exact paths>` then `git commit -F <msgfile> -- <same paths>`. Never `-a`.

## 5 · What you may not do

Never move an entry's status to record your own opinion — a status word is evidence about
what was *tested*, and `tested-attended` means the owner watched it in the game. Never
bulk-upgrade a legacy bare `tested`. "Vanilla fixed it" is a claim: trace the replacement
body before acting on it, because a rename reads as a deletion.
