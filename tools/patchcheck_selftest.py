#!/usr/bin/env python3
"""Regression test for patchcheck.py: it must reproduce the 1.0.7 -> 1.1.0 backtest.

    python tools/patchcheck_selftest.py                 # ~30 s; exit 0 = every leg PASS
    python tools/patchcheck_selftest.py --break REQ     # the falsifier: must exit 1

Input: the pre-patch pack (`git archive f7bd288 Code`, the last commit before the
first 1.1.0 response) over the two archived trees. Expected values are the
design report's (`docs/agent/reports/GAME_PATCH_INSTRUMENTS.md` §3.1, §3.5, §3.3),
checked against the 1.1.0 re-verification answer key (§1a/1b/1d: FIX 10,
REMOVE 35, KEEP 35; `DroneTransportMinors` counted once, as KEEP).

Legs:
  1. per-column FIX/REMOVE/KEEP counts for PIN, REQ, SIGCALL, CITE and D1
     (= PIN+REQ+CITE) equal the §3.1 table, and the verdict is full;
  2. identity overlay (every file old): 0 of 80 modules in M, verdict none;
  3. one-file overlay (`Lua/Buildings/Residence.lua` at 1.1.0, SYNTHETIC): M is
     exactly {StaleReservations, DomeFreeSpaceMismatch} (the report's prose says
     FreedHousingNotice; its prototype, re-run, flags DomeFreeSpaceMismatch), and
     the verdict is full by B alone (that file's 1.1.0 `__parents` lines moved);
     3b. `Lua/Buildings/Community.lua` alone: M = {ShelterReflex}, verdict scoped;
  4. D2 finds `ArrivalDeaths` -> `ChooseDome` (F117), ranked incompatible;
  5. ANON flags `MeteorFrequency` (R-9, report §3.3: the one D1 miss).

`--break COLUMN` empties that column's harvest (REQ, PIN, CITE or SIGCALL) before
the legs run. A pass under `--break` means the test is vacuous. Run it after any
edit to either script.
"""
import argparse, os, subprocess, sys, tempfile, tarfile, io

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import patchcheck as pc  # noqa: E402

PRE_SHA = "f7bd288"
OLD, NEW = "1.0.7.396349", "1.1.0.403908"

FIX = set("SaintBlessing StaleReservations ShelterReflex FirstAsteroidPrefabs AstrogeologistExtractors "
          "PayloadTemplateRefill RocketDroneChurn LandscapeUnitFilter VacuumWalks TrainCargoDumping".split())
REMOVE = set("""LowStorageWarning LanderCargoRatchet TouristSatisfaction AutomationLawCompensation UpgradeModifierLeak
SmallLandscapeSites DroneUnreachableForever MeteorFrequency MeteorStormWedge AsteroidLanderAvailable
GridGlobalStorage LastTransmissionStorage RainsDeadlock DustSicknessDamage IndependenceTerraforming
UniversityOvertraining CaveInsNoDisasters CommandCenterNumbers DisasterPredictionLeak DustDevilSpawnGate
DustDevilsDescrMap DustStormUndergroundBreaks ExtractorStaffedPerformance LanderReturnFuel LandscapeCostRefresh
LocalizedUIText MilestoneCrash MoraleComfortTooltip SpaceYDroneCapBullet StorageRateModifiers
TechDescriptionBuilding TouristApplicants TrainMinors TrainPlatformWedge 90_SaveSanitizer""".split())

# GAME_PATCH_INSTRUMENTS.md §3.1: (FIX, REMOVE, KEEP, flagged)
TABLE = {"PIN": (6, 21, 16, 43), "REQ": (6, 14, 17, 37), "SIGCALL": (3, 7, 4, 14),
         "CITE": (10, 34, 28, 72), "D1": (10, 34, 32, 76)}


