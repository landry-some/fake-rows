# Roadmap

v0.1 covers seeded generators, column specs, CSV/JSON/JSONL output and the CLI.
Everything below is planned follow-up work. Estimates are rough.

Total: **26 h**

## Features

- [ ] Schema files (TOML) so a fixture set can be saved and reused — 3 h
- [ ] Row-consistent fields: `email` built from the same row's `name` — 2 h
- [ ] `--unique` per column with a clear error when the space runs out — 2 h
- [x] More kinds: `phone`, `bool`, `float:A..B`, `datetime`, `word`, `sentence` — 3 h
- [ ] SQL `INSERT` output for a given table name — 2 h
- [x] Nullable columns (`col=kind?10%` leaves 10% of values empty) — 1.5 h

## Bugs and edge cases

- [ ] CSV quoting of values with commas, quotes and newlines in `choice` — 1 h
- [ ] Date ranges that are reversed, equal or outside year 1–9999 — 1 h
- [ ] Large `-n` (1M rows) should stream instead of building a list — 1.5 h
- [ ] Clear errors for duplicate column names and empty choice lists — 0.5 h

## Refactors

- [ ] Registry of generators with per-kind argument parsing and help text — 2 h
- [ ] Move word lists into data files loaded with `importlib.resources` — 1 h

## Tests

- [ ] Golden-file tests: fixed seed gives byte-identical output per format — 1.5 h
- [ ] Property tests for ranges (values always inside bounds) — 1 h
- [ ] CLI tests for every error path and exit code — 1 h

## Docs

- [ ] `fakerows --list-kinds` and a full kind reference in the README — 1 h
- [ ] Recipes: seeding a SQLite table, feeding a pytest fixture — 1 h
