#!/usr/bin/env python3
"""The Excuse Your Agent Gives You — make.fun entry.

Reads the one-line excuse from entry.txt shipped beside this program
and writes it byte-identical to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

The gate requires UTF-8 text of 1 to 200 characters, not only
whitespace, so the program validates exactly that before writing.
Pure standard library; no network, no secrets, deterministic.
"""

import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    with open(src, "rb") as f:
        data = f.read()

    text = data.decode("utf-8")  # raises on non-UTF-8: exit non-zero
    if not (1 <= len(text) <= 200):
        raise SystemExit("entry must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("entry must not contain control characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
