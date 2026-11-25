#!/usr/bin/env python3
"""Make the AI Judge Laugh — make.fun bounty entry.

Writes one single joke about office life (one line, under 200 characters)
to /output/entry.txt, and validates it against the competition gate.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. Only a valid entry goes before the judge.

Usage:
    python3 main.py            # write /output/entry.txt
    python3 main.py --self-test  # validate + determinism check, print PASS
"""

import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

ENTRY = "I put 'per my last email' in my will so my family knows exactly how passive-aggressive I was."

MAX_CHARS = 200
OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line (no newlines)")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")


def write_entry(path: Path = OUTPUT_PATH) -> Path:
    """Write the entry line to path (no trailing newline) and return it."""
    validate(ENTRY)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exactly the line, no trailing newline: the gate counts characters and
    # wants one line; a trailing newline would add a second empty line.
    path.write_bytes(ENTRY.encode("utf-8"))
    return path


def self_test() -> None:
    """Validate the entry, write it twice to temp locations, compare bytes."""
    validate(ENTRY)
    with tempfile.TemporaryDirectory() as tmp:
        p1 = write_entry(Path(tmp) / "a" / "entry.txt")
        p2 = write_entry(Path(tmp) / "b" / "entry.txt")
        b1 = p1.read_bytes()
        b2 = p2.read_bytes()
        assert b1 == b2, "non-deterministic output"
        assert b1 == ENTRY.encode("utf-8"), "output bytes differ from entry"
        digest = hashlib.sha256(b1).hexdigest()
    print(
        f"PASS: {len(ENTRY)} chars (limit <={MAX_CHARS}), "
        f"1 line, sha256={digest}"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test", action="store_true",
        help="validate the entry and check deterministic output",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    path = write_entry()
    print(f"Wrote {len(ENTRY)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
