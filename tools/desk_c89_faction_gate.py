#!/usr/bin/env python3
"""C89 faction dome-size gate over the shipped FactionDef DomeFilter evals.

⭐ THE EVALS ARE EXTRACTED FROM THE SHIPPED PRESETS, NEVER RETYPED, and loaded
under their real file name and line offset, so an error inside one reads
`Data/FactionDef/NewSol.lua:47: ...` exactly as a game log line would. They are
located by their own like `Id` line, not by line number, so the harness does not
rot when the presets move. The module is loaded whole through stub
Register/Require/DataPatch seams that mirror 00_Core's contracts.

⛔ WHAT IS STUBBED, AND WHY NONE OF IT DECIDES ANYTHING (the F59 rule in
deskbench's header). Only three things are faked: the FactionDefs preset map
(rebuilt here from the shipped eval bodies), SMRFixPack's Register/Require/DataPatch
scaffolding, and the dome objects. The dome objects are plain label arrays — which
is all a real dome is to these evals — and the evals themselves are the shipped
bodies, unstubbed. Nothing here stands in for a function that could refuse,
validate or reject: these evals do arithmetic on two arrays and return a boolean,
and that is the whole of them. The one number that decides the outcome, the
threshold, is not supplied by the harness at all — the module reads it out of
Justice's shipped eval by behaviour.

⭐ FALSIFIED 2026-09-12 against guard-reverted copies of the module, because a
harness that cannot fail is not a falsifier and the builder's own APPLY_MODULE
switch is not independent. Each row is one replacement made in a scratch copy of
Code/Fix_FactionDomeSizeGate.lua with MODULE pointed at it; the named legs FAILED,
and all six guards were caught.

    reverted (1 hit each, verbatim)                            -> legs that failed
    "if already_gated(t.eval, threshold) then" -> "if false then"
                                                        (f), (f2), (f3)
    "return #obj.labels.Colonist >= threshold and orig(obj)" -> "return orig(obj)"
                                                        (a2), (g)
    "if #targets ~= TARGET_COUNT then" -> "if false then"        (h)
    "if bad_precedent or not threshold or seen_precedent < #PRECEDENT_IDS then"
        -> "threshold = threshold or 10 if false then"           (i)
    adding JusticeUnemployment to TARGET_IDS
                                (a2), (e), (e2), (f2), (f3), (g), (h)
    "if not self_check_passed then return end" -> ""             (k), (k2)

⚠️ Leg (j), the 1.0.7 decline, is protected by TWO independent guards — the
precedent check and the all-or-nothing count — so reverting either one alone leaves
it passing. That is redundancy, not a gap: each guard is shown necessary by the
other legs above, and (j) is the leg that would catch losing both.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_FactionDomeSizeGate.lua")

# faction preset file -> the like Ids it carries that this fix is about
LIKES = {
    "JusticeMovement": ["JusticeUnemployment", "JusticeHomeless"],
    "ProsperityForMars": ["ProsperityUnemployment"],
    "MarsDemocraticParty": ["UtopiaUnemployment", "UtopiaHomeless"],
    "WorkersParty": ["CollectiveUnemployment", "CollectiveHomeless"],
    "NewSol": ["NewSolUnemployment", "NewSolHomeless"],
}
TARGETS = ["ProsperityUnemployment", "UtopiaUnemployment", "UtopiaHomeless",
           "CollectiveUnemployment", "CollectiveHomeless",
           "NewSolUnemployment", "NewSolHomeless"]
PRECEDENT = ["JusticeUnemployment", "JusticeHomeless"]


def like_eval(faction, like_id, tree="1.1.0"):
    """-> (eval body text, 1-based first line) for one like's DomeFilter.eval,
    found by its own `'Id', "<like_id>",` line in the shipped preset."""
    rel = "Data/FactionDef/%s.lua" % faction
    lines = db.read_lines_for(rel, tree)
    id_at = [i for i, l in enumerate(lines)
             if re.match(r"^\s*'Id',\s*\"%s\",\s*$" % re.escape(like_id), l)]
    assert len(id_at) == 1, "%s %s -> %d Id lines" % (rel, like_id, len(id_at))
    start = None
    for i in range(id_at[0], min(id_at[0] + 12, len(lines))):
        if re.match(r"^\s*eval = function \(obj\)\s*$", lines[i]):
            start = i
            break
    assert start is not None, "%s %s: no eval within 12 lines of its Id" % (rel, like_id)
    end = None
    for i in range(start + 1, min(start + 12, len(lines))):
        if lines[i].strip() in ("end,", "end"):
            end = i
            break
    assert end is not None, "%s %s: eval has no closing end," % (rel, like_id)
    return "\n".join(lines[start:end + 1]).rstrip(","), start + 1


# deskbench exposes body()/span() only; this harness needs raw lines per tree.
def _read_lines_for(rel, tree="1.1.0"):
    from luafn import read_lines
    return read_lines(os.path.join(db.TREES[tree], rel))


db.read_lines_for = _read_lines_for

PRELUDE = db.ENGINE_SHIMS + r'''
FactionLikeDomes = { CountDome = function() end }
FactionDefs = {}
SMRFixPack = { fixes = {}, data_edited = {} }
SMRFixPack_Disabled = {}
LOG = {}
function SMRFixPack.Log(fmt, ...) LOG[#LOG + 1] = string.format(fmt, ...) end
APPLY_MODULE = true
DATA_LOADED = true

-- A stub DataPatch that mirrors 00_Core's ctx contract (latch/heal/ever_changed/
-- data_loaded/patched) closely enough for the legs, and exposes the pass so the
-- harness can fire it deliberately rather than through engine messages.
function SMRFixPack.DataPatch(id, opts)
	local ctx = { patched = false, data_loaded = DATA_LOADED, classes_built = true,
		ever_changed = SMRFixPack.data_edited[id] or false }
	LATCH = nil
	LATCH_BENIGN = nil
	function ctx.latch(detail, log_suffix, benign)
		LATCH = detail
		LATCH_BENIGN = benign
		local e = SMRFixPack.fixes[id]
		if e then e.status = "inactive" e.detail = detail end
	end
	function ctx.heal() end
	PASS_CTX = ctx
	RUN_PASS = function()
		local ok, err = pcall(opts.pass, ctx)
		if ok then PASS_ERROR = nil else PASS_ERROR = tostring(err) end
		if ctx.ever_changed then SMRFixPack.data_edited[id] = true end
	end
	return function() end
end

function SMRFixPack.Register(id, def)
	SMRFixPack.fixes[id] = { title = def.title, status = "pending", detail = "" }
	if APPLY_MODULE then
		local res = def.apply()
		SMRFixPack.apply_error = res
		SMRFixPack.fixes[id].status = type(res) == "string" and "inactive" or "active"
	end
end
function SMRFixPack.Require(_, specs)
	for _, spec in ipairs(specs) do
		if spec.class and spec.method then
			local class = _G[spec.class]
			if type(class) ~= "table" or type(class[spec.method]) ~= "function" then
				return (spec.class .. "." .. spec.method .. " not found")
			end
		elseif spec.test and not spec.test() then
			return spec.reason or "shape declined"
		end
	end
end
function SMRFixPack.WhenActive(_, fn) return fn end
OnMsg = {}

-- A dome is only label arrays to these evals.
function dome(colonists, unemployed, homeless)
	local c, u, h = {}, {}, {}
	for i = 1, colonists do c[i] = i end
	for i = 1, unemployed do u[i] = i end
	for i = 1, (homeless or 0) do h[i] = i end
	return { labels = { Colonist = c, Unemployed = u, Homeless = h } }
end

EVALS = {}   -- like id -> the shipped eval, before any patching
function add_like(faction_id, like_id, eval)
	local f = FactionDefs[faction_id]
	if not f then
		f = { id = faction_id, likes = {} }
		FactionDefs[faction_id] = f
	end
	local like = {
		Id = like_id,
		Value = -300,
		DomeFilter = { Params = "obj", eval = eval },
	}
	f.likes[#f.likes + 1] = like
	EVALS[like_id] = eval
	return like
end

function eval_now(like_id)
	for _, f in pairs(FactionDefs) do
		for _, like in ipairs(f.likes) do
			if like.Id == like_id then return like.DomeFilter.eval end
		end
	end
end
'''


def make_runtime(apply=True, tree="1.1.0", drop=None, break_shape=None,
                 simulate_patched=(), data_loaded=True):
    """drop: a like id to omit entirely. break_shape: a like id whose DomeFilter.eval
    is made a non-function. simulate_patched: like ids to hand a gated eval, as a
    post-Paradox-patch vanilla would ship."""
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    rt.globals().DATA_LOADED = bool(data_loaded)
    loaded = []
    for faction, ids in LIKES.items():
        for like_id in ids:
            if like_id == drop:
                continue
            text, line = like_eval(faction, like_id, tree)
            rel = "Data/FactionDef/%s.lua" % faction
            fn_name = "EVAL_" + like_id
            # The extracted text is `eval = function (obj) ... end`, verbatim. Load
            # it inside a table constructor rather than rewriting the assignment, so
            # not one byte of the shipped body changes and every line still sits at
            # its real offset (the prefix shares line 1 of the body).
            db.load_at(rt, "HOLDER = {" + text + "\n}", "=" + rel, line)
            rt.execute("%s = HOLDER.eval" % fn_name)
            loaded.append((rel, like_id, line))
            if like_id in simulate_patched:
                # what vanilla ships once the developers add the gate themselves
                rt.execute('''
					local shipped = %s
					%s = function(obj)
						return #obj.labels.Colonist >= 10 and shipped(obj)
					end
				''' % (fn_name, fn_name))
            rt.execute('add_like("%s", "%s", %s)' % (faction, like_id, fn_name))
            if like_id == break_shape:
                rt.execute('''
					for _, f in pairs(FactionDefs) do
						for _, l in ipairs(f.likes) do
							if l.Id == "%s" then l.DomeFilter.eval = "not a function" end
						end
					end
				''' % like_id)
    rt.globals().APPLY_MODULE = apply
    db.load_at(rt, db.read(MODULE), "=Code/Fix_FactionDomeSizeGate.lua", 1)
    rt.eval("RUN_PASS")()
    return rt, loaded


def main():
    bench = db.Bench("C89 faction dome-size gate -- shipped DomeFilter evals and module")
    check = bench.check

    rt, loaded = make_runtime()
    for rel, like_id, line in loaded:
        print("extracted %-40s %-24s at :%d" % (rel, like_id, line))
    print()
    g = rt.globals()
    check("the module applies and the pass runs clean",
          g.SMRFixPack["apply_error"] is None and g.PASS_ERROR is None,
          g.PASS_ERROR or "")

    # ---- (a) the defect, reproduced, and the fix -----------------------------
    small = "dome(3, 1, 1)"
    rt.execute("SMALL = %s" % small)
    shipped_true = all(
        rt.eval('EVALS["%s"](SMALL)' % lid) is True for lid in TARGETS)
    check("(a) THE DEFECT REPRODUCED -- all seven shipped evals fire on a dome of "
          "3 with 1 idle/homeless colonist", shipped_true)
    patched_false = all(
        rt.eval('eval_now("%s")(SMALL)' % lid) is False for lid in TARGETS)
    check("(a2) after the patch all seven refuse that dome", patched_false)

    # ---- (b) a dome of ten: both agree --------------------------------------
    rt.execute("TEN = dome(10, 1, 1)")
    check("(b) a dome of 10 with 1 idle/homeless: shipped evals fire",
          all(rt.eval('EVALS["%s"](TEN)' % lid) is True for lid in TARGETS))
    check("(b2) ... and the patched evals still fire -- the gate changes nothing at "
          "ten or above",
          all(rt.eval('eval_now("%s")(TEN)' % lid) is True for lid in TARGETS))

    # ---- (c) a big dome under the percentage: both refuse -------------------
    rt.execute("BIG = dome(30, 2, 2)")
    check("(c) a dome of 30 with 2 idle/homeless (under 10%): both refuse",
          all(rt.eval('EVALS["%s"](BIG)' % lid) is False for lid in TARGETS)
          and all(rt.eval('eval_now("%s")(BIG)' % lid) is False for lid in TARGETS))

    # ---- (d) Justice is byte-for-byte untouched ----------------------------
    justice_same = all(
        rt.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
        for lid in PRECEDENT)
    check("(d) CONTROL -- both Justice evals are the SAME function object after the "
          "pass (not wrapped, not replaced)", justice_same)
    check("(d2) ... and Justice already refused the small dome, which is the whole "
          "precedent",
          all(rt.eval('EVALS["%s"](SMALL)' % lid) is False for lid in PRECEDENT))

    # ---- (e) exactly the seven were patched, nothing else -------------------
    changed = [lid for lid in TARGETS + PRECEDENT
               if rt.eval('eval_now("%s") ~= EVALS["%s"]' % (lid, lid)) is True]
    check("(e) exactly the seven target likes were patched, and no other",
          sorted(changed) == sorted(TARGETS), sorted(changed))
    check("(e2) the module logged the count and the threshold it read from Justice",
          any("7 faction dislike(s) now wait for 10 colonists" in str(v)
              for v in dict(g.LOG).values()), list(dict(g.LOG).values()))

    # ---- (f) a post-patch vanilla: skip, never double-gate ------------------
    part, _ = make_runtime(simulate_patched=("NewSolUnemployment", "UtopiaHomeless"))
    gp = part.globals()
    check("(f) a like the developers have ALREADY gated is skipped, not double-gated",
          part.eval('eval_now("NewSolUnemployment") == EVALS["NewSolUnemployment"]') is True
          and part.eval('eval_now("UtopiaHomeless") == EVALS["UtopiaHomeless"]') is True)
    check("(f2) ... while the five still-unguarded ones ARE patched, and the log "
          "names the skipped ones",
          all(part.eval('eval_now("%s") ~= EVALS["%s"]' % (lid, lid)) is True
              for lid in TARGETS
              if lid not in ("NewSolUnemployment", "UtopiaHomeless"))
          and any("already gated" in str(v) for v in dict(gp.LOG).values()),
          list(dict(gp.LOG).values()))

    allp, _ = make_runtime(simulate_patched=tuple(TARGETS))
    ga = allp.globals()
    check("(f3) a fully post-patch vanilla latches the module inactive as benign "
          "(the RETIRE signal), and patches nothing",
          ga.LATCH is not None and ga.LATCH_BENIGN == "benign"
          and all(allp.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
                  for lid in TARGETS), ga.LATCH)

    # ---- (g) idempotency: a second pass changes nothing ---------------------
    twice, _ = make_runtime()
    before = [twice.eval('eval_now("%s")' % lid) for lid in TARGETS]
    twice.eval("RUN_PASS")()
    check("(g) a second pass (DataChanged re-fire) double-gates nothing and does not "
          "latch",
          all(twice.eval('eval_now("%s")(dome(3,1,1))' % lid) is False for lid in TARGETS)
          and all(twice.eval('eval_now("%s")(dome(10,1,1))' % lid) is True for lid in TARGETS)
          and twice.globals().LATCH is None)

    # ---- (h) fail closed: a missing or misshapen like patches NOTHING -------
    miss, _ = make_runtime(drop="CollectiveHomeless")
    gm = miss.globals()
    check("(h) one missing like ⇒ NOTHING is patched and the module latches "
          "(a partial application would leave the five factions inconsistent)",
          gm.LATCH is not None
          and all(miss.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
                  for lid in TARGETS if lid != "CollectiveHomeless"), gm.LATCH)

    shape, _ = make_runtime(break_shape="UtopiaUnemployment")
    check("(h2) a like whose DomeFilter.eval is not a function ⇒ nothing patched, "
          "module latches", shape.globals().LATCH is not None)

    # ---- (i) the precedent is required, not assumed -------------------------
    nog = db.lua_runtime()
    nog.execute(PRELUDE)
    # Justice present but with its guard removed -- the precedent is gone, so the
    # judgment call has nothing to copy and the module must decline.
    for faction, ids in LIKES.items():
        for like_id in ids:
            text, line = like_eval(faction, like_id)
            rel = "Data/FactionDef/%s.lua" % faction
            if like_id in PRECEDENT:
                text = text.replace("#obj.labels.Colonist >= 10 and ", "")
            db.load_at(nog, "HOLDER = {" + text + "\n}", "=" + rel, line)
            nog.execute('add_like("%s", "%s", HOLDER.eval)' % (faction, like_id))
    db.load_at(nog, db.read(MODULE), "=Code/Fix_FactionDomeSizeGate.lua", 1)
    nog.eval("RUN_PASS")()
    gn = nog.globals()
    check("(i) Justice WITHOUT its own gate ⇒ the module declines and patches "
          "nothing -- the precedent this judgment call copies must be present",
          gn.LATCH is not None
          and all(nog.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
                  for lid in TARGETS), gn.LATCH)

    # ---- (j) THE 1.0.7 BRANCH -- the ids differ, so the module must DECLINE ---
    # On 1.0.7 the EXPRESSIONS are byte-identical but the IDS are not: three
    # factions share `JusticeHomeless` (JusticeMovement.lua:123 guarded,
    # MarsDemocraticParty.lua:102 and WorkersParty.lua:128 unguarded), and 1.1.0's
    # UtopiaHomeless / CollectiveHomeless do not exist. The branch guard must catch
    # that with no version check, and it must do so DETERMINISTICALLY -- not
    # depending on which duplicate `pairs` reaches first.
    old_likes = {
        "JusticeMovement": ["JusticeUnemployment", "JusticeHomeless"],
        "ProsperityForMars": ["ProsperityUnemployment"],
        "MarsDemocraticParty": ["UtopiaUnemployment", "JusticeHomeless"],
        "WorkersParty": ["CollectiveUnemployment", "JusticeHomeless"],
        "NewSol": ["NewSolUnemployment", "NewSolHomeless"],
    }
    try:
        declines = []
        for _ in range(6):   # repeated, because the failure mode was pairs-order
            old = db.lua_runtime()
            old.execute(PRELUDE)
            for faction, ids in old_likes.items():
                for i, like_id in enumerate(ids):
                    text, line = like_eval(faction, like_id, "1.0.7")
                    rel = "Data/FactionDef/%s.lua" % faction
                    db.load_at(old, "HOLDER = {" + text + "\n}", "=" + rel, line)
                    # a duplicate id must still produce a distinct like object
                    old.execute('add_like("%s", "%s", HOLDER.eval)' % (faction, like_id))
            db.load_at(old, db.read(MODULE), "=Code/Fix_FactionDomeSizeGate.lua", 1)
            old.eval("RUN_PASS")()
            declines.append(old.globals().LATCH)
    except (AssertionError, OSError, KeyError) as exc:
        check("(j) the 1.0.7 archived tree makes the module decline", False,
              "archive unavailable or moved: %s" % exc)
    else:
        check("(j) the 1.0.7 tree: the module DECLINES on every run -- the duplicate "
              "unguarded `JusticeHomeless` is caught deterministically, with no "
              "version check",
              all(d is not None for d in declines), set(str(d) for d in declines))
        check("(j2) ... and the 1.0.7 expressions themselves are the same defect "
              "(the branch differs by ID, not by expression)",
              all(old.eval('EVALS["%s"](dome(3,1,1))' % lid) is True
                  for lid in ("ProsperityUnemployment", "UtopiaUnemployment",
                              "CollectiveUnemployment", "NewSolUnemployment",
                              "NewSolHomeless")))

    # ---- (k) NEGATIVE: registered but never applied ------------------------
    never, _ = make_runtime(apply=False)
    check("(k) NEGATIVE -- a module registered but never applied patches nothing",
          all(never.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
              for lid in TARGETS)
          and all(never.eval('eval_now("%s")(dome(3,1,1))' % lid) is True
                  for lid in TARGETS))

    # ---- (k2) NEGATIVE: a DECLINED self-check must not patch either ---------
    # DataPatch's runner re-reads the veto but not the apply verdict, so without the
    # module's own flag a declined self-check would still patch the presets while the
    # entry read `inactive`. This is the leg that holds that guard (see bugs/C90.md).
    declined = db.lua_runtime()
    declined.execute(PRELUDE)
    declined.execute("FactionLikeDomes = {}")   # CountDome gone => Require fails
    for faction, ids in LIKES.items():
        for like_id in ids:
            text, line = like_eval(faction, like_id)
            rel = "Data/FactionDef/%s.lua" % faction
            db.load_at(declined, "HOLDER = {" + text + "\n}", "=" + rel, line)
            declined.execute('add_like("%s", "%s", HOLDER.eval)' % (faction, like_id))
    db.load_at(declined, db.read(MODULE), "=Code/Fix_FactionDomeSizeGate.lua", 1)
    declined.eval("RUN_PASS")()
    gd = declined.globals()
    check("(k2) NEGATIVE -- a module whose self-check DECLINED patches nothing, even "
          "though DataPatch's runner still fires its pass",
          gd.SMRFixPack["apply_error"] is not None
          and all(declined.eval('eval_now("%s") == EVALS["%s"]' % (lid, lid)) is True
                  for lid in TARGETS)
          and all(declined.eval('eval_now("%s")(dome(3,1,1))' % lid) is True
                  for lid in TARGETS),
          gd.SMRFixPack["apply_error"])

    # ---- (m) THE OWNER'S CONSOLE LINE IS A CLAIM TOO -----------------------
    # checklist 158 hands the owner SMRFixPack.FactionDomeGate.Report(SelectedObj).
    # Trace it here, not in the game: it must say GATE ACTIVE on a small dome, show
    # no difference on a dome of ten, and say GATE-ABSENT rather than something
    # reassuring when the fix never applied.
    rep, _ = make_runtime()
    rep.execute('LOG = {} SMRFixPack.FactionDomeGate.Report(dome(3, 1, 1))')
    small_log = " | ".join(str(v) for v in dict(rep.globals().LOG).values())
    check("(m) Report() on a dome of 3 says GATE ACTIVE and shows shipped=true vs "
          "live=false on all seven rows",
          "GATE ACTIVE" in small_log and "7 row(s), 7 where" in small_log
          and "shipped=true live=false" in small_log, small_log[:200])

    rep.execute('LOG = {} SMRFixPack.FactionDomeGate.Report(dome(10, 1, 1))')
    ten_log = " | ".join(str(v) for v in dict(rep.globals().LOG).values())
    check("(m2) Report() on a dome of 10 shows no difference -- the gate is a gate, "
          "not a blanket suppression",
          "0 where the gate changed" in ten_log and "shipped=true live=true" in ten_log,
          ten_log[:160])

    off, _ = make_runtime(apply=False)
    off.execute('LOG = {} SMRFixPack.FactionDomeGate.Report(dome(3, 1, 1))')
    off_log = " | ".join(str(v) for v in dict(off.globals().LOG).values())
    check("(m3) Report() with the fix NOT applied says shipped=not-wrapped and does "
          "NOT claim the gate is active -- the owner cannot bank a false PASS",
          "not-wrapped" in off_log and "GATE ACTIVE" not in off_log, off_log[:200])

    rep.execute('LOG = {} SMRFixPack.FactionDomeGate.Report({ class = "NotADome" })')
    bad_log = " | ".join(str(v) for v in dict(rep.globals().LOG).values())
    check("(m4) Report() on a non-dome says so instead of printing numbers",
          "select a DOME first" in bad_log, bad_log[:120])

    # ---- (l) the F75 lesson: absence before DataLoaded does not latch ------
    early, _ = make_runtime(drop="NewSolHomeless", data_loaded=False)
    check("(l) a missing like BEFORE DataLoaded does NOT latch (absence proves "
          "nothing yet -- the F75 lesson)", early.globals().LATCH is None)

    return bench.finish(
        "ALL DEMANDS HELD -- the seven shipped evals fire on a dome of three with "
        "one idle colonist and stop after the patch; a dome of ten is unchanged; "
        "Justice is the same function object throughout; the module reads its "
        "threshold from Justice's own behaviour, skips a like already gated, "
        "latches benign when all seven are, and patches nothing at all if any "
        "part of the shape is missing."
    )


if __name__ == "__main__":
    sys.exit(main())
