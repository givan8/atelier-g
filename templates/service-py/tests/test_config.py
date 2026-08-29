import pytest

from app.config import Config, ConfigError, parse_port, required


def test_rejects_a_port_outside_the_valid_range() -> None:
    with pytest.raises(ConfigError, match="between 1 and 65535"):
        parse_port("70000")


def test_rejects_a_port_that_is_not_a_number() -> None:
    with pytest.raises(ConfigError, match="must be an integer"):
        parse_port("http")


def test_names_the_missing_variable() -> None:
    with pytest.raises(ConfigError, match="ABSENT"):
        required("ABSENT", env={})


def test_defaults_are_applied_when_the_environment_is_empty() -> None:
    config = Config.from_env(env={})
    assert config.port == 8080
    assert config.log_level == "info"
