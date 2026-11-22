#!/usr/bin/env python3
"""news-image-20261122 entry program (Python 3.13, standard library only).

Writes the entry image - a one-image summary of the world news of
Sunday 22 November 2026 - to /output/entry.png. Outside the grader's
container, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The image is the entry.png beside this file, drawn by generate.py from
news.json. Copying it is deterministic: two runs write the same bytes.
"""
import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    src = HERE / "entry.png"
    if not src.is_file():
        raise SystemExit("entry.png missing beside main.py")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    print(f"entry.png written: {dest} ({dest.stat().st_size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
