"""اختبار index.html - المنطق الحقيقي"""

import os
from pathlib import Path


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

BASE_DIR = Path(__file__).parent.parent.parent
INDEX_PATH = BASE_DIR / 'templates' / 'index.html'


class TestIndexHtmlExists:
    """اختبار وجود الملف"""
    def test_file_exists(self):
        assert INDEX_PATH.exists()


class TestIndexHtmlLangButtons:
    """اختبار أزرار اللغة"""

    def test_has_ar_button(self):
        """يحتوي على زر AR"""
        content = INDEX_PATH.read_text()
        assert "switchLang('ar')" in content

    def test_has_en_button(self):
        """يحتوي على زر EN"""
        content = INDEX_PATH.read_text()
        assert "switchLang('en')" in content

    def test_has_btnAr(self):
        """يحتوي على btnAr"""
        content = INDEX_PATH.read_text()
        assert 'id="btnAr"' in content

    def test_has_btnEn(self):
        """يحتوي على btnEn"""
        content = INDEX_PATH.read_text()
        assert 'id="btnEn"' in content

    def test_has_lang_btns_class(self):
        """يحتوي على lang-btns"""
        content = INDEX_PATH.read_text()
        assert 'lang-btns' in content


class TestIndexHtmlNoDuplicates:
    """اختبار عدم وجود تكرار"""

    def test_single_app_js_load(self):
        """app.js محمل مرة واحدة"""
        content = INDEX_PATH.read_text()
        count = content.count('src="/static/js/app.js"')
        assert count == 1

    def test_single_switchlang_definition(self):
        """switchLang معرف مرة واحدة فقط"""
        content = INDEX_PATH.read_text()
        count = content.count('function switchLang')
        assert count == 1


class TestIndexHtmlStructure:
    """اختبار هيكل الصفحة"""

    def test_has_header(self):
        """يحتوي على header"""
        content = INDEX_PATH.read_text()
        assert 'class="header"' in content

    def test_has_dropzone(self):
        """يحتوي على dropzone"""
        content = INDEX_PATH.read_text()
        assert 'id="dropzone"' in content

    def test_has_results_area(self):
        """يحتوي على results-area"""
        content = INDEX_PATH.read_text()
        assert 'id="resultsArea"' in content

    def test_has_tabs(self):
        """يحتوي على تبويبات"""
        content = INDEX_PATH.read_text()
        assert 'data-tab="readme"' in content
        assert 'data-tab="api"' in content
        assert 'data-tab="wiki"' in content
        assert 'data-tab="changelog"' in content

    def test_has_export_buttons(self):
        """يحتوي على أزرار تصدير"""
        content = INDEX_PATH.read_text()
        assert 'id="btnMD"' in content
        assert 'id="btnHTML"' in content
        assert 'id="btnPDF"' in content
        assert 'id="btnZIP"' in content

    def test_has_pwa_status(self):
        """يحتوي على pwaStatus"""
        content = INDEX_PATH.read_text()
        assert 'id="pwaStatus"' in content
