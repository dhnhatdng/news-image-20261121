"""Entry program for news-image-20261121.

Copies the front-page image stored in this repository to the output
directory the grader provides. Standard library only; the copy is
byte-for-byte, so repeated runs produce identical output.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        raise SystemExit("copy incomplete: size mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
