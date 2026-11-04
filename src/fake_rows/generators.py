"""Value generators. Each takes a seeded random.Random and returns one value."""

import random
import uuid
from datetime import date, datetime, time, timedelta

from . import words


def first(rng: random.Random) -> str:
    return rng.choice(words.FIRST_NAMES)


def last(rng: random.Random) -> str:
    return rng.choice(words.LAST_NAMES)


def name(rng: random.Random) -> str:
    return f"{first(rng)} {last(rng)}"


def email(rng: random.Random) -> str:
    user = f"{first(rng)}.{last(rng)}".lower()
    return f"{user}{rng.randint(1, 99)}@{rng.choice(words.EMAIL_DOMAINS)}"


def make_uuid(rng: random.Random) -> str:
    # uuid4() reads os.urandom; building it from rng keeps --seed reproducible.
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def address(rng: random.Random) -> str:
    street = f"{rng.randint(1, 999)} {rng.choice(words.STREETS)} {rng.choice(words.STREET_TYPES)}"
    return f"{street}, {rng.choice(words.CITIES)} {rng.randint(10000, 99999)}"


def make_int(rng: random.Random, low: int, high: int) -> int:
    return rng.randint(low, high)


def make_date(rng: random.Random, start: date, end: date) -> str:
    offset = rng.randint(0, (end - start).days)
    return (start + timedelta(days=offset)).isoformat()


def make_float(rng: random.Random, low: float, high: float) -> float:
    return round(rng.uniform(low, high), 2)


def make_datetime(rng: random.Random, start: date, end: date) -> str:
    seconds = rng.randint(0, (end - start).days * 86400 + 86399)
    return (datetime.combine(start, time()) + timedelta(seconds=seconds)).isoformat()


def phone(rng: random.Random) -> str:
    # 555-0100..0199 is reserved for fiction in the North American plan.
    return f"({rng.randint(200, 999)}) 555-01{rng.randint(0, 99):02d}"


def make_bool(rng: random.Random) -> bool:
    return rng.random() < 0.5


def word(rng: random.Random) -> str:
    return rng.choice(words.WORDS)


def sentence(rng: random.Random) -> str:
    text = " ".join(word(rng) for _ in range(rng.randint(4, 10)))
    return text.capitalize() + "."


def choice(rng: random.Random, options: list[str]) -> str:
    return rng.choice(options)
