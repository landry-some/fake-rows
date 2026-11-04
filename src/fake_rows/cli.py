"""Command-line entry point: ``fakerows COLUMN... [-n N] [--seed S] [-f FMT] [-o FILE]``."""

import argparse
import os
import sys

from . import __version__
from .output import FORMATS, write
from .spec import KIND_HELP, KINDS, SpecError, generate, parse_columns

EPILOG = f"""\
column specs:  [name=]kind[:args][?N%]   (?N% leaves about N% of values empty)
kinds:         {", ".join(KINDS)}
examples:      id=seq  user=name  email  joined=date:2020-01-01..2024-12-31
               age=int:18..90  plan=choice:free|pro|team  key=uuid  address
               price=float:1..50  seen=datetime  phone  bio=sentence
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fakerows",
        description="Generate fake test fixtures as CSV, JSON or JSONL.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("columns", nargs="*", metavar="COLUMN", help="column spec, see below")
    p.add_argument("-n", "--count", type=int, default=10, help="rows to generate (default 10)")
    p.add_argument("-s", "--seed", type=int, help="seed for reproducible output")
    p.add_argument("-f", "--format", choices=FORMATS, default="csv", help="output format (default csv)")
    p.add_argument("-o", "--output", metavar="FILE", help="write to FILE instead of stdout")
    p.add_argument("--list-kinds", action="store_true", help="list column kinds and exit")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list_kinds:
        width = max(map(len, KINDS))
        for kind in KINDS:
            print(f"{kind:<{width}}  {KIND_HELP[kind]}")
        return 0
    if not args.columns:
        parser.error("at least one COLUMN is required (see --list-kinds)")
    if args.count < 0:
        parser.error("--count must be 0 or more")
    try:
        columns = parse_columns(args.columns)
    except SpecError as e:
        parser.error(str(e))

    rows = generate(columns, args.count, args.seed)
    fields = [c.name for c in columns]
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            write(rows, fields, args.format, f)
        return 0
    try:
        write(rows, fields, args.format, sys.stdout)
        sys.stdout.flush()
    except BrokenPipeError:
        # Reader went away (e.g. `| head`); stop quietly like other CLI tools.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 0


if __name__ == "__main__":
    sys.exit(main())
