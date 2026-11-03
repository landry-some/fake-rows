import csv
import io
import json

import pytest

from fake_rows.cli import main


def run(capsys, *argv):
    code = main(list(argv))
    return code, capsys.readouterr()


def test_default_is_ten_csv_rows(capsys):
    code, out = run(capsys, "name", "email")
    assert code == 0
    rows = list(csv.DictReader(io.StringIO(out.out)))
    assert len(rows) == 10
    assert list(rows[0]) == ["name", "email"]


def test_seed_makes_output_repeatable(capsys):
    _, first = run(capsys, "id=uuid", "address", "-n", "5", "--seed", "7")
    _, second = run(capsys, "id=uuid", "address", "-n", "5", "--seed", "7")
    assert first.out == second.out


def test_json_format(capsys):
    _, out = run(capsys, "id=seq", "-n", "3", "-f", "json")
    assert json.loads(out.out) == [{"id": 1}, {"id": 2}, {"id": 3}]


def test_jsonl_format(capsys):
    _, out = run(capsys, "id=seq:5", "-n", "2", "-f", "jsonl")
    assert out.out == '{"id": 5}\n{"id": 6}\n'


def test_zero_rows(capsys):
    _, out = run(capsys, "name", "-n", "0")
    assert out.out == "name\n"


def test_output_file(tmp_path, capsys):
    target = tmp_path / "users.csv"
    code, out = run(capsys, "id=seq", "name", "-n", "4", "-o", str(target))
    assert code == 0 and out.out == ""
    assert len(target.read_text().splitlines()) == 5


def test_bad_spec_exits_2_with_message(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["phone"])
    assert exc.value.code == 2
    assert "unknown kind 'phone'" in capsys.readouterr().err


def test_negative_count_is_rejected(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["name", "-n", "-1"])
    assert exc.value.code == 2
    assert "--count" in capsys.readouterr().err
