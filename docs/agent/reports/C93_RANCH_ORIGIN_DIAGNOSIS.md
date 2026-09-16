# C93 — Outside Ranch Origin-pile diagnosis

## Outcome

**C93's ranch symptom is reproduced and its immediate mechanism is identified.** The
owner's `OpenPasture(4396)` has nine live `MixedPoolStockpile` objects. Six are attached
to the entity's real `Resourcepile1`–`Resourcepile6` spots; three are attached to
`Origin`. During the attended production-cycle run, all six real-spot pickup approaches
returned `true` and all three Origin-pile approaches returned `false`.

The Origin piles held exactly the centre-stack reading already visible in the toolkit:
81 resource units total, split 46 Food and 35 Meat. This is placement-specific, not
livestock- or resource-specific: the reachable piles accepted and released Cheese, Food
and Meat during the run, while both Food and Meat were stranded in the Origin set.

No pack fix was built. The fired brief's proposed generic entity guard targets a separate
error source and cannot move these crates: every ranch pile has the
`ResourcePlatform` entity. The next C93 build must target the nine-declared/six-real spot
mismatch and must recover already-affected saves; that is a new design scope, not licence
to improvise a pile migration in this sitting.

## Evidence

Attended log: [C93 ranch probe boot](../../archive/logs/C93_ranch_probe_Mars.exe-20260916-11.52.38-6a91a190.log),
game 1.1.0.403908 / build `6a91a190`. The archived copy and the source log measured
4,193,863 bytes and the same SHA-256,
`BE69C75CCF4CEEFB0655C12D1E202D43F3591F0DCB24B039673BA9C9659398AA`.

The counting command selected only the ModLog copy of each probe line, excluding the
intentional duplicate plain-print line:

```powershell
$probeLines = Select-String -LiteralPath $log -Pattern '^\[mod\] \[SMRTest\] C93_RANCH'
```

`[RAN 2026-09-16, log C93_ranch_probe_Mars.exe-20260916-11.52.38-6a91a190.log]`

| measurement | result | reconciliation |
|---|---:|---|
| unique piles on `OpenPasture(4396)` | 9 | 6 real-spot + 3 Origin = 9 |
| completed pickup approaches | 9 | 6 `true` + 3 `false` = 9 |
| Origin stored amount | 81,000 scaled | 46,000 Food + 35,000 Meat = 81,000 |

At load, the six real-spot piles were empty. The three Origin piles each held 27,000
scaled units. Their three pickup attempts preserved both stored and supply amounts and
returned `false`. After the production cycle, the six real-spot piles received output;
their pickup attempts returned `true`. The owner's independent screen observation was
that a large Food load was carried to outside depots in this run.

## Source join

**SOURCE, installed 1.1.0.403908:** `OpenPastureBase` declares nine stockpile names for
each producer (`Lua/Units/Animals.lua:1108-1114`). Both creation routes convert a missing
named spot to `Origin`: `StockpileController:CreateStockpiles` prints on the branch
(`Lua/Buildings/StockpileController.lua:102-107`), while
`SavegameFixups.SharePastureStockpilePools2` performs the same fallback silently
(`Lua/Units/Animals.lua:1430-1436`). The measured final state is exactly that output
shape. The log does not distinguish which of those two routes originally created these
three persisted piles.

This also corrects C93's old control. Zero `doesn't have spot` lines proves only that the
printing creation branch did not run in this boot. It cannot refute persisted Origin
piles or the silent pasture fixup. The direct control is each live pile's
`GetAttachSpot()`/parent spot name plus an observed pickup result.

## Scope decision and stop

The first, entity-only probe named `MegaMall` requesters. The owner identified a
mall-related mod as the likely source and explicitly instructed this investigation to
ignore those targets. No MegaMall defect was filed and no generic `Unit` guard was built.
That ruling is condition-scoped to separating the mall-mod diagnostic noise from C93;
it makes no claim about a clean vanilla mall.

The temporary probes were removed immediately after their runs. Final sweep: zero
`TEMPORARY`/`C93_RANCH` hits across pack and TestKit `Code/`; the TestKit worktree returned
clean. No player reply was drafted or queued.

Executed model recorded from the session transcript: **GPT-5 (Codex)**.
