from src.config import read_config


def test_error_on_not_logging_in_config():
    pass


def test_dev_config():
    config = read_config("dev")
    assert "server" in config
    assert "logging" in config
