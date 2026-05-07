"""اختبار github.js"""
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent.parent
GH_JS_PATH = BASE_DIR / 'static' / 'js' / 'github.js'


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

class TestGithubJsExists:
    def test_js_exists(self): assert GH_JS_PATH.exists()

class TestGithubJsCore:
    def test_has_analyze_repo(self): assert 'function analyzeRepo' in GH_JS_PATH.read_text()
    def test_has_export_doc(self): assert 'function exportDoc' in GH_JS_PATH.read_text()
