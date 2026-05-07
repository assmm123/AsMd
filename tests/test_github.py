"""Tests for github.py"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.integrations.github import *
from src.integrations.github import GitHubAnalyzer


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

class TestGitHubAnalyzer:
    def test_create(self):
        obj = GitHubAnalyzer("testuser/testrepo")
        assert obj is not None

    def test_analyze_and_generate_exists(self):
        obj = GitHubAnalyzer("testuser/testrepo")
        assert hasattr(obj, "analyze_and_generate")

    def test_analyze_exists(self):
        obj = GitHubAnalyzer("testuser/testrepo")
        assert hasattr(obj, "analyze")
