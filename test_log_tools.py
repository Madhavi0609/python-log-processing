import pytest

from log_tools import read_logs, retry


def test_read_logs(tmp_path):
    file = tmp_path / "test.log"
    file.write_text(
        "2026-10-07 10:00:00,payment,ERROR,Payment failed\n"
        "2026-10-07 10:01:00,auth,INFO,Login success\n",
        encoding="utf-8",
    )

    logs = list(read_logs(file))

    assert len(logs) == 2
    assert logs[0]["service"] == "payment"
    assert logs[0]["level"] == "ERROR"


def test_retry():
    calls = {"count": 0}

    @retry(times=3)
    def fail():
        calls["count"] += 1
        raise ValueError("Temporary error")

    with pytest.raises(ValueError):
        fail()

    assert calls["count"] == 3


def test_bad_line(tmp_path):
    file = tmp_path / "bad.log"
    file.write_text(
        "this is a bad line\n"
        "2026-10-07 10:02:00,payment,ERROR,Payment failed\n",
        encoding="utf-8",
    )

    logs = list(read_logs(file))

    assert len(logs) == 1
    assert logs[0]["service"] == "payment"
