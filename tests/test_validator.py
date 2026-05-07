"""Tests for validator.py"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.security.validator import *


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

class TestValidate_file_extension:
    def test_exists(self):
        assert callable(validate_file_extension)
    def test_valid(self):
        result = validate_file_extension("test.py")
        assert isinstance(result, bool)

class TestValidate_file_size:
    def test_exists(self):
        assert callable(validate_file_size)
    def test_valid(self):
        result = validate_file_size(b"hello", 100)
        assert isinstance(result, bool)

class TestValidate_file_content:
    def test_exists(self):
        assert callable(validate_file_content)
    def test_valid(self):
        result = validate_file_content("hello")
        assert isinstance(result, bool)

class TestSanitize_filename:
    def test_exists(self):
        assert callable(sanitize_filename)
    def test_valid(self):
        result = sanitize_filename("test.py")
        assert isinstance(result, str)

class TestValidate_file:
    def test_exists(self):
        assert callable(validate_file)
    def test_valid(self):
        result = validate_file("test.py", "print('hello')")
        assert isinstance(result, bool)

class TestDetect_language:
    def test_exists(self):
        assert callable(detect_language)
    def test_valid(self):
        result = detect_language("test.py")
        assert isinstance(result, str)

class TestGet_file_stats:
    def test_exists(self):
        assert callable(get_file_stats)
    def test_valid(self):
        result = get_file_stats("config.py")
        assert isinstance(result, dict)
