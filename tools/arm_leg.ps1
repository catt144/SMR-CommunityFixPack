# arm_leg.ps1 - THE canonical arming harness for unattended in-game measurement
# legs. One script, manifest-driven. Replaces the copy-forward lineage:
#
#   d13-rescue/RS_ARM.ps1   (grave 6b75e11)
#     -> combined-sitting/CS_ARM.ps1
#   c47-farm/C47_ARM.ps1    (grave fd1102a)
#     -> c48-brake/C48B_ARM.ps1 -> c48-pairing/C48P_ARM.ps1
#
# Three generations rediscovered the same rules from graves. The rules, and why
# each exists, are in docs/agent/prompts/arming/README.md. The short version:
#
#   C11  arming is a FILE, never an inline one-liner (an inline edit's quoting
#        was mangled once and the game launched UNARMED).
#   C11a never pipe this script's output through Select-Object - a piped
#        consumer terminates the upstream pipeline and can kill the script
#        before its write executes. Nothing here is piped.
#   G5   after writing, EVERY piece is read BACK OFF DISK, and a missing piece
#        OR a piece listed twice is a failure. The double-listing half is not
#        theoretical: d13-rescue cell r1 was armed on top of armed-r0, metadata
#        listed the payload twice, it executed twice, and two legs raced.
#   S3   ASCII-only payload bodies; metadata is written with NO BOM (PS 5.1's
#        Set-Content/Out-File will give you a BOM and CRLF - this uses
#        UTF8Encoding($false) via WriteAllText. NOT WriteAllLines: it
#        joins with Environment.NewLine and would write CRLF.
#
# [STOP] PAYLOADS GO IN THE TEST KIT, NEVER IN THE FIX PACK (owner ruling 110: "the
#    pack ships ZERO diagnostic code"). This script only ever writes under the
#    kit repo.
#
# [STOP] AN ARMED TREE CANNOT BE COMMITTED, BY DESIGN. Every payload must carry a
#    TEMPORARY marker, and tools/doccheck.py's temporary_sweep() returns
#    `not hits` - so a TEMPORARY marker anywhere in Code/ or the kit's Code/
#    makes doccheck RED and the pre-commit hook blocks. Disarm, then commit.
#
# [*] FIXED IN THIS REWRITE - a latent false GREEN inherited from all three
#    ancestors. They asked "is the payload listed?" with a raw substring match
#    over the whole metadata file, e.g.
#        $m -match [regex]::Escape('"Code/98_C48Brake.lua"')
#    That matches a COMMENTED-OUT line too - and commenting a line out is the
#    kit's own disarm convention (see 97_ForceInactive in its metadata). So the
#    gate could confirm a payload was armed when it was inert and would never
#    load. This version parses the code list line by line and ignores any line
#    whose first non-whitespace is `--`. Check the thing, not its label.
#
#   Usage:
#     .\arm_leg.ps1 -Manifest <leg.json> -Mode arm
#     .\arm_leg.ps1 -Manifest <leg.json> -Mode disarm
#     .\arm_leg.ps1 -Manifest <leg.json> -Mode verify    # gates only, no write
#     .\arm_leg.ps1 -SelfTest                            # the falsifier
#
# Exit code is 0 only when every gate passed.

[CmdletBinding(DefaultParameterSetName = "Run")]
param(
  [Parameter(Mandatory = $true, ParameterSetName = "Run")]
  [string]$Manifest,

  [Parameter(Mandatory = $true, ParameterSetName = "Run")]
  [ValidateSet("arm", "disarm", "verify")]
  [string]$Mode,

  [Parameter(Mandatory = $true, ParameterSetName = "SelfTest")]
  [switch]$SelfTest
)

$ErrorActionPreference = "Stop"
$script:noBom = New-Object System.Text.UTF8Encoding($false)
$script:fail = $false
$script:insertOk = $false
$script:selfTestExit = 1

