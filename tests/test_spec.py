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


def test_float_range_argument():
    rows = generate(parse_columns(["p=float:-1.5..-1.5"]), 3, seed=1)
    assert [r["p"] for r in rows] == [-1.5, -1.5, -1.5]


def test_datetime_range_argument():
    rows = generate(parse_columns(["t=datetime:2021-05-05..2021-05-05"]), 5, seed=1)
    assert all(r["t"].startswith("2021-05-05T") for r in rows)


def test_new_kinds_without_arguments():
    cols = parse_columns(["phone", "bool", "word", "sentence", "float", "datetime"])
    row = next(generate(cols, 1, seed=3))
    assert isinstance(row["bool"], bool)
    assert 0 <= row["float"] <= 1


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
        ("colour", "unknown kind 'colour'"),
        ("x=", "missing kind"),
        ("int:5", "LOW..HIGH"),
        ("int:a..b", "whole numbers"),
        ("int:9..1", "reversed"),
        ("date:2020-13-01..2021-01-01", "YYYY-MM-DD"),
        ("date:2022-01-01..2021-01-01", "reversed"),
        ("float:1..x", "float range needs numbers"),
        ("float:2..1", "float range is reversed"),
        ("float:0..inf", "finite"),
        ("datetime:2020-01-01", "datetime range must look like"),
        ("datetime:2022-01-01..2021-01-01", "datetime range is reversed"),
        ("bool:yes", "bool takes no argument"),
        ("phone:1", "phone takes no argument"),
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


def test_nullable_column_leaves_about_that_share_empty():
    rows = list(generate(parse_columns(["age=int:18..90?25%"]), 1000, seed=1))
    nulls = sum(r["age"] is None for r in rows)
    assert 200 < nulls < 300
    assert all(18 <= r["age"] <= 90 for r in rows if r["age"] is not None)


def test_nullable_bare_kind_keeps_kind_as_name():
    col = parse_column("email?10%")
    assert col.name == "email"


@pytest.mark.parametrize("percent, expected", [("0%", 0), ("100%", 20)])
def test_nullable_edges(percent, expected):
    rows = generate(parse_columns([f"n=seq?{percent}"]), 20, seed=1)
    assert sum(r["n"] is None for r in rows) == expected


def test_nullable_percentage_over_100():
    with pytest.raises(SpecError, match="0 to 100"):
        parse_column("name?150%")


def test_question_mark_inside_choice_is_kept():
    rows = generate(parse_columns(["q=choice:why?|how?"]), 20, seed=1)
    assert {r["q"] for r in rows} == {"why?", "how?"}


def test_every_kind_has_help_text():
    from fake_rows.spec import KIND_HELP, KINDS

    assert set(KIND_HELP) == set(KINDS)
