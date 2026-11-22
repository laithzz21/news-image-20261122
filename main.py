#!/usr/bin/env python3
"""make.fun bounty: Sum up 22 November's world news in one image.

Copies the entry image (entry.png, held in this repository) to
/output/entry.png (or $MAKEFUN_OUTPUT if set).

Stdlib only (os, shutil). No network, no randomness, no clock: the copy is
byte-for-byte, so two runs write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SRC, out)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
