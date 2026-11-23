"""One-Line Roast: The Gadget You Use Every Day.

Writes a single original roast line (96 characters) to entry.txt in the
output directory. The line roasts the wireless earbuds used every day:
they die mid-sentence so often that saying goodbye up front has become
a habit.

Pure standard library. No network, no randomness, no clock, no model
call: the same line is written on every run, byte for byte.
"""

import os
import sys
from pathlib import Path

ROAST = (
    "My earbuds die mid-sentence so often I now say goodbye "
    "at the start of every call, just in case."
)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ROAST, encoding="utf-8")

    # Read back and verify: the gate requires UTF-8 text of 1 to 200
    # characters, not only white space, and the two grading runs must
    # produce identical output, so fail loudly instead of shipping a
    # bad file.
    written = target.read_text(encoding="utf-8")
    if written != ROAST or not 1 <= len(written) <= 200 or not written.strip():
        print("error: entry.txt failed the gate check", file=sys.stderr)
        return 1
    print(f"Wrote {target} ({len(ROAST)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