# S3, the half that bit every ancestor: [System.IO.File]::WriteAllLines joins
# with Environment.NewLine, which is CRLF on Windows -- so all three ancestor
# scripts silently converted the kit metadata.lua (LF, no BOM) to CRLF on every
# arm and disarm. This writer is the only place metadata is written here. The
# self-test leg "metadata written with no BOM, LF only" is what caught it, which
# is why that leg exists.
function Write-LinesLf([string]$path, $lines) {
  $joined = ($lines -join "`n")
  if ($joined -ne "" -and -not $joined.EndsWith("`n")) { $joined = $joined + "`n" }
  [System.IO.File]::WriteAllText($path, $joined, $script:noBom)
}

function Say($text) { Write-Output $text }
function GateOk($text) { Write-Output ("GATE OK       " + $text) }
function GateFail($text) { Write-Output ("GATE FAIL:    " + $text); $script:fail = $true }

# --- metadata code list, comment-aware ---------------------------------------
# Returns the ACTIVE "Code/..." entries only. A line whose first non-whitespace
# is `--` is disarmed and must not count as listed (see the note at the top).
function Get-ActiveCodeEntries([string]$metaPath) {
  $active = New-Object System.Collections.Generic.List[string]
  foreach ($line in [System.IO.File]::ReadAllLines($metaPath)) {
    if ($line -match '^\s*--') { continue }
    $m = [regex]::Match($line, '"(Code/[^"]+)"')
    if ($m.Success) { $active.Add($m.Groups[1].Value) }
  }
  return $active
}

function Count-Active([string]$metaPath, [string]$entry) {
  $n = 0
  foreach ($e in Get-ActiveCodeEntries $metaPath) {
    if ($e -eq $entry) { $n = $n + 1 }
  }
  return $n
}

# --- strip: remove this leg's own lines, armed or commented ------------------
function Strip-LegLines([string]$metaPath, [string]$stripPattern, [string[]]$excludeEntries) {
  $lines = [System.IO.File]::ReadAllLines($metaPath)
  $kept = New-Object System.Collections.Generic.List[string]
  foreach ($line in $lines) {
    $drop = $false
    if ($stripPattern -ne "" -and $line -match $stripPattern) { $drop = $true }
    foreach ($ex in $excludeEntries) {
      if ($line -match [regex]::Escape('"' + $ex + '"')) { $drop = $true }
    }
    if (-not $drop) { $kept.Add($line) }
  }
  Write-LinesLf $metaPath $kept
  return ($lines.Count - $kept.Count)
}

