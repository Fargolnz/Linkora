"""Linkora compiler command-line interface.

Usage:
    python main.py <source.lkr> [--out <directory>]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from compiler import compile_source


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="linkora",
        description="Compile a Linkora (.lkr) page into static HTML.",
    )
    parser.add_argument(
        "source",
        type=Path,
        metavar="SOURCE",
        help="path to the .lkr source file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("output"),
        metavar="DIR",
        help="output directory (default: output)",
    )
    args = parser.parse_args(argv)

    if not args.source.is_file():
        print(f"Error: source file not found: {args.source}", file=sys.stderr)
        return 1

    source_text = args.source.read_text(encoding="utf-8")
    result = compile_source(source_text)

    if not result.success:
        for error in result.errors:
            print(error.format(), file=sys.stderr)
            print(file=sys.stderr)
        print(
            f"Compilation failed with {len(result.errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    out_file = args.out / "index.html"
    out_file.write_text(result.html or "", encoding="utf-8")
    print(f"Generated {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
