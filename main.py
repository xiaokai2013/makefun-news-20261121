#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty news-image-20261121.

Ships the front page of Saturday 21 November 2026 (entry.png, drawn
by render.py from news.json) to /output/entry.png. Set OUT to pick a
different destination.

Stdlib only, on purpose: the grader runs `python3 -P -s /bot/main.py`
in a bare python:3.13-slim container with no Pillow and no system
fonts, so nothing beyond the standard library may be imported here.
The picture is drawn at build time by render.py; this file only copies
it. Copying is deterministic — the bytes written are exactly the bytes
committed in entry.png.
"""
import os
import shutil
import sys

IMAGE = "entry.png"


def copy_image():
    """Copy entry.png next to this file into /output/entry.png."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    if not os.path.isfile(src):
        print("error: entry image %s is missing; it must sit next to "
              "main.py in the repo" % src, file=sys.stderr)
        return 1
    dest = os.environ.get("OUT", os.path.join("/output", IMAGE))
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dest)
    if os.path.getsize(dest) != os.path.getsize(src):
        print("error: wrote %d bytes, expected %d"
              % (os.path.getsize(dest), os.path.getsize(src)),
              file=sys.stderr)
        return 1
    print("wrote", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(copy_image())
