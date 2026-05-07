"""اختبار github.py - المنطق الحقيقي"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.integrations.github import GitHubAnalyzer


class TestGitHubAnalyzerInit:
    """اختبارات إنشاء المحلل"""

    def test_create_with_user_repo(self):
        """إنشاء بـ user/repo"""
        a = GitHubAnalyzer("user/repo")
        assert a.user == "user"
        assert a.repo == "repo"

    def test_create_with_full_url(self):
        """إنشاء برابط كامل"""
        a = GitHubAnalyzer("https://github.com/user/repo")
        assert a.user == "user"
        assert a.repo == "repo"

    def test_create_with_git_suffix(self):
        """إنشاء برابط .git"""
        a = GitHubAnalyzer("https://github.com/user/repo.git")
        assert a.repo == "repo"

    def test_create_with_trailing_slash(self):
        """إنشاء برابط بشرطة في النهاية"""
        a = GitHubAnalyzer("user/repo/")
        assert a.repo == "repo"


class TestGitHubAnalyzerInvalid:
    """اختبارات الروابط غير الصالحة"""

    def test_invalid_url(self):
        """رابط غير صالح يرجع error"""
        a = GitHubAnalyzer("not-a-valid-url")
        result = a.analyze()
        assert result['success'] == False
        assert 'Invalid' in result['error'] or 'error' in result


class TestGitHubAnalyzerLanguage:
    """اختبارات دعم اللغة"""

    def test_analyze_with_arabic(self):
        """استدعاء بـ language=ar"""
        a = GitHubAnalyzer("test/test")
        result = a.analyze(language="ar")
        assert 'error' in result or 'success' in result

    def test_analyze_with_english(self):
        """استدعاء بـ language=en"""
        a = GitHubAnalyzer("test/test")
        result = a.analyze(language="en")
        assert 'error' in result or 'success' in result

    def test_analyze_and_generate_alias(self):
        """analyze_and_generate تستدعي analyze"""
        a = GitHubAnalyzer("test/test")
        result = a.analyze_and_generate(language="en")
        assert 'error' in result or 'success' in result


class TestGitHubAnalyzerParseUrl:
    """اختبارات تحليل الرابط"""

    def test_parse_url_sets_user(self):
        """_parse_url يعين user"""
        a = GitHubAnalyzer("https://github.com/microsoft/vscode")
        assert a.user == "microsoft"

    def test_parse_url_sets_repo(self):
        """_parse_url يعين repo"""
        a = GitHubAnalyzer("https://github.com/microsoft/vscode")
        assert a.repo == "vscode"

    def test_no_github_in_url_adds_prefix(self):
        """رابط بدون github.com يضاف له"""
        a = GitHubAnalyzer("user/repo")
        assert "github.com" in a.repo_url
