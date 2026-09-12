# Final menu registry read — temporary probe plan

Coordinator `/root`, 2026-09-12. Stale-probe gate CLEAN before this plan and
before each launch; this session declares only `97_StillNeededBootRead.lua`.
The retail boot logs a transient Saint inactive message followed by a save-heal
arming message. `ctx.heal()` changes the registry without logging a new applied
message. Read final registry directly at a settled main menu instead of treating
the last status-shaped log message as the final registry value.

SOURCE route: `Code/00_Core.lua:345` (heal) and `:645` (ListFixes); main-menu wait
pattern from the shipped TestKit 95_AutoRun and the existing co-run harness.
No colony, save loading/writing, suite, console input, account mutation or portal
call. One REAL-time thread, one watchdog, read-only registry enumeration and
ListFixes logging, then graceful `quit()`. F102 class/entity reads are included.
Boot statuses measure installation only; entity existence is not a freeze cure.

Parked payload, copied into TestKit Code only for the launched reading:

```lua
-- TEMPORARY: still-needed sweep, final menu registry read; no colony or saves.
CreateRealTimeThread(function()
  Sleep(1000)
  local deadline = RealTime() + 90000
  while not GetPreGameMainMenu() do
    if RealTime() >= deadline then
      ModLog("[STILLNEEDED] TIMEOUT waiting for menu")
      quit()
      return
    end
    Sleep(250)
  end
  Sleep(5000)
  local ok, err = pcall(function()
    ModLog("[STILLNEEDED] BEGIN final registry")
    local pack = rawget(_G, "SMRFixPack")
    if not pack then ModLog("[STILLNEEDED] MISSING fix pack"); return end
    pack.ListFixes()
    local total, active = 0, 0
    for _, id in ipairs(pack.order) do
      local entry = pack.fixes[id]
      total = total + 1
      if entry.status == "active" then active = active + 1 end
      ModLog("[STILLNEEDED] STATUS " .. tostring(id) .. " " .. tostring(entry.status))
    end
    ModLog("[STILLNEEDED] TOTAL " .. tostring(active) .. "/" .. tostring(total))
    ModLog("[STILLNEEDED] F102 entity=" .. tostring(SubsurfaceDepositPreciousMinerals.entity)
      .. " rare-sign-valid=" .. tostring(IsValidEntity("SignRareMineralsDeposit")))
    ModLog("[STILLNEEDED] END final registry")
  end)
  if not ok then ModLog("[STILLNEEDED] ERROR " .. tostring(err):gsub("%%", "%%%%")) end
  Sleep(2000)
  quit()
end)
```

Execution: [NEVER RUN] at plan creation. Arm through TestKit metadata code list,
read back exact source/list entry, parsecheck, declare marker sweep, launch retail
through Steam (without autorun), wait at most 90 seconds, archive flushed log,
restore TestKit metadata byte-for-byte and delete payload in result-recording
unit. Record final measurements in `RUNTIME.md` once the payload has run.
