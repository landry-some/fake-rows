import pytest

from fake_rows.spec import SpecError, generate, parse_column, parse_columns


def test_bare_kind_names_the_column():
    assert parse_column("email").name == "email"


def test_explicit_column_name():
    assert parse_column("contact=email").name == "contact"


def test_int_range_argument():
    col = parse_columns(["n=int:3..3"])
    assert [r["n"] for r in generate(col, 4, seed=1)] == [3, 3, 3, 3]


def test_date_range_argument():
    rows = list(generate(parse_columns(["d=date:2021-05-05..2021-05-05"]), 2, seed=1))
    assert rows == [{"d": "2021-05-05"}, {"d": "2021-05-05"}]


def test_choice_options():
    rows = generate(parse_columns(["c=choice:x|y"]), 30, seed=1)
    assert {r["c"] for r in rows} == {"x", "y"}


def test_seq_counts_rows_from_start():
    rows = generate(parse_columns(["id=seq:10"]), 3, seed=1)
    assert [r["id"] for r in rows] == [10, 11, 12]


def test_seq_defaults_to_one():
    rows = generate(parse_columns(["seq"]), 2)
    assert [r["seq"] for r in rows] == [1, 2]


def test_rows_keep_column_order_and_seed():
    cols = parse_columns(["id=uuid", "name", "email", "born=date"])
    a = list(generate(cols, 5, seed=9))
    b = list(generate(cols, 5, seed=9))
    assert a == b
    assert list(a[0]) == ["id", "name", "email", "born"]


def test_different_seeds_differ():
    cols = parse_columns(["uuid"])
    assert list(generate(cols, 3, seed=1)) != list(generate(cols, 3, seed=2))


@pytest.mark.parametrize(
    "spec, message",
    [
        ("phone", "unknown kind 'phone'"),
        ("x=", "missing kind"),
        ("int:5", "LOW..HIGH"),
        ("int:a..b", "whole numbers"),
        ("int:9..1", "reversed"),
        ("date:2020-13-01..2021-01-01", "YYYY-MM-DD"),
        ("date:2022-01-01..2021-01-01", "reversed"),
        ("choice", "needs options"),
        ("choice:|", "needs options"),
        ("seq:one", "whole number"),
        ("uuid:4", "uuid takes no argument"),
    ],
)
def test_bad_specs(spec, message):
    with pytest.raises(SpecError, match=message):
        parse_column(spec)


def test_duplicate_column_names():
    with pytest.raises(SpecError, match="duplicate column name 'email'"):
        parse_columns(["email", "email"])
