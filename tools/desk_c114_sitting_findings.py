#!/usr/bin/env python3
"""C114 sitting follow-up: exercise source-derived fixtures at measured distances.

Run: python -B tools/desk_c114_sitting_findings.py

Uses desk_c114_hub_access's pinned 1.1.1.405907 native body and installed
hubset wrapper. Hub hex identity and topology are fixtures, not reporter
measurements; this checks access only.
"""

import desk_c114_hub_access as access


def check_case(runtime, distance, position, connected=True, nearby=False):
    case = runtime.eval("make_case()")
    colonist = case["colonist"]
    home = case["source"]
    hub = case["hub"]
    dome_hexes = case["map"]["object_hex_grid"]["domes"]
    dome_hexes["-30:0"] = None
    home["q"] = -distance
    dome_hexes[f"-{distance}:0"] = home
    if nearby:
        neighbor = case["small"]
        neighbor["cluster"] = runtime.table_from([home])
        colonist["city"]["labels"]["Community"] = runtime.table_from([neighbor, home])
    if position == "dumped":
        colonist["passage_hub"] = hub
    elif position == "standing":
        colonist["holder"] = hub
        colonist["passage_hub"] = hub
    elif position == "unmarked":
        pass
    else:
        raise ValueError(position)
    if not connected:
        hub["hub_domes"][home] = 0
    return bool(colonist.HasLocalAccess(colonist, home))


def main():
    native = access.runtime(False)
    fixed = access.runtime(True)
    cases = (
        (24, "dumped", True, False, True, "holderless marked hub, reporter distance 24"),
        (25, "dumped", True, False, True, "holderless marked hub, reporter distance 25"),
        (28, "dumped", True, False, True, "holderless marked hub, reporter distance 28"),
        (29, "standing", True, False, True, "07 standing hub distance 29"),
        (29, "unmarked", True, False, False, "unmarked on-hub control"),
        (29, "dumped", False, False, False, "removed connection control"),
    )
    for distance, position, connected, expected_native, expected_fixed, label in cases:
        old = check_case(native, distance, position, connected)
        new = check_case(fixed, distance, position, connected)
        print(f"{label}: distance={distance} native={old} fixed={new}")
        if (old, new) != (expected_native, expected_fixed):
            raise AssertionError(label)
    for rt, expected, name in ((native, True, "native"), (fixed, True, "fixed")):
        result = check_case(rt, 29, "standing", nearby=True)
        print(f"nearby connected community: build={name} access={result}")
        if result != expected:
            raise AssertionError("nearby community native-true control")
    print("C114 SITTING DESK CHECK HELD")


if __name__ == "__main__":
    main()
