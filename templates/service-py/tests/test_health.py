from app.health import health


def test_reports_ok_with_whole_seconds_of_uptime() -> None:
    result = health(now=lambda: 112.7, started_at=100.0)
    assert result.status == "ok"
    assert result.uptime_seconds == 12
