"""اختبار app.js - المنطق الحقيقي"""

import os
from pathlib import Path


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

BASE_DIR = Path(__file__).parent.parent.parent
APP_JS_PATH = BASE_DIR / 'static' / 'js' / 'app.js'
LANG_JS_PATH = BASE_DIR / 'static' / 'js' / 'lang.js'


class TestAppJsExists:
    """اختبار وجود الملف"""

    def test_app_js_file_exists(self):
        """app.js موجود"""
        assert APP_JS_PATH.exists()

    def test_lang_js_removed(self):
        """lang.js تم حذفه"""
        assert not LANG_JS_PATH.exists()


class TestAppJsContent:
    """اختبار محتوى الملف"""

    def test_contains_translations_dict(self):
        """يحتوي على قاموس ترجمة"""
        content = APP_JS_PATH.read_text()
        assert 'var TRANSLATIONS' in content

    def test_contains_arabic(self):
        """يحتوي على ترجمة عربية"""
        content = APP_JS_PATH.read_text()
        assert 'ar:' in content

    def test_contains_english(self):
        """يحتوي على ترجمة إنجليزية"""
        content = APP_JS_PATH.read_text()
        assert 'en:' in content

    def test_contains_switch_lang(self):
        """يحتوي على switchLang"""
        content = APP_JS_PATH.read_text()
        assert 'function switchLang' in content

    def test_contains_t_function(self):
        """يحتوي على T()"""
        content = APP_JS_PATH.read_text()
        assert 'function T(' in content

    def test_contains_apply_lang(self):
        """يحتوي على applyLang"""
        content = APP_JS_PATH.read_text()
        assert 'function applyLang' in content

    def test_contains_localstorage(self):
        """يستخدم localStorage لتخزين اللغة"""
        content = APP_JS_PATH.read_text()
        assert "localStorage.getItem('docgen_lang')" in content


class TestTranslationKeys:
    """اختبار مفاتيح الترجمة الأساسية"""

    def test_has_generate_all_key(self):
        """مفتاح generateAll موجود"""
        content = APP_JS_PATH.read_text()
        assert 'generateAll:' in content

    def test_has_clear_key(self):
        """مفتاح clear موجود"""
        content = APP_JS_PATH.read_text()
        assert 'clear:' in content

    def test_has_readme_key(self):
        """مفتاح readme موجود"""
        content = APP_JS_PATH.read_text()
        assert 'readme:' in content

    def test_has_api_key(self):
        """مفتاح api موجود"""
        content = APP_JS_PATH.read_text()
        assert 'api:' in content

    def test_has_ok_key(self):
        """مفتاح ok موجود"""
        content = APP_JS_PATH.read_text()
        assert 'ok:' in content

    def test_has_fail_key(self):
        """مفتاح fail موجود"""
        content = APP_JS_PATH.read_text()
        assert 'fail:' in content

    def test_has_select_files_key(self):
        """مفتاح selectFiles موجود"""
        content = APP_JS_PATH.read_text()
        assert 'selectFiles:' in content
