#!/usr/bin/env python3
"""make.fun bounty: Sum up 22 November's world news in one image.

Copies the entry image (entry.png, held in this repository) to
/output/entry.png (or $MAKEFUN_OUTPUT if set).

Before copying, the image is validated: it must be a real PNG, exactly
1024x1024, and under 1 MiB. After copying, the output's SHA-256 is
checked against the source, so a bad copy fails loudly instead of
submitting a corrupt entry.

Stdlib only (hashlib, os, shutil, struct). No network, no randomness, no
clock: the copy is byte-for-byte, so two runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# Entry requirements: a 1024x1024 PNG under 1 MiB.
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_file(path):
    """SHA-256 hex digest of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_png(path):
    """Check the entry image meets the bounty requirements.

    Verifies the file exists, is a real PNG, is exactly 1024x1024
    (parsed from the IHDR chunk, stdlib only), and is under 1 MiB.
    Exits with a clear error instead of copying a bad entry.
    Returns (width, height, size_bytes, sha256).
    """
    if not os.path.isfile(path):
        raise SystemExit("error: entry image not found: %s" % path)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(
            "error: entry image is %d bytes, over the %d-byte limit"
            % (size, MAX_BYTES)
        )
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise SystemExit("error: entry image is not a PNG file: %s" % path)
    if header[12:16] != b"IHDR":
        raise SystemExit("error: PNG has no IHDR chunk: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            "error: entry image is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    return width, height, size, sha256_file(path)


def main():
    width, height, size, digest = validate_png(SRC)
    out = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SRC, out)
    # Verify the copy is byte-identical to the validated source.
    if sha256_file(out) != digest:
        raise SystemExit("error: copied file differs from source: %s" % out)
    print(
        "wrote %s (%dx%d, %d bytes, sha256 %s)"
        % (out, width, height, size, digest)
    )


if __name__ == "__main__":
    main()
