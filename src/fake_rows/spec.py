"""Parse column specs like ``joined=date:2020-01-01..2024-12-31`` into columns."""

import random
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable

from . import generators as g

# A column value is built from the shared rng and the 0-based row index.
ValueFn = Callable[[random.Random, int], Any]

DEFAULT_INT = (1, 100)
# Fixed default so output does not change with the day it is run.
DEFAULT_DATES = (date(2000, 1, 1), date(2029, 12, 31))


class SpecError(ValueError):
    pass


@dataclass
class Column:
    name: str
    value: ValueFn


def _split_range(arg: str, kind: str) -> tuple[str, str]:
    low, sep, high = arg.partition("..")
    if not sep or not low or not high:
        raise SpecError(f"{kind} range must look like LOW..HIGH, got {arg!r}")
    return low, high


def _int_range(arg: str | None) -> tuple[int, int]:
    if arg is None:
        return DEFAULT_INT
    low, high = _split_range(arg, "int")
    try:
        lo, hi = int(low), int(high)
    except ValueError:
        raise SpecError(f"int range needs whole numbers, got {arg!r}") from None
    if lo > hi:
        raise SpecError(f"int range is reversed: {arg!r}")
    return lo, hi


def _date_range(arg: str | None) -> tuple[date, date]:
    if arg is None:
        return DEFAULT_DATES
    low, high = _split_range(arg, "date")
    try:
        start, end = date.fromisoformat(low), date.fromisoformat(high)
    except ValueError:
        raise SpecError(f"date range needs YYYY-MM-DD dates, got {arg!r}") from None
    if start > end:
        raise SpecError(f"date range is reversed: {arg!r}")
    return start, end


def _no_arg(fn: Callable[[random.Random], Any]) -> Callable[[str | None], ValueFn]:
    def build(arg: str | None) -> ValueFn:
        if arg is not None:
            raise SpecError(f"{fn.__name__.removeprefix('make_')} takes no argument")
        return lambda rng, _i: fn(rng)

    return build


def _build_int(arg: str | None) -> ValueFn:
    lo, hi = _int_range(arg)
    return lambda rng, _i: g.make_int(rng, lo, hi)


def _build_date(arg: str | None) -> ValueFn:
    start, end = _date_range(arg)
    return lambda rng, _i: g.make_date(rng, start, end)


def _build_choice(arg: str | None) -> ValueFn:
    options = [o for o in (arg or "").split("|") if o]
    if not options:
        raise SpecError("choice needs options, e.g. choice:red|green|blue")
    return lambda rng, _i: g.choice(rng, options)


def _build_seq(arg: str | None) -> ValueFn:
    try:
        start = 1 if arg is None else int(arg)
    except ValueError:
        raise SpecError(f"seq start must be a whole number, got {arg!r}") from None
    return lambda _rng, i: start + i


KINDS: dict[str, Callable[[str | None], ValueFn]] = {
    "name": _no_arg(g.name),
    "first": _no_arg(g.first),
    "last": _no_arg(g.last),
    "email": _no_arg(g.email),
    "uuid": _no_arg(g.make_uuid),
    "address": _no_arg(g.address),
    "int": _build_int,
    "date": _build_date,
    "choice": _build_choice,
    "seq": _build_seq,
}


def parse_column(text: str) -> Column:
    col, sep, rest = text.partition("=")
    if not sep:
        col, rest = "", text
    kind, colon, arg = rest.partition(":")
    col = col.strip() or kind
    if not kind:
        raise SpecError(f"missing kind in {text!r}")
    if kind not in KINDS:
        known = ", ".join(sorted(KINDS))
        raise SpecError(f"unknown kind {kind!r} (known: {known})")
    return Column(col, KINDS[kind](arg if colon else None))


def parse_columns(texts: list[str]) -> list[Column]:
    columns = [parse_column(t) for t in texts]
    seen = set()
    for c in columns:
        if c.name in seen:
            raise SpecError(f"duplicate column name {c.name!r}")
        seen.add(c.name)
    return columns


def generate(columns: list[Column], count: int, seed: int | None = None):
    """Yield ``count`` rows as dicts, in column order."""
    rng = random.Random(seed)
    for i in range(count):
        yield {c.name: c.value(rng, i) for c in columns}
