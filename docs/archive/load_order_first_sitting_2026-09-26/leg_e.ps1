# Leg E of the LoadFirst sitting (2026-09-26): disarm the sitting instrument, restore the
# owner's saved order with the branch's set leg on the sitting worktree (junction still on
# it), repoint the junction at the main tree, read the order back with the read leg on a
# fresh boot, disarm, restore the kit's metadata and hash-compare. Payloads are parked as
# copies of the 1325db5 blobs; manifests are those blobs with park redirected to scratch.
$ErrorActionPreference = "Stop"
$main = "B:\Dev\SMR\SMR-BugFixPack"
$sitting = "B:\Dev\SMR\SMR-FixPack-sitting"
$kit = "B:\Dev\SMR\SMR-BugFixPack-TestKit"
$scratch = "C:\Users\stkot\AppData\Local\Temp\claude\b--Dev-SMR-SMR-BugFixPack\5b51c8ed-6fde-40ba-b43c-174519e23981\scratchpad\audit4"
$park = Join-Path $scratch "sitting_park"
$logs = Join-Path $env:APPDATA "Surviving Mars Relaunched\logs"
$junction = Join-Path $env:APPDATA "Surviving Mars Relaunched\Mods\SMR-BugFixPack"
$utf8 = New-Object System.Text.UTF8Encoding($false)
$commit = "1325db54a0ec2a835b694eed8b1034817d08f948"
$armScript = Join-Path $sitting "tools\arm_leg.ps1"

function Guard { if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { throw "Mars.exe is running; stop" } }
function KitCheck {
  Push-Location $kit; & git checkout -- metadata.lua
  $h = (& git rev-parse HEAD:metadata.lua); $w = (& git hash-object metadata.lua); Pop-Location
  Write-Output ("KIT metadata HEAD=" + $h + " worktree=" + $w + " match=" + ($h -eq $w) + " status=[" + ((& git -C $kit status --short) -join " | ") + "]")
}
function Arm($manifest) {
  & powershell -File $armScript -Manifest $manifest -Mode arm | Select-String "RESULT|GATE FAIL|WROTE"
  if ($LASTEXITCODE -ne 0) { throw "arm failed exit $LASTEXITCODE" }
}
function Disarm($manifest) {
  & powershell -File $armScript -Manifest $manifest -Mode disarm | Select-String "RESULT|GATE FAIL|DELETED"
  Write-Output ("DISARM exit=" + $LASTEXITCODE)
  KitCheck
}
function ParkBranch($name) {
  $text = ((& git -C $main show ($commit + ":tools/arming/payloads/" + $name)) -join "`n") + "`n"
  $dst = Join-Path $park $name
  [System.IO.File]::WriteAllText($dst, $text, $utf8)
  Write-Output ("PARKED " + $name + " sha256=" + (Get-FileHash $dst -Algorithm SHA256).Hash.ToLower())
}
function ManifestFromBranch($name) {
  $text = (& git -C $main show ($commit + ":tools/arming/legs/" + $name)) -join "`n"
  $text = $text.Replace('"park": "B:\\Dev\\SMR\\SMR-BugFixPack\\tools\\arming\\payloads"', '"park": "' + $park.Replace("\", "\\") + '"')
  if ($text -notmatch "sitting_park") { throw "park redirect failed for $name" }
  $dst = Join-Path $scratch $name
  [System.IO.File]::WriteAllText($dst, $text + "`n", $utf8)
  return $dst
}
function Launch($tag) {
  Guard
  $before = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
  $t0 = Get-Date
  & "C:\Program Files (x86)\Steam\steam.exe" -applaunch 3215050
  $appeared = $false
  for ($i = 0; $i -lt 90; $i++) { Start-Sleep -Seconds 1; if (Get-Process -Name Mars -ErrorAction SilentlyContinue) { $appeared = $true; break } }
  $exited = $false
  for ($i = 0; $i -lt 240; $i++) { Start-Sleep -Seconds 1; if (-not (Get-Process -Name Mars -ErrorAction SilentlyContinue)) { $exited = $true; break } }
  Start-Sleep -Seconds 3
  $after = Get-ChildItem $logs -Filter "Mars.exe-*.log" | Sort-Object LastWriteTime | Select-Object -Last 1
  if ($before -and $after.Name -eq $before.Name) { throw "no new log for $tag" }
  $copy = Join-Path $scratch ($tag + "_" + $after.Name)
  Copy-Item $after.FullName $copy
  Write-Output ("LAUNCH " + $tag + " at " + $t0.ToString("HH:mm:ss") + " appeared=" + $appeared + " exited=" + $exited + " seconds=" + [int]((Get-Date) - $t0).TotalSeconds + " log=" + $after.Name)
  return $copy
}

Guard
$j = Get-Item $junction
Write-Output ("JUNCTION before: " + ($j.Target -join ";"))
if (($j.Target -join ";") -ne $sitting) { throw "junction is not on the sitting worktree" }

# 1. disarm the sitting instrument
Disarm (Join-Path $scratch "load-first-sitting.json")

# 2. set leg on the branch: ORDER literal in the branch blob is the owner's order
ParkBranch "98_LoadFirstSet.lua.txt"
$order = Select-String -Path (Join-Path $park "98_LoadFirstSet.lua.txt") -Pattern '^\s*"SMR_' | ForEach-Object { $_.Line.Trim().Trim(',').Trim('"') }
Write-Output ("ORDER literal: " + ($order -join ","))
$setManifest = ManifestFromBranch "load-first-set.json"
Arm $setManifest
$log1 = Launch "L14_restore_branch"
Select-String -Path $log1 -Pattern "LOADFIRST-SET\]|Loaded mod items|LoadFirst:|LUA ERROR" | ForEach-Object { $_.LineNumber.ToString() + ":" + $_.Line.Substring(0, [Math]::Min(230, $_.Line.Length)) }
Disarm $setManifest

# 3. junction back to the main tree
Guard
cmd /c rmdir "$junction"
if (Test-Path $junction) { throw "junction still present" }
cmd /c mklink /J "$junction" "$main" | Out-Null
$j = Get-Item $junction
Write-Output ("JUNCTION after: linktype=" + $j.LinkType + " target=" + ($j.Target -join ";") + " main branch=" + (& git -C $main branch --show-current))

# 4. read leg on main
ParkBranch "98_LoadFirstRead.lua.txt"
$readManifest = ManifestFromBranch "load-first-read.json"
Arm $readManifest
$log2 = Launch "L15_readback_main"
Select-String -Path $log2 -Pattern "LOADFIRST\]|Loaded mod items|LoadFirst:|LUA ERROR" | ForEach-Object { $_.LineNumber.ToString() + ":" + $_.Line.Substring(0, [Math]::Min(230, $_.Line.Length)) }
Disarm $readManifest
Write-Output ("MAIN status: [" + ((& git -C $main status --short) -join " | ") + "]")
