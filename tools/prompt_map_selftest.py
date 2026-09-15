#!/usr/bin/env python3
"""Falsify the PROMPT MAP gate in disposable directory fixtures."""
import hashlib
from pathlib import Path
import tempfile

from repair_pass_selftest import ROOT, load_copy


GOOD_MAP = """# fixture prompt map

## `perma/` — standing prompts

| prompt | declared class | use |
|---|---|---|
| `PROMPT.md` | `prompt` | fixture prompt |
| `RELEASE_OUTBOX.md` | `ledger-exception` | owner-exempt ledger |

## Root — live one-offs

| prompt | declared class | state |
|---|---|---|
| `ONE.md`, `TWO.md` | `prompt` | grouped fixture prompts |

## Chain folders

| chain | declared class | state |
|---|---|---|
| `live-a/`, `live-b/` | `live` | grouped live fixture chains |
"""


def make_fixture(module, root):
    docs = root / "docs"
    prompts = docs / "agent" / "prompts"
    perma = prompts / "perma"
    perma.mkdir(parents=True)
    for name in ("PROMPT.md", "RELEASE_OUTBOX.md"):
        (perma / name).write_text("fixture\n", encoding="utf-8")
    for name in ("ONE.md", "TWO.md"):
        (prompts / name).write_text("fixture\n", encoding="utf-8")
    (prompts / "README.md").write_text(GOOD_MAP, encoding="utf-8")
    (prompts / "live-a").mkdir()
    (prompts / "live-a" / "README.md").write_text("fixture\n", encoding="utf-8")
    (prompts / "live-a" / "evidence.json").write_text("{}\n", encoding="utf-8")
    (prompts / "live-b").mkdir()
    (prompts / "live-b" / "evidence.txt").write_text("fixture\n", encoding="utf-8")
    module.DOCS = str(docs)
    return prompts


def rewrite_map(prompts, old, new):
    path = prompts / "README.md"
    body = path.read_text(encoding="utf-8")
    assert old in body
    path.write_text(body.replace(old, new), encoding="utf-8")


def run_case(module, root, label, mutate, should_pass):
    prompts = make_fixture(module, root / label.replace(" ", "-"))
    if mutate is not None:
        mutate(prompts)
    out = []
    result = module.check_prompt_map(out)
    assert result is should_pass, (label, out)
    if should_pass:
        assert any(line.startswith("PROMPT MAP: PASS") for line in out), out
    else:
        assert any(line.startswith("PROMPT MAP: RED") for line in out), out
    print("PASS %s: %s" % (label, "gate passes" if result else "broken fixture fails"))
    return out


def main():
    live = ROOT / "tools" / "doccheck.py"
    original = live.read_bytes()
    source = original.decode("utf-8-sig")
    with tempfile.TemporaryDirectory(prefix="prompt-map-") as directory:
        root = Path(directory)
        module = load_copy(root / "doccheck.py", source)

        good = run_case(module, root, "mapped live evidence map and outbox", None, True)
        assert "live-chain README/evidence and the map itself are permitted" in "\n".join(good)

        run_case(module, root, "unmapped chain",
                 lambda p: (p / "unmapped").mkdir(), False)
        run_case(module, root, "mapped missing chain",
                 lambda p: rewrite_map(
                     p, "| `live-a/`, `live-b/` | `live` |",
                     "| `live-a/`, `live-b/`, `missing/` | `live` |"), False)
        run_case(module, root, "support declared at perma",
                 lambda p: rewrite_map(
                     p, "| `PROMPT.md` | `prompt` |",
                     "| `PROMPT.md` | `support-migration-leg-03` |"), False)
        run_case(module, root, "support declared at root",
                 lambda p: rewrite_map(
                     p, "| `ONE.md`, `TWO.md` | `prompt` |",
                     "| `ONE.md`, `TWO.md` | `support-migration-leg-03` |"), False)

        def closed_outside_allowance(prompts):
            (prompts / "old").mkdir()
            rewrite_map(
                prompts, "| `live-a/`, `live-b/` | `live` |",
                "| `live-a/`, `live-b/` | `live` |\n"
                "| `old/` | `closed-migration-leg-02` | closed |")

        run_case(module, root, "closed chain outside migration debt",
                 closed_outside_allowance, False)
        run_case(module, root, "struck map row",
                 lambda p: rewrite_map(
                     p, "| `ONE.md`, `TWO.md` | `prompt` |",
                     "| ~~`ONE.md`, `TWO.md`~~ | `prompt` |"), False)

    assert live.read_bytes() == original
    print("UNCHANGED live doccheck SHA256 " + hashlib.sha256(original).hexdigest())


if __name__ == "__main__":
    main()
