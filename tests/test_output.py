import csv
import io
import json

import pytest

from fake_rows.output import write

ROWS = [
    {"id": 1, "city": "Dunmere", "note": 'says "hi", twice'},
    {"id": 2, "city": "Fernhollow", "note": "plain"},
]
FIELDS = ["id", "city", "note"]


def render(fmt, rows=ROWS):
    buf = io.StringIO()
    write(iter(rows), FIELDS, fmt, buf)
    return buf.getvalue()


def test_csv_has_header_and_quotes_awkward_values():
    text = render("csv")
    assert text.splitlines()[0] == "id,city,note"
    assert list(csv.DictReader(io.StringIO(text)))[0]["note"] == 'says "hi", twice'


def test_csv_with_no_rows_still_has_header():
    assert render("csv", []) == "id,city,note\n"


def test_json_is_a_list_that_round_trips():
    assert json.loads(render("json")) == ROWS


def test_json_with_no_rows_is_empty_list():
    assert json.loads(render("json", [])) == []


def test_jsonl_is_one_object_per_line():
    lines = render("jsonl").splitlines()
    assert [json.loads(line) for line in lines] == ROWS


@pytest.mark.parametrize("fmt", ["csv", "json", "jsonl"])
def test_output_ends_with_newline(fmt):
    assert render(fmt).endswith("\n")


def test_json_matches_json_dump_layout():
    assert render("json") == json.dumps(ROWS, indent=2, ensure_ascii=False) + "\n"
    assert render("json", []) == "[]\n"


@pytest.mark.parametrize("fmt", ["csv", "json", "jsonl"])
def test_writers_stream_rows_one_at_a_time(fmt):
    # Each row must reach the output before the next one is requested.
    buf = io.StringIO()
    seen = []

    def rows():
        for row in ROWS:
            seen.append(len(buf.getvalue()))
            yield row

    write(rows(), FIELDS, fmt, buf)
    assert seen[1] > seen[0]
