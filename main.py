#!/usr/bin/env python3
"""Roast writer for the make.fun one-line-roast bounty.

Purpose
-------
Emit exactly one roast line about the gadget the author uses daily
(wireless earbuds) into ``entry.txt`` inside the harness output
directory, then prove the file on disk is byte-for-byte that line.

Guarantees
----------
* Standard library only; nothing is imported beyond ``pathlib`` and ``sys``.
* No network, no clock reads, no randomness, no environment surprises:
  the same input always produces the same bytes.
* The output file is UTF-8, holds a single line, and carries no trailing
  newline, so a second run lands on identical bytes.
"""

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The roast itself
# ---------------------------------------------------------------------------
#
# One sentence, one grievance, one habit it forced on its owner. The line
# below is the entire entry; everything else in this file exists only to
# deliver it unchanged and to check that it arrived unchanged.

ROAST_LINE = "My earbuds die mid-sentence so often I now say goodbye at the start of every call, just in case."

# The bounty allows a single line of 1 to 200 characters.
LOWER_BOUND = 1
UPPER_BOUND = 200

# Name of the file the harness grades.
OUTPUT_NAME = "entry.txt"

# Where the file goes when the harness does not say otherwise.
DEFAULT_OUTPUT_DIR = "/output"


# ---------------------------------------------------------------------------
# Output location
# ---------------------------------------------------------------------------

def resolve_output_dir(env):
    """Pick the output directory from the environment mapping given.

    ``MAKEFUN_OUTPUT_DIR`` wins when it is set to a non-empty value;
    otherwise the harness default is used.
    """
    requested = env.get("MAKEFUN_OUTPUT_DIR")
    if requested:
        return Path(requested)
    return Path(DEFAULT_OUTPUT_DIR)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def problems_with(text):
    """Collect every way ``text`` could fail the bounty's entry rule.

    Returns a list of human-readable problems; an empty list means the
    text is a valid entry.
    """
    found = []
    if not LOWER_BOUND <= len(text) <= UPPER_BOUND:
        found.append(
            "entry must be %d-%d characters, got %d"
            % (LOWER_BOUND, UPPER_BOUND, len(text))
        )
    if text != text.strip():
        found.append("entry must not start or end with whitespace")
    if not text.strip():
        found.append("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    return found


def check_written_file(path, expected):
    """Read ``path`` back and confirm it holds exactly ``expected``.

    Both the decoded text and the raw byte count are compared, so a
    stray newline or a different encoding cannot slip through.
    """
    stored = path.read_text(encoding="utf-8")
    if stored != expected:
        return ["written file differs from the roast line"]
    raw = path.read_bytes()
    if len(raw) != len(expected.encode("utf-8")):
        return ["written file byte size does not match the roast line"]
    return problems_with(stored)


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def emit_roast(directory):
    """Write the roast into ``directory/entry.txt`` and return its path."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / OUTPUT_NAME
    target.write_text(ROAST_LINE, encoding="utf-8", newline="")
    return target


def report_problems(problems):
    """Print each problem to stderr, one per line."""
    for problem in problems:
        print("error: %s" % problem, file=sys.stderr)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(argv=None, env=None):
    """Write the roast, verify it, and report success or failure.

    ``argv`` is accepted for testability and ignored; ``env`` defaults to
    the real process environment.
    """
    environment = os.environ if env is None else env
    target = emit_roast(resolve_output_dir(environment))
    problems = check_written_file(target, ROAST_LINE)
    if problems:
        report_problems(problems)
        return 1
    print("wrote %s (%d characters)" % (target, len(ROAST_LINE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
