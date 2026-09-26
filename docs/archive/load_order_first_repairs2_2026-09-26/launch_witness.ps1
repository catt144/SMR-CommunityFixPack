# Unattended LoadFirst sync-witness launch on main (2026-09-26): arm the kit with the
# sync payload in MODE unattended, launch, wait for the exit, copy the log, disarm,
# restore the kit's metadata to HEAD and compare hashes. No pack branch is checked out.
$ErrorActionPreference = "Stop"
$wt = "B:\Dev\SMR\SMR-FixPack-loadfirst"
$main = "B:\Dev\SMR\SMR-BugFixPack"
$kit = "B:\Dev\SMR\SMR-BugFixPack-TestKit"
$scratch = "C:\Users\stkot\AppData\Local\Temp\claude\b--Dev-SMR-SMR-BugFixPack\5b51c8ed-6fde-40ba-b43c-174519e23981\scratchpad\repairs2"
$logs = Join-Path $env:APPDATA "Surviving Mars Relaunched\logs"

if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { throw "Mars.exe is running; not launching" }

# the leg's park is the main tree's payload folder; the payload lives on the branch, so
# park an UNTRACKED copy with MODE swapped for this launch only
$src = Join-Path $wt "tools\arming\payloads\98_LoadFirstSync.lua.txt"
$dst = Join-Path $main "tools\arming\payloads\98_LoadFirstSync.lua.txt"
$text = [System.IO.File]::ReadAllText($src)
$count = ([regex]::Matches($text, 'MODE = "sitting"')).Count
if ($count -ne 1) { throw "MODE literal count $count" }
$text = $text.Replace('MODE = "sitting"', 'MODE = "unattended"')
[System.IO.File]::WriteAllText($dst, $text, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ("PARKED " + $dst + " MODE=unattended sha256=" + (Get-FileHash $dst -Algorithm SHA256).Hash.ToLower())

$manifest = Join-Path $wt "tools\arming\legs\load-first-sync.json"
& powershell -File (Join-Path $wt "tools\arm_leg.ps1") -Manifest $manifest -Mode arm
if ($LASTEXITCODE -ne 0) { throw "arm failed exit $LASTEXITCODE" }
Write-Output "ARMED exit=0"

$before = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
$t0 = Get-Date
& "C:\Program Files (x86)\Steam\steam.exe" -applaunch 3215050
Write-Output ("LAUNCH steam -applaunch 3215050 at " + $t0.ToString("HH:mm:ss"))
$appeared = $false
for ($i = 0; $i -lt 90; $i++) {
  Start-Sleep -Seconds 1
  if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { $appeared = $true; break }
}
Write-Output ("MARS appeared=" + $appeared + " after " + [int]((Get-Date) - $t0).TotalSeconds + "s")
$exited = $false
for ($i = 0; $i -lt 240; $i++) {
  Start-Sleep -Seconds 1
  if (-not (Get-Process -Name Mars -ErrorAction SilentlyContinue)) { $exited = $true; break }
}
Write-Output ("MARS exited=" + $exited + " after " + [int]((Get-Date) - $t0).TotalSeconds + "s")
Start-Sleep -Seconds 3
$after = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
if ($before -and $after.Name -eq $before.Name) { Write-Output "WARNING no new log" }
$copy = Join-Path $scratch ("L12_sync_witness_main_" + $after.Name)
Copy-Item $after.FullName $copy
Write-Output ("LOG " + $after.FullName + " -> " + $copy + " bytes=" + $after.Length)

& powershell -File (Join-Path $wt "tools\arm_leg.ps1") -Manifest $manifest -Mode disarm
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
