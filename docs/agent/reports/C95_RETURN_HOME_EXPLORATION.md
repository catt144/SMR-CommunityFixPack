# C95 return-home exploration

In progress. The owner authorized this exploration on 2026-09-16; nothing here
authorizes shipping or changing the v11 exclusion.

## Live work list

- IN PROGRESS — Trace and compare repairs; commit the source findings with scoped checks.
- PENDING — Build an unshipped prototype and exercise desk and retail paths; commit evidence.
- PENDING — Finish this report, rewrite ck200, consume the prompt and verify the final commit.

## Source finding that changes the design

The brief's walking-only description stops too early. Both return receivers issue
`unit:SetCommand("ReturnFromExpedition", rocket, home)`. The declaring
`Colonist:SetCommand` in `Lua/Units/ColonistTransport.lua:381-502` first invokes
`ReturnFromExpedition_TransportDestination` (:204-207), which sets `arriving`.
It can book a train through `StartTransport` (:354-371) and run
`DisembarkOnArrival` (:321-352), then `GoToStation`, without entering the
`ReturnFromExpedition` body at all. This is source evidence, not a live result.

The smallest candidate therefore widens the synchronous home selector's input
for a valid, reserved habitat with a verified walking or train route. The shipped
command dispatcher can perform the journey. A separate concern is employment
while the bed is reserved: the normal picker consults actual residence, not the
reserved habitat. The train branch's cleanup also differs from the walking branch.
These require tests before selecting the repair.

The fallback reservation can destroy the old-home reference *before* the return
command: `Residence:ReserveResidence` calls `CancelResidenceReservation`, whose
body clears `expedition_residence` (`Residence.lua:290-307,385-399`). A wrapper on
the return command alone is consequently too late to recover that identity.

Evidence commands at HEAD `a0f9e1dee67c9034a7d7436c58760f84a4b69990`:

```text
python tools/luafn.py Lua/CargoTransporterNew.lua 'function CargoTransporterNew:UnloadPassengers'
python tools/luafn.py Lua/Buildings/RocketBase.lua 'function RocketBase:Disembark'
python tools/luafn.py Lua/Units/ColonistTransport.lua 'function Colonist:SetCommand\(' 'function Colonist:DisembarkOnArrival\('
python tools/luafn.py Lua/Buildings/Residence.lua 'function Residence:(ReserveResidence|CancelResidenceReservation)\('
```

The installed fingerprint reports Steam build 24995074. Its date-bearing EF-107
group is labeled MOVED despite naming 1.1.0.403908; the targeted source read above
uses the installed tree, rather than treating that parser label as an update.

## Probe hygiene

Initial `rg -n TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/` returned no matches.
`tasklist /FI "IMAGENAME eq Mars.exe"` found no running game. These are preflight
observations only; repeat the process check immediately before a launch.

## Outstanding evidence

No prototype result or live return is claimed yet. Far habitat, all-habitat colony,
habitat beside a dome, ordinary dome residents, save/load and removal remain open.

Executed model: GPT-6 (Codex), as supplied by this session's transcript. No subagents.
