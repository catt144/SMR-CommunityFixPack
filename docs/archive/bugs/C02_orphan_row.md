# C02 — archived index row (no entry text ever existed)

Archived **2026-09-16** with the 1.0.7-era candidate block. C02 is the one id
that held an INDEX row and **no entry body anywhere** in the original
`docs/BUGS.md` — verified twice on 2026-08-03 — so the 2026-08-03 split parked
its row in `docs/agent/bugs/_notes.md` front matter rather than inventing an
entry for it.

That row is preserved verbatim here, and `_notes.md`'s `orphan_rows` is now
empty. Row **112** is therefore held by this file: `doccheck`'s gap check reads
the number back out of `docs/archive/bugs/` and accepts the hole in the live
numbering because of it.

```
{"row": 112, "id": "C02", "title": "Cave-ins reported on asteroids — no Src code path found", "status": "cand", "status_source": "row-evidence", "priority": "?", "evidence": "cand", "row_status": "runtime-check", "note": "NO ENTRY TEXT (verified prompt 1, 2026-08-03)"}
```

⛔ **Pull-only.** Nothing tracks this file and nothing raises it. It exists so a
future pointer about asteroid cave-ins has somewhere to land — read it then,
not before.

⚠️ The subject is not baseless: `_notes.md`'s own "Not yet swept" backlog still
carries *"Asteroid cave-in trigger — NOT the underground marsquake repeat
(asteroids are `Environment == "Asteroid"`, gate requires `"Underground"`); find
actual source."* That line stays live in `_notes.md`; only the empty index row
was archived.
