#!/usr/bin/env python3
from __future__ import annotations

import sys

from verify_publish import main


if __name__ == "__main__":
    raise SystemExit(main(["--live", *sys.argv[1:]]))
