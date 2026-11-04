"""Write rows as CSV, JSON or JSONL."""

import csv
import json
import textwrap
from typing import Iterable, TextIO

FORMATS = ("csv", "json", "jsonl")


def write_csv(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


def write_json(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    # Write one row at a time so a million rows never sit in memory as a list.
    sep = "[\n"
    for row in rows:
        out.write(sep + textwrap.indent(json.dumps(row, indent=2, ensure_ascii=False), "  "))
        sep = ",\n"
    out.write("[]\n" if sep == "[\n" else "\n]\n")


def write_jsonl(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    for row in rows:
        out.write(json.dumps(row, ensure_ascii=False) + "\n")


WRITERS = {"csv": write_csv, "json": write_json, "jsonl": write_jsonl}


def write(rows: Iterable[dict], fields: list[str], fmt: str, out: TextIO) -> None:
    WRITERS[fmt](rows, fields, out)
