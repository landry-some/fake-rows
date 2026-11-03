"""Value generators. Each takes a seeded random.Random and returns one value."""

import random
import uuid
from datetime import date, timedelta

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


def choice(rng: random.Random, options: list[str]) -> str:
    return rng.choice(options)