function Insert-Entries([string]$metaPath, [string[]]$entries, [string]$anchorAfter, [string]$legTag) {
  $lines = [System.IO.File]::ReadAllLines($metaPath)
  $out = New-Object System.Collections.Generic.List[string]
  $inserted = $false

  if ($anchorAfter -ne "") {
    foreach ($line in $lines) {
      $out.Add($line)
      if (-not $inserted -and $line -match [regex]::Escape($anchorAfter)) {
        foreach ($e in $entries) { $out.Add(("`t`t`"" + $e + "`",  -- TEMPORARY " + $legTag)) }
        $inserted = $true
      }
    }
    if (-not $inserted) {
      GateFail ("anchorAfter '" + $anchorAfter + "' not found in metadata - refusing to guess a load position")
      $script:insertOk = $false
      return
    }
  } else {
    # No anchor named: insert after the LAST active Code/ entry, so the payload
    # loads after everything the kit already loads.
    $lastIdx = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
      if ($lines[$i] -notmatch '^\s*--' -and $lines[$i] -match '"Code/[^"]+"') { $lastIdx = $i }
    }
    if ($lastIdx -lt 0) {
      GateFail "no active Code/ entry found to anchor against"
      $script:insertOk = $false
      return
    }
    for ($i = 0; $i -lt $lines.Count; $i++) {
      $out.Add($lines[$i])
      if ($i -eq $lastIdx) {
        foreach ($e in $entries) { $out.Add(("`t`t`"" + $e + "`",  -- TEMPORARY " + $legTag)) }
      }
    }
  }
  Write-LinesLf $metaPath $out
  $script:insertOk = $true
}

# --- the gates ---------------------------------------------------------------
function Invoke-Gates($cfg, [string]$kit, [string]$metaPath, [bool]$armed) {

  # G5a - anything declared permanent must survive every mode.
  foreach ($p in $cfg.permanent) {
    if ((Count-Active $metaPath $p) -ge 1) { GateOk ("permanent still listed: " + $p) }
    else { GateFail ("permanent no longer listed: " + $p) }
    if (Test-Path -LiteralPath (Join-Path $kit $p)) { GateOk ("permanent on disk:     " + $p) }
    else { GateFail ("permanent missing from disk: " + $p) }
  }

  # G5b - anything declared mustNotBeListed stays inert (comment-aware, so a
  # commented-out line correctly reads as NOT listed).
  foreach ($x in $cfg.mustNotBeListed) {
    if ((Count-Active $metaPath $x) -eq 0) { GateOk ("not listed (inert):    " + $x) }
    else { GateFail ($x + " is ACTIVELY listed - " + $cfg.mustNotBeListedWhy) }
  }

  foreach ($pl in $cfg.payloads) {
    $entry = "Code/" + $pl.dst
    $onDisk = Join-Path $kit (Join-Path "Code" $pl.dst)

    if (-not $armed) {
      if (Test-Path -LiteralPath $onDisk) { GateFail ("disarm left the payload on disk: " + $pl.dst) }
      else { GateOk ("payload gone from disk: " + $pl.dst) }
      if ((Count-Active $metaPath $entry) -eq 0) { GateOk ("payload unlisted:      " + $pl.dst) }
      else { GateFail ("disarm left the payload listed: " + $pl.dst) }
      continue
    }

    if (-not (Test-Path -LiteralPath $onDisk)) { GateFail ("payload missing from disk: " + $pl.dst); continue }
    GateOk ("payload on disk:       " + $pl.dst)

    $n = Count-Active $metaPath $entry
    if ($n -eq 1) { GateOk ("payload listed ONCE:   " + $pl.dst) }
    elseif ($n -eq 0) { GateFail ("payload not actively listed (commented out?): " + $pl.dst) }
    else { GateFail ("payload listed " + $n + " TIMES - it would execute " + $n + "x and race itself: " + $pl.dst) }

    $text = [System.IO.File]::ReadAllText($onDisk)

    if ($text -match "TEMPORARY") { GateOk ("TEMPORARY marker:      " + $pl.dst) }
    else { GateFail ("no TEMPORARY marker in " + $pl.dst + " - doccheck could not stop this being committed") }

    # S3: printable ASCII plus tab/LF/CR. Built with character
    # arithmetic on purpose - no escape sequence to be eaten. The first
    # attempt at this line took a NUL byte where an escape was meant and
    # the range silently started at zero, which is the same trap that put a
    # 0x01 in a prompt and a 0x08 in GAME_1_1_0_AUDIT 2c.
    $nonAscii = 0
    foreach ($ch in $text.ToCharArray()) {
      $c = [int]$ch
      if ($c -gt 126) { $nonAscii = $nonAscii + 1; continue }
      if ($c -lt 32 -and $c -ne 9 -and $c -ne 10 -and $c -ne 13) {
        $nonAscii = $nonAscii + 1
      }
    }
    if ($nonAscii -eq 0) { GateOk ("S3 ASCII-only body:    " + $pl.dst) }
    else { GateFail ("S3: " + $nonAscii + " non-ASCII byte(s) in " + $pl.dst) }

    # Comment-stripped view, so a banned call named only in a comment is not a
    # false positive and a real one cannot hide behind an OnMsg name.
    $code = ($text -split "`r?`n" | ForEach-Object { ($_ -replace '--.*$', '') }) -join "`n"
    $code = $code -replace 'OnMsg\.[A-Za-z_]\w*', 'OnMsgHandler'

    if ($pl.selfDrives) {
      if ($cfg.bootSymbol -ne "" -and $code -match ('(?m)^\s*' + [regex]::Escape($cfg.bootSymbol) + '\s*\(')) {
        GateOk ("self-drives:           " + $cfg.bootSymbol + "() at file scope")
      } else {
        GateFail ("payload does not call " + $cfg.bootSymbol + "() at file scope - an unattended leg that never starts measures nothing")
      }
      if ($code -match 'quit\s*\(') { GateOk ("quits the process:     " + $pl.dst) }
      else { GateFail ($pl.dst + " never calls quit() - the rig would sit at the menu forever") }
    } elseif ($cfg.bootSymbol -ne "") {
      # The inverse, inherited from CS_ARM: a LIBRARY payload must NOT drive
      # itself. Two flows at file scope race, and the loser's measurements are
      # silently interleaved with the winner's.
      if ($code -match ('(?m)^\s*' + [regex]::Escape($cfg.bootSymbol) + '\s*\(')) {
        GateFail ($pl.dst + " calls " + $cfg.bootSymbol + "() at file scope but is not the driver - two flows would race")
      } else {
        GateOk ("library, does not drive: " + $pl.dst)
      }
    }

    foreach ($bad in $cfg.bannedPatterns) {
      if ($code -match $bad) { GateFail ("banned pattern /" + $bad + "/ present in " + $pl.dst) }
    }
    if ($cfg.bannedPatterns.Count -gt 0) { GateOk ("banned-pattern scan:   " + $pl.dst) }
  }

  if (-not $armed) { return }

  # THE DECLARED-MUTATION GATE (inherited from C47_ARM/C48B_ARM). A leg that
  # mutates state must SAY what it mutates, label it, and be able to restore it.
  # A payload missing these is either inert or smuggling - and an inert payload
  # that still launches the game is the expensive failure, because it looks like
  # a clean run that measured nothing.
  if ($cfg.requiredPresent.Count -gt 0) {
    $allText = ""
    foreach ($pl in $cfg.payloads) {
      $allText = $allText + [System.IO.File]::ReadAllText((Join-Path $kit (Join-Path "Code" $pl.dst))) + "`n"
    }
    foreach ($need in $cfg.requiredPresent) {
      if ($allText -match [regex]::Escape($need)) { GateOk ("declared content present: " + $need) }
      else { GateFail ("declared content MISSING: " + $need) }
    }
  }

  # THE SYMBOL-RESOLUTION GATE (the ancestors' "G1 cross-check", generalised off
  # the hard-coded C47 namespace). Every <ns>.Name USED anywhere in the leg must
  # be DEFINED somewhere in the leg. This is the class no parser can see: the Lua
  # compiles, then indexes a nil at run time and the leg dies mid-measurement.
  if ($cfg.symbolNamespace -ne "") {
    $ns = [regex]::Escape($cfg.symbolNamespace)
    $joined = ""
    foreach ($pl in $cfg.payloads) {
      $joined = $joined + [System.IO.File]::ReadAllText((Join-Path $kit (Join-Path "Code" $pl.dst))) + "`n"
    }
    $live = ($joined -split "`r?`n" | ForEach-Object { ($_ -replace '--.*$', '') }) -join "`n"
    $defined = @{}
    foreach ($m in [regex]::Matches($live, '(?m)^\s*function\s+' + $ns + '\.([A-Za-z_]\w*)')) { $defined[$m.Groups[1].Value] = $true }
    foreach ($m in [regex]::Matches($live, '(?m)^\s*' + $ns + '\.([A-Za-z_]\w*)\s*=')) { $defined[$m.Groups[1].Value] = $true }
    $used = @{}
    foreach ($m in [regex]::Matches($live, $ns + '\.([A-Za-z_]\w*)')) { $used[$m.Groups[1].Value] = $true }
    $unresolved = @()
    foreach ($k in $used.Keys) { if (-not $defined.ContainsKey($k)) { $unresolved += $k } }
    if ($unresolved.Count -gt 0) {
      GateFail ("unresolved " + $cfg.symbolNamespace + ".* name(s): " + (($unresolved | Sort-Object) -join ", ") + " - these index a nil at run time")
    } else {
      GateOk ("all " + $used.Count + " " + $cfg.symbolNamespace + ".* name(s) resolve")
    }
  }
}

# --- self-test (the falsifier) ----------------------------------------------
# Every gate must be SEEN to fire on a rigged case and seen NOT to fire on a
# clean one, or this script is a comment.
function Invoke-SelfTest {
  $root = Join-Path $env:TEMP ("arm_leg_selftest_" + [guid]::NewGuid().ToString("N").Substring(0, 8))
  $kit = Join-Path $root "kit"
  $park = Join-Path $root "park"
  New-Item -ItemType Directory -Path (Join-Path $kit "Code") -Force | Out-Null
  New-Item -ItemType Directory -Path $park -Force | Out-Null
  $meta = Join-Path $kit "metadata.lua"
  $legs = 0
  $bad = New-Object System.Collections.Generic.List[string]

  function Reset-Fixture {
    $body = @(
      "return {",
      "`tcode = {",
      "`t`t`"Code/00_TestCore.lua`",",
      "`t`t`"Code/61_Probes_Wave11.lua`",",
      "`t`t-- `"Code/96_AutoRunFlag.lua`",  -- DISARMED",
      "`t`t`"Code/99_FixtureCarry.lua`",",
      "`t},",
      "}"
    )
    Write-LinesLf $meta $body
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\00_TestCore.lua"), "-- core")
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\61_Probes_Wave11.lua"), "-- permanent")
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\99_FixtureCarry.lua"), "-- fixture")
  }

  function Check($label, [bool]$expectFail, [scriptblock]$body) {
    $script:fail = $false
    & $body | Out-Null
    $got = $script:fail
    $ok = ($got -eq $expectFail)
    $verdict = "PASS"
    if (-not $ok) { $verdict = "*** FAIL ***" }
    Write-Output ("  {0,-46} fired={1,-5} want={2,-5} {3}" -f $label, $got, $expectFail, $verdict)
    if (-not $ok) { $bad.Add($label) }
  }

  $payloadText = "-- TEMPORARY selftest" + "`n" + "T.Boot()" + "`n" + "quit()" + "`n"
  [System.IO.File]::WriteAllText((Join-Path $park "98_Probe.lua.txt"), $payloadText)

  $cfg = [pscustomobject]@{
    leg = "selftest"; park = $park; kit = $kit
    stripPattern = 'Code/98_Probe'
    anchorAfter = "99_FixtureCarry.lua"
    bootSymbol = "T.Boot"
    permanent = @("Code/61_Probes_Wave11.lua")
    mustNotBeListed = @("Code/96_AutoRunFlag.lua")
    mustNotBeListedWhy = "it would start a NEW COLONY and race this payload"
    bannedPatterns = @('SaveGame\s*\(')
    requiredPresent = @()
    symbolNamespace = ""
    payloads = @([pscustomobject]@{ src = "98_Probe.lua.txt"; dst = "98_Probe.lua"; selfDrives = $true })
  }

  Write-Output "arm_leg.ps1 --SelfTest - every gate must be seen to fire"
  Write-Output ""

  # 1 clean arm -> no gate fires
  Reset-Fixture
  Check "clean arm (the negative)" $false {
    Invoke-Arm $cfg $kit $meta
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 2 a commented-out payload line must NOT read as listed (the inherited bug)
  Reset-Fixture
  Check "commented-out payload reads as NOT armed" $true {
    Invoke-Arm $cfg $kit $meta
    $ls = [System.IO.File]::ReadAllLines($meta)
    for ($i = 0; $i -lt $ls.Count; $i++) {
      if ($ls[$i] -match 'Code/98_Probe\.lua') { $ls[$i] = "`t`t-- " + $ls[$i].TrimStart() }
    }
    Write-LinesLf $meta $ls
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 3 double-listing must fire (the d13-rescue r1 failure)
  Reset-Fixture
  Check "payload listed twice" $true {
    Invoke-Arm $cfg $kit $meta
    $ls = New-Object System.Collections.Generic.List[string]
    foreach ($l in [System.IO.File]::ReadAllLines($meta)) {
      $ls.Add($l)
      if ($l -match 'Code/98_Probe\.lua') { $ls.Add($l) }
    }
    Write-LinesLf $meta $ls
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 4 missing TEMPORARY marker must fire
  Reset-Fixture
  Check "no TEMPORARY marker in payload" $true {
    Invoke-Arm $cfg $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"), "T.Boot()`nquit()`n")
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 5 no self-drive must fire
  Reset-Fixture
  Check "payload never calls the boot symbol" $true {
    Invoke-Arm $cfg $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"), "-- TEMPORARY`nquit()`n")
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 6 no quit() must fire
  Reset-Fixture
  Check "payload never calls quit()" $true {
    Invoke-Arm $cfg $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"), "-- TEMPORARY`nT.Boot()`n")
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 7 a banned call must fire, and only outside a comment
  Reset-Fixture
  Check "banned pattern in live code" $true {
    Invoke-Arm $cfg $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"), "-- TEMPORARY`nT.Boot()`nSaveGame('x')`nquit()`n")
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++
  Reset-Fixture
  Check "banned pattern only in a COMMENT (no fire)" $false {
    Invoke-Arm $cfg $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"), "-- TEMPORARY`n-- never SaveGame('x')`nT.Boot()`nquit()`n")
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 8 a permanent entry going missing must fire
  Reset-Fixture
  Check "permanent probe removed" $true {
    Invoke-Arm $cfg $kit $meta
    Remove-Item -LiteralPath (Join-Path $kit "Code\61_Probes_Wave11.lua") -Force
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 9 mustNotBeListed actively listed must fire
  Reset-Fixture
  Check "excluded entry actively listed" $true {
    Invoke-Arm $cfg $kit $meta
    $ls = New-Object System.Collections.Generic.List[string]
    foreach ($l in [System.IO.File]::ReadAllLines($meta)) {
      $ls.Add($l)
      if ($l -match '99_FixtureCarry') { $ls.Add("`t`t`"Code/96_AutoRunFlag.lua`",") }
    }
    Write-LinesLf $meta $ls
    Invoke-Gates $cfg $kit $meta $true
  }
  $legs++

  # 10 a missing anchor must refuse rather than guess
  Reset-Fixture
  Check "anchorAfter absent -> refuse" $true {
    $c2 = $cfg.PSObject.Copy(); $c2.anchorAfter = "NOPE_NOT_THERE.lua"
    Invoke-Arm $c2 $kit $meta
  }
  $legs++

  # 11 disarm leaves nothing behind
  Reset-Fixture
  Check "disarm is clean (the negative)" $false {
    Invoke-Arm $cfg $kit $meta
    Invoke-Disarm $cfg $kit $meta
    Invoke-Gates $cfg $kit $meta $false
  }
  $legs++

  # 12 no BOM and LF endings survive a write
  Reset-Fixture
  Check "metadata written with no BOM, LF only" $false {
    Invoke-Arm $cfg $kit $meta
    $bytes = [System.IO.File]::ReadAllBytes($meta)
    if ($bytes[0] -eq 0xEF) { GateFail "metadata was written WITH a BOM" }
    if (([System.Text.Encoding]::UTF8.GetString($bytes)).Contains("`r")) { GateFail "metadata was written with CRLF" }
  }
  $legs++

  # 13 declared-mutation gate: missing declared content must fire
  Reset-Fixture
  Check "declared content missing" $true {
    $c3 = $cfg.PSObject.Copy()
    $c3.requiredPresent = @("RestoreBrake", "FORCED")
    Invoke-Arm $c3 $kit $meta
    Invoke-Gates $c3 $kit $meta $true
  }
  $legs++
  Reset-Fixture
  Check "declared content present (no fire)" $false {
    $c3 = $cfg.PSObject.Copy()
    $c3.requiredPresent = @("RestoreBrake", "FORCED")
    Invoke-Arm $c3 $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"),
      "-- TEMPORARY`nlocal FORCED = 1`nfunction RestoreBrake() end`nT.Boot()`nquit()`n")
    Invoke-Gates $c3 $kit $meta $true
  }
  $legs++

  # 14 symbol-resolution gate: a used-but-undefined name must fire. This is the
  # class no parser sees - it compiles, then indexes a nil at run time.
  Reset-Fixture
  Check "unresolved namespace name" $true {
    $c4 = $cfg.PSObject.Copy()
    $c4.symbolNamespace = "T"
    Invoke-Arm $c4 $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"),
      "-- TEMPORARY`nfunction T.Boot() T.NeverDefined() end`nT.Boot()`nquit()`n")
    Invoke-Gates $c4 $kit $meta $true
  }
  $legs++
  Reset-Fixture
  Check "namespace names all resolve (no fire)" $false {
    $c4 = $cfg.PSObject.Copy()
    $c4.symbolNamespace = "T"
    Invoke-Arm $c4 $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"),
      "-- TEMPORARY`nfunction T.Helper() end`nfunction T.Boot() T.Helper() end`nT.Boot()`nquit()`n")
    Invoke-Gates $c4 $kit $meta $true
  }
  $legs++
  Reset-Fixture
  Check "unresolved name only in a COMMENT (no fire)" $false {
    $c4 = $cfg.PSObject.Copy()
    $c4.symbolNamespace = "T"
    Invoke-Arm $c4 $kit $meta
    [System.IO.File]::WriteAllText((Join-Path $kit "Code\98_Probe.lua"),
      "-- TEMPORARY`n-- see T.NeverDefined for history`nfunction T.Boot() end`nT.Boot()`nquit()`n")
    Invoke-Gates $c4 $kit $meta $true
  }
  $legs++

  # 15 a library payload that self-drives must fire (two flows would race)
  Reset-Fixture
  Check "library payload drives itself" $true {
    $c5 = $cfg.PSObject.Copy()
    $c5.payloads = @(
      [pscustomobject]@{ src = "97_Lib.lua.txt";  dst = "97_Lib.lua";  selfDrives = $false },
      [pscustomobject]@{ src = "98_Probe.lua.txt"; dst = "98_Probe.lua"; selfDrives = $true }
    )
    $c5.stripPattern = 'Code/9[78]_(Lib|Probe)'
    [System.IO.File]::WriteAllText((Join-Path $park "97_Lib.lua.txt"), "-- TEMPORARY`nT.Boot()`n")
    Invoke-Arm $c5 $kit $meta
    Invoke-Gates $c5 $kit $meta $true
  }
  $legs++
  Reset-Fixture
  Check "library payload stays a library (no fire)" $false {
    $c5 = $cfg.PSObject.Copy()
    $c5.payloads = @(
      [pscustomobject]@{ src = "97_Lib.lua.txt";  dst = "97_Lib.lua";  selfDrives = $false },
      [pscustomobject]@{ src = "98_Probe.lua.txt"; dst = "98_Probe.lua"; selfDrives = $true }
    )
    $c5.stripPattern = 'Code/9[78]_(Lib|Probe)'
    [System.IO.File]::WriteAllText((Join-Path $park "97_Lib.lua.txt"), "-- TEMPORARY`nfunction T.Helper() end`n")
    Invoke-Arm $c5 $kit $meta
    Invoke-Gates $c5 $kit $meta $true
  }
  $legs++

  Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
  Write-Output ""
  if ($bad.Count -eq 0) {
    Write-Output ("SELFTEST: ALL " + $legs + " LEGS PASS")
    $script:selfTestExit = 0
    return
  }
  Write-Output ("SELFTEST FAILED on: " + ($bad -join ", "))
  $script:selfTestExit = 1
  return
}

# --- arm / disarm ------------------------------------------------------------
function Invoke-Arm($cfg, [string]$kit, [string]$metaPath) {
  $entries = @()
  foreach ($pl in $cfg.payloads) { $entries += ("Code/" + $pl.dst) }

  # Clean slate first, every time, armed or commented - this is what stops an
  # arm-on-top-of-armed double listing at source.
  foreach ($pl in $cfg.payloads) {
    $f = Join-Path $kit (Join-Path "Code" $pl.dst)
    if (Test-Path -LiteralPath $f) { Remove-Item -LiteralPath $f -Force; Say ("DELETED  " + $pl.dst) }
  }
  $n = Strip-LegLines $metaPath $cfg.stripPattern ($entries + $cfg.mustNotBeListed)
  Say ("metadata: stripped " + $n + " line(s)")

  foreach ($pl in $cfg.payloads) {
    Copy-Item -LiteralPath (Join-Path $cfg.park $pl.src) `
              -Destination (Join-Path $kit (Join-Path "Code" $pl.dst)) -Force
    Say ("WROTE    Code/" + $pl.dst)
  }
  $script:insertOk = $false
  Insert-Entries $metaPath $entries $cfg.anchorAfter $cfg.leg
  if ($script:insertOk) { Say "WROTE    metadata.lua (no BOM, LF)" }
}

function Invoke-Disarm($cfg, [string]$kit, [string]$metaPath) {
  $entries = @()
  foreach ($pl in $cfg.payloads) { $entries += ("Code/" + $pl.dst) }
  foreach ($pl in $cfg.payloads) {
    $f = Join-Path $kit (Join-Path "Code" $pl.dst)
    if (Test-Path -LiteralPath $f) { Remove-Item -LiteralPath $f -Force; Say ("DELETED  " + $pl.dst) }
  }
  $n = Strip-LegLines $metaPath $cfg.stripPattern ($entries + $cfg.mustNotBeListed)
  Say ("metadata: stripped " + $n + " line(s)")
}

# --- main --------------------------------------------------------------------
if ($PSCmdlet.ParameterSetName -eq "SelfTest") {
  # NOT `exit (Invoke-SelfTest)` -- a PowerShell function returns its whole
  # OUTPUT STREAM, so capturing the call swallows every progress line into the
  # return value and prints nothing. Call it, then read the script-scoped code.
  $script:selfTestExit = 1
  Invoke-SelfTest
  exit $script:selfTestExit
}

if (-not (Test-Path -LiteralPath $Manifest)) { Write-Output ("no manifest at " + $Manifest); exit 1 }
$cfg = Get-Content -LiteralPath $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json

# PS 5.1 gives a PSCustomObject, and absent members read as $null - normalise so
# every gate can iterate without a null check at each site.
foreach ($f in @("permanent", "mustNotBeListed", "bannedPatterns", "requiredPresent")) {
  if ($null -eq $cfg.$f) { $cfg | Add-Member -NotePropertyName $f -NotePropertyValue @() -Force }
}
foreach ($f in @("stripPattern", "anchorAfter", "bootSymbol", "mustNotBeListedWhy", "symbolNamespace")) {
  if ($null -eq $cfg.$f) { $cfg | Add-Member -NotePropertyName $f -NotePropertyValue "" -Force }
}

$kit = $cfg.kit
$meta = Join-Path $kit "metadata.lua"
if (-not (Test-Path -LiteralPath $meta)) { Write-Output ("no kit metadata at " + $meta); exit 1 }

Say ("leg      " + $cfg.leg)
Say ("mode     " + $Mode)
Say ("kit      " + $kit)
Say ""

if ($Mode -eq "arm") {
  Invoke-Arm $cfg $kit $meta
  Say ""
  Invoke-Gates $cfg $kit $meta $true
} elseif ($Mode -eq "disarm") {
  Invoke-Disarm $cfg $kit $meta
  Say ""
  Invoke-Gates $cfg $kit $meta $false
} else {
  $armed = $true
  foreach ($pl in $cfg.payloads) {
    if (-not (Test-Path -LiteralPath (Join-Path $kit (Join-Path "Code" $pl.dst)))) { $armed = $false }
  }
  Say ("verify: tree reads as " + $(if ($armed) { "ARMED" } else { "DISARMED" }))
  Invoke-Gates $cfg $kit $meta $armed
}

Say ""
if ($script:fail) {
  Say "RESULT: GATE FAILURES ABOVE - do NOT launch the game"
  exit 1
}
if ($Mode -eq "arm") {
  Say "RESULT: ARMED and every gate passed."
  Say "        Reminder: doccheck is now RED (TEMPORARY markers). Disarm before committing."
} else {
  Say "RESULT: every gate passed."
}
exit 0
