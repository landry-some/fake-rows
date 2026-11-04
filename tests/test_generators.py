import random
import re
import uuid
from datetime import date

from fake_rows import generators as g
from fake_rows import words


def rng(seed=1):
    return random.Random(seed)


def test_same_seed_gives_same_values():
    a, b = rng(42), rng(42)
    assert [g.name(a) for _ in range(5)] == [g.name(b) for _ in range(5)]


def test_name_uses_built_in_lists():
    first, last = g.name(rng()).split(" ")
    assert first in words.FIRST_NAMES
    assert last in words.LAST_NAMES


def test_email_uses_reserved_domain():
    for seed in range(20):
        value = g.email(rng(seed))
        assert re.fullmatch(r"[a-z]+\.[a-z]+\d+@example\.(com|org|net)", value)


def test_uuid_is_valid_v4_and_seeded():
    value = g.make_uuid(rng(3))
    assert uuid.UUID(value).version == 4
    assert value == g.make_uuid(rng(3))


def test_address_shape():
    value = g.address(rng())
    assert re.fullmatch(r"\d{1,3} \w+ \w+, [\w ]+ \d{5}", value)


def test_int_stays_in_bounds():
    r = rng()
    values = [g.make_int(r, 5, 7) for _ in range(200)]
    assert set(values) == {5, 6, 7}


def test_date_stays_in_range_and_is_iso():
    r = rng()
    start, end = date(2024, 2, 27), date(2024, 3, 2)
    values = {g.make_date(r, start, end) for _ in range(200)}
    assert min(values) == "2024-02-27"
    assert max(values) == "2024-03-02"
    assert "2024-02-29" in values


def test_choice_picks_from_options():
    r = rng()
    assert {g.choice(r, ["a", "b"]) for _ in range(50)} == {"a", "b"}


def test_float_stays_in_bounds_with_two_decimals():
    r = rng()
    values = [g.make_float(r, 1.5, 2.5) for _ in range(200)]
    assert all(1.5 <= v <= 2.5 for v in values)
    assert all(round(v, 2) == v for v in values)


def test_datetime_stays_in_range_and_is_iso():
    r = rng()
    values = {g.make_datetime(r, date(2024, 1, 1), date(2024, 1, 2)) for _ in range(200)}
    assert all(re.fullmatch(r"2024-01-0[12]T\d\d:\d\d:\d\d", v) for v in values)
    assert any(v.startswith("2024-01-02") for v in values)


def test_phone_uses_fictional_range():
    for seed in range(20):
        assert re.fullmatch(r"\([2-9]\d\d\) 555-01\d\d", g.phone(rng(seed)))


def test_bool_gives_both_values():
    r = rng()
    assert {g.make_bool(r) for _ in range(50)} == {True, False}


def test_word_and_sentence_use_word_list():
    assert g.word(rng()) in words.WORDS
    text = g.sentence(rng())
    assert text[0].isupper() and text.endswith(".")
    assert all(w in words.WORDS for w in text[:-1].lower().split())
