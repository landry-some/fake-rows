# fake-rows

A small command-line tool that generates fake test fixtures: names, emails,
addresses, phone numbers, UUIDs, dates, numbers and text. You describe the columns
on the command line and get CSV, JSON or JSONL back. With `--seed` the output is
the same on every run, so it can go straight into tests.

It is for developers who need a few believable rows for a test, a demo database or
an import, and are tired of typing "John Doe, test@test.com" by hand.

Built with Python 3.11+ and the standard library only. Tests use pytest. All
values are made up: names come from short built-in lists and every email uses the
reserved `example.com`, `example.org` and `example.net` domains.

## Install

```bash
git clone https://github.com/landry-some/fake-rows.git
cd fake-rows
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
```

This puts a `fakerows` command in the virtual environment.

## Usage

```bash
fakerows COLUMN... [-n COUNT] [--seed SEED] [-f csv|json|jsonl] [-o FILE]
```

Each `COLUMN` is `[name=]kind[:args]`. Without `name=`, the kind is used as the
column name.

| Kind | Args | Example value |
|---|---|---|
| `name` | none | `Keiko Ember` |
| `first`, `last` | none | `Keiko`, `Ember` |
| `email` | none | `mara.vale7@example.com` |
| `uuid` | none | random version 4 UUID |
| `address` | none | `945 Meadow Rd, Graywater 11709` |
| `phone` | none | `(337) 555-0172` (fictional 555-01xx range) |
| `bool` | none | `True` / `False` (`true` / `false` in JSON) |
| `word` | none | `harbor` |
| `sentence` | none | `Harbor hollow engine garden anchor narrow.` |
| `int` | `LOW..HIGH`, default `1..100` | `int:18..90` |
| `float` | `LOW..HIGH`, default `0..1`, 2 decimals | `float:9.99..99.99` |
| `date` | `START..END` as `YYYY-MM-DD`, default `2000-01-01..2029-12-31` | `date:2020-01-01..2024-12-31` |
| `datetime` | `START..END` dates, same default as `date` | `2000-12-18T06:57:46` |
| `choice` | options split by `\|` | `choice:free\|pro\|team` |
| `seq` | start number, default `1` | `seq:100` gives 100, 101, ... |

Options:

- `-n`, `--count`: number of rows, default 10
- `-s`, `--seed`: same seed and same columns give the same output every time
- `-f`, `--format`: `csv` (default), `json` (one array) or `jsonl` (one object per line)
- `-o`, `--output`: write to a file instead of stdout

Quote specs that contain `|` so the shell does not treat it as a pipe.

### Examples

```bash
# 8 users, same output on every run (this is examples/users.csv)
fakerows id=seq name email joined=date:2020-01-01..2024-12-31 'plan=choice:free|pro|team' -n 8 --seed 7

# JSON for an API mock
fakerows id=uuid name address -n 3 -f json

# 1000 rows of JSONL into a file
fakerows id=seq:1000 email age=int:18..90 -n 1000 -f jsonl -o users.jsonl
```

A bad spec exits with code 2 and says what is wrong:

```console
$ fakerows colour
fakerows: error: unknown kind 'colour' (known: address, bool, choice, date, datetime, email, first, float, int, last, name, phone, sentence, seq, uuid, word)
```

## Run the tests

```bash
pytest
```

Planned work is in [ROADMAP.md](ROADMAP.md).
