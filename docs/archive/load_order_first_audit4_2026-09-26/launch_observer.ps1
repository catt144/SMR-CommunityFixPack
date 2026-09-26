# Unattended rehearsal of the 1325db5 sync observer on main (2026-09-26), precondition 1 of
# report s17. The payload and manifest are taken from the branch commit; an UNTRACKED copy
# of the payload with MODE unattended is parked in the main tree's payload folder (the
# manifest's park is relative and resolves against this working directory), armed into the
# real kit, launched, collected, disarmed; the kit's metadata is restored to HEAD and
# hash-compared; the parked copy is removed. No pack branch is checked out.
$ErrorActionPreference = "Stop"
$main = "B:\Dev\SMR\SMR-BugFixPack"
$kit = "B:\Dev\SMR\SMR-BugFixPack-TestKit"
$scratch = "C:\Users\stkot\AppData\Local\Temp\claude\b--Dev-SMR-SMR-BugFixPack\5b51c8ed-6fde-40ba-b43c-174519e23981\scratchpad\audit4"
$logs = Join-Path $env:APPDATA "Surviving Mars Relaunched\logs"
$utf8 = New-Object System.Text.UTF8Encoding($false)
$commit = "1325db54a0ec2a835b694eed8b1034817d08f948"

function Guard { if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { throw "Mars.exe is running; stop" } }
Guard
Set-Location $main
if ((& git branch --show-current) -ne "main") { throw "junction is not on main" }

$payload = (& git show ($commit + ":tools/arming/payloads/98_LoadFirstSync.lua.txt")) -join "`n"
$payload = $payload + "`n"
$count = ([regex]::Matches($payload, 'MODE = "sitting"')).Count
if ($count -ne 1) { throw "MODE literal count $count" }
$sha = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($utf8.GetBytes($payload))).Replace("-", "").ToLower()
Write-Output ("BRANCH payload sha256=" + $sha)
$parked = $payload.Replace('MODE = "sitting"', 'MODE = "unattended"')
$dst = Join-Path $main "tools\arming\payloads\98_LoadFirstSync.lua.txt"
[System.IO.File]::WriteAllText($dst, $parked, $utf8)
Write-Output ("PARKED " + $dst + " MODE=unattended sha256=" + (Get-FileHash $dst -Algorithm SHA256).Hash.ToLower())

$manifest = Join-Path $scratch "load-first-sync.json"
$mtext = (& git show ($commit + ":tools/arming/legs/load-first-sync.json")) -join "`n"
[System.IO.File]::WriteAllText($manifest, $mtext + "`n", $utf8)
Write-Output ("MANIFEST sha256=" + (Get-FileHash $manifest -Algorithm SHA256).Hash.ToLower())

& powershell -File (Join-Path $main "tools\arm_leg.ps1") -Manifest $manifest -Mode arm
if ($LASTEXITCODE -ne 0) { throw "arm failed exit $LASTEXITCODE" }
Write-Output "ARMED exit=0"
$armed = Join-Path $kit "Code\98_LoadFirstSync.lua"
Write-Output ("ARMED copy sha256=" + (Get-FileHash $armed -Algorithm SHA256).Hash.ToLower())

Guard
$before = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
$t0 = Get-Date
& "C:\Program Files (x86)\Steam\steam.exe" -applaunch 3215050
Write-Output ("LAUNCH steam -applaunch 3215050 at " + $t0.ToString("HH:mm:ss"))
$appeared = $false
for ($i = 0; $i -lt 90; $i++) { Start-Sleep -Seconds 1; if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { $appeared = $true; break } }
Write-Output ("MARS appeared=" + $appeared + " after " + [int]((Get-Date) - $t0).TotalSeconds + "s")
$exited = $false
for ($i = 0; $i -lt 240; $i++) { Start-Sleep -Seconds 1; if (-not (Get-Process -Name Mars -ErrorAction SilentlyContinue)) { $exited = $true; break } }
Write-Output ("MARS exited=" + $exited + " after " + [int]((Get-Date) - $t0).TotalSeconds + "s")
Start-Sleep -Seconds 3
$after = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
if ($before -and $after.Name -eq $before.Name) { Write-Output "WARNING no new log" }
$copy = Join-Path $scratch ("L13_observer_rehearsal_main_" + $after.Name)
Copy-Item $after.FullName $copy
Write-Output ("LOG " + $after.FullName + " -> " + $copy + " bytes=" + $after.Length)

& powershell -File (Join-Path $main "tools\arm_leg.ps1") -Manifest $manifest -Mode disarm
Write-Output ("DISARM exit=" + $LASTEXITCODE)
Push-Location $kit
& git checkout -- metadata.lua
$head = (& git rev-parse HEAD:metadata.lua)
$work = (& git hash-object metadata.lua)
Pop-Location
Write-Output ("KIT metadata HEAD=" + $head + " worktree=" + $work + " match=" + ($head -eq $work))
Write-Output ("KIT status: " + ((& git -C $kit status --short) -join " | "))
Remove-Item $dst
Write-Output ("REMOVED parked copy; main status: " + ((& git -C $main status --short) -join " | "))
