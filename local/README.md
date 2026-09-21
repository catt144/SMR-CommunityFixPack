# local/

Git-ignored home for DURABLE material that belongs to THIS tree but must not
be committed — large binaries, logs, evidence a report links to. Owner
decision, 2026-09-21: material that belongs to one tree lives in that tree
(the exceptions are things every SMR mod uses — the TestKit and Assets
repos, the archived game source, the Workshop mod corpus, the owner's
screen-capture drop folder — see docs/README.md "Outside the repo"). An
in-tree home with no gate becomes a dumping ground, so this folder gets one.

Unlike `scratch/` (working space, swept at 14 days by the eviction prompt),
`local/` is **not swept**. Nothing here ages out on its own; it leaves when
its row's condition is met.

**The gate: one row per subfolder, below.** No row, no folder — `doccheck`
reports a subfolder with no row, and a row that names a folder not on disk,
both RED. Nothing in this table is itself a record; the record is the entry
or report in the citing column, or git history.

| folder | holds | cited by | ends when |
|---|---|---|---|
| `c92-placement/` | Icon contact sheets (research-image comparisons, law/Thomas controls, Industry/Hi-Tech candidates) and a couple of scratch text files from the C92 icon hunt | [`agent/reports/C92_PLACEMENT.md`](../docs/agent/reports/C92_PLACEMENT.md), [`agent/reports/c92-placement/ICON_HUNT.md`](../docs/agent/reports/c92-placement/ICON_HUNT.md) | C92 ships or is dropped — status is `cand` (build authorised, shipping held), so the sheets stay until then |
| `c95-place/` | Game logs and a save-inventory JSON from the C95 placement instrument runs | [`agent/reports/C95_PLACE_HOME_BUILD.md`](../docs/agent/reports/C95_PLACE_HOME_BUILD.md) | Never on a fixed date — C95 is `tested-attended` and its report says the instrument history is kept here |

