# fake-rows

A small command-line tool that generates fake test fixtures: names, emails,
addresses, UUIDs, dates, numbers. You describe the columns on the command line and
get CSV, JSON or JSONL back. With `--seed` the output is the same on every run, so
it can go straight into tests.

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

## Run the tests

```bash
pytest
```
