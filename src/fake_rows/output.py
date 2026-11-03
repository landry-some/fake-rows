"""Write rows as CSV, JSON or JSONL."""

import csv
import json
from typing import Iterable, TextIO

FORMATS = ("csv", "json", "jsonl")


def write_csv(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


def write_json(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    json.dump(list(rows), out, indent=2, ensure_ascii=False)
    out.write("\n")


def write_jsonl(rows: Iterable[dict], fields: list[str], out: TextIO) -> None:
    for row in rows:
        out.write(json.dumps(row, ensure_ascii=False) + "\n")


WRITERS = {"csv": write_csv, "json": write_json, "jsonl": write_jsonl}


def write(rows: Iterable[dict], fields: list[str], fmt: str, out: TextIO) -> None:
    WRITERS[fmt](rows, fields, out)
