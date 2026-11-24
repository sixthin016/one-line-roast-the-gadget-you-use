#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Writes a single roast line about a daily gadget to entry.txt.
Standard library only, deterministic, no network, no clock, no randomness.
The file is written with no trailing newline, exactly as the gate expects.
"""

import os
import sys

ROAST = "My earbuds die mid-sentence so often I now say goodbye at the start of every call, just in case."


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ROAST)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ROAST:
        print("error: entry.txt does not match ROAST", file=sys.stderr)
        return 1
    if not 1 <= len(written) <= 200:
        print("error: entry must be 1-200 characters", file=sys.stderr)
        return 1
    if not written.strip():
        print("error: entry must not be blank", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(written)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