def extract_pre(dest):
    blob = subprocess.run(["git", "-C", pc.REPO, "archive", PRE_SHA, "Code"], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        if hasattr(tarfile, "data_filter"):
            tf.extractall(dest, filter="data")
        else:
            tf.extractall(dest)
    return os.path.join(dest, "Code")


def install_break(col):
    orig = pc.harvest

    def broken(path):
        h = orig(path)
        if col == "REQ":
            h["reqs"] = set()
        elif col == "PIN":
            h["pins"] = set()
        elif col == "CITE":
            h["cites"], h["bare"] = set(), set()
        elif col == "SIGCALL":
            h["calls"] = set()
        return h
    pc.harvest = broken


def verdict_of(cmp, code, overlay):
    argv = ["--old", OLD, "--new", NEW, "--code", code, "--no-notes", "--no-parity", "--no-d5-list"]
    if overlay is not None:
        argv += ["--overlay", ",".join(sorted(overlay)) or "__none__"]
    lines = []
    res = pc.run(pc.parse(argv), out=lines.append, cmp=cmp)
    return res["verdict"], lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--break", dest="brk", choices=["REQ", "PIN", "CITE", "SIGCALL"])
    a = ap.parse_args()
    if a.brk:
        install_break(a.brk)
        print("⚠️ FALSIFIER: the %s column is emptied; this run MUST fail" % a.brk)
    fails = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  — " + detail) if detail else ""))
        if not cond:
            fails.append(label)

    old_root, new_root = pc.resolve_tree(OLD), pc.resolve_tree(NEW)
    with tempfile.TemporaryDirectory() as tmp:
        code = extract_pre(tmp)
        n_mod = len(pc.module_files(code))
        check("pre-patch pack has 80 modules", n_mod == 80, "got %d" % n_mod)
        full = pc.Compare(old_root, new_root)
        rows = pc.analyse(full, code)

        def verdict_key(r):
            return "FIX" if r["module"] in FIX else "REMOVE" if r["module"] in REMOVE else "KEEP"
        key = [verdict_key(r) for r in rows]
        check("answer key splits 10/35/35", (key.count("FIX"), key.count("REMOVE"), key.count("KEEP")) == (10, 35, 35),
              str((key.count("FIX"), key.count("REMOVE"), key.count("KEEP"))))
        # leg 1
        for col, want in TABLE.items():
            hit = [r for r in rows if (r["D1"] if col == "D1" else bool(r[col]))]
            got = (sum(1 for r in hit if verdict_key(r) == "FIX"), sum(1 for r in hit if verdict_key(r) == "REMOVE"),
                   sum(1 for r in hit if verdict_key(r) == "KEEP"), len(hit))
            check("§3.1 %-7s FIX/REMOVE/KEEP/flagged = %s" % (col, "/".join(map(str, want))), got == want,
                  "got " + "/".join(map(str, got)))
        v, _ = verdict_of(full, code, None)
        check("1.0.7 -> 1.1.0 verdict is full", v == "full", v)
        # leg 4
        d2 = {(r["module"], n): cls for r in rows for (_k, n, cls, _o, _nw) in r["SIGCALL"]}
        check("D2 finds ArrivalDeaths -> ChooseDome, incompatible (F117)",
              d2.get(("ArrivalDeaths", "ChooseDome")) == "incompatible", str(d2.get(("ArrivalDeaths", "ChooseDome"))))
        # leg 5
        mf = [r for r in rows if r["module"] == "MeteorFrequency"]
        check("ANON flags MeteorFrequency (R-9, the D1 miss)", bool(mf and mf[0]["ANON"] and not mf[0]["D1"]),
              "ANON=%s D1=%s" % (bool(mf and mf[0]["ANON"]), bool(mf and mf[0]["D1"])))
        # leg 2
        ident = pc.Compare(old_root, new_root, overlay=set(), base=full)
        m = [r["module"] for r in pc.analyse(ident, code) if r["flagged"]]
        check("identity overlay: 0/80 flagged", not m, ", ".join(m))
        v, _ = verdict_of(ident, code, set())
        check("identity overlay verdict is none", v == "none", v)
        # leg 3 -- the report's §3.5 prose names FreedHousingNotice; its own
        # prototype (`backtest.py --overlay`, re-run 2026-09-19) flags
        # DomeFreeSpaceMismatch (cited ChooseResidence changed). The measurement wins.
        ov = {"Lua/Buildings/Residence.lua"}
        one = pc.Compare(old_root, new_root, overlay=ov, base=full)
        m = sorted(r["module"] for r in pc.analyse(one, code) if r["flagged"])
        check("one-file overlay (SYNTHETIC) flags exactly DomeFreeSpaceMismatch, StaleReservations",
              m == ["DomeFreeSpaceMismatch", "StaleReservations"], ", ".join(m))
        v, lines = verdict_of(one, code, ov)
        vline = [l for l in lines if l.startswith("verdict:")]
        # 1.1.0's Residence.lua really changes two `__parents` lines, so B fires:
        # the verdict is full by B alone while |M| = 2 sits inside the scoped limit.
        check("one-file overlay verdict is full by B alone", v == "full" and vline and "— B = 1  (" in vline[0],
              vline[0] if vline else v)
        # leg 3b -- a one-file overlay with no structure change exercises scoped
        ov = {"Lua/Buildings/Community.lua"}
        one = pc.Compare(old_root, new_root, overlay=ov, base=full)
        m = sorted(r["module"] for r in pc.analyse(one, code) if r["flagged"])
        check("one-file overlay Community.lua (SYNTHETIC) flags exactly ShelterReflex", m == ["ShelterReflex"], ", ".join(m))
        v, _ = verdict_of(one, code, ov)
        check("Community.lua overlay verdict is scoped", v == "scoped", v)
    print("")
    if fails:
        print("RED  %d leg(s) failed%s" % (len(fails), " — as the falsifier requires" if a.brk else ""))
        return 1
    print("GREEN  every leg passed%s" % (" — ⛔ THE FALSIFIER PASSED: the test is vacuous" if a.brk else ""))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
