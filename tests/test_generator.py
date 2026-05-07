"""Tests for generator.py"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.generator import *


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

SAMPLE_ANALYSIS = {
    "functions": [{"name": "test_func", "args": [], "has_return": False}],
    "classes": [],
    "complexity": {"total_lines": 10},
    "language": "Python",
    "filename": "test.py"
}

class TestGenerate_readme_advanced:
    def test_exists(self):
        assert callable(generate_readme_advanced)

    def test_valid(self):
        result = generate_readme_advanced(SAMPLE_ANALYSIS, project_name="Test")
        assert result is not None
        assert isinstance(result, str)

class TestGenerate_api_docs_advanced:
    def test_exists(self):
        assert callable(generate_api_docs_advanced)

    def test_valid(self):
        result = generate_api_docs_advanced(SAMPLE_ANALYSIS)
        assert result is not None
        assert isinstance(result, str)

class TestGenerate_wiki:
    def test_exists(self):
        assert callable(generate_wiki)

    def test_valid(self):
        result = generate_wiki(SAMPLE_ANALYSIS)
        assert result is not None
        assert isinstance(result, str)

class TestGenerate_changelog:
    def test_exists(self):
        assert callable(generate_changelog)

    def test_valid(self):
        result = generate_changelog(SAMPLE_ANALYSIS)
        assert result is not None
        assert isinstance(result, str)

class TestGenerate_all_docs:
    def test_exists(self):
        assert callable(generate_all_docs)

    def test_valid(self):
        result = generate_all_docs("print(1)", SAMPLE_ANALYSIS, "Test")
        assert result is not None
        assert isinstance(result, dict)

class TestGet_quality_report:
    def test_exists(self):
        assert callable(get_quality_report)

    def test_valid(self):
        docs = {"README.md": "# Test Project\n\nDescription\n\n## Installation\n\n```\npip install\n```\n\n## Usage\n\n## Features\n- test\n\n## Requirements\n\n## License\nMIT\n\n## Stats\n| A | B |\n|---|---|\n|x|y|"}
        result = get_quality_report(docs)
        assert result is not None
        assert isinstance(result, dict)
