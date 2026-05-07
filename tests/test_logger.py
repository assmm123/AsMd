"""Tests for logger.py"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.logger import *
from src.utils.logger import ColoredFormatter, LoggerManager


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

class TestGet_logger:
    def test_exists(self):
        assert callable(get_logger)

    def test_valid(self):
        result = get_logger(None, 42)
        assert result is not None

class TestColoredFormatter:
    def test_create(self):
        obj = ColoredFormatter()
        assert obj is not None

    def test_format_exists(self):
        obj = ColoredFormatter()
        assert hasattr(obj, "format")

class TestLoggerManager:
    def test_create(self):
        obj = LoggerManager()
        assert obj is not None

    def test_debug_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "debug")

    def test_info_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "info")

    def test_warning_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "warning")

    def test_error_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "error")

    def test_critical_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "critical")

    def test_get_stats_exists(self):
        obj = LoggerManager()
        assert hasattr(obj, "get_stats")
