#!/usr/bin/env python3
"""One-Line Office Joke entry.

Writes a single one-line joke about office life to
$MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only. The joke is a fixed constant: the program is deterministic
and produces byte-identical output on every run.
"""

import os
import sys

JOKE = (
    "My calendar finally had a free hour, so I booked a meeting with "
    "myself to find out why I'm always in meetings."
)

MAX_CHARS = 200


def validate(text):
    """Check the joke against the competition gate before writing."""
    if not text or not text.strip():
        raise ValueError("joke is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("joke exceeds %d characters" % MAX_CHARS)
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be exactly one line")
    if len(text.splitlines()) != 1:
        raise ValueError("joke must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("joke contains control characters")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    joke = validate(JOKE)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Atomic write: temp file in the same directory, fsync, os.replace.
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(joke)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, target)

    # Post-write byte-level verification: re-read and compare exactly.
    with open(target, "rb") as fh:
        written = fh.read()
    if written != joke.encode("utf-8"):
        raise ValueError("post-write verification failed: bytes differ")
    if len(written.decode("utf-8")) != len(joke):
        raise ValueError("post-write verification failed: char count differs")

    print("wrote %d characters to %s" % (len(joke), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
