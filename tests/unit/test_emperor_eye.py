"""اختبار Project Scanner - المنطق الحقيقي"""

import sys, os, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.testing.emperor.eye import (
    ProjectScanner, ScannedFile, ProjectMap, scan_project,
    list_source_files, list_test_files, find_untested_files
)


class TestProjectScanner:
    """اختبارات الماسح الأساسية"""

    def test_scan_current_directory(self):
        """مسح المجلد الحالي"""
        scanner = ProjectScanner()
        pm = scanner.scan(".")
        assert pm.total_files > 0
        assert len(pm.source_files) > 0
        assert pm.has_src_layout

    def test_scan_empty_directory(self):
        """مسح مجلد فارغ"""
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert pm.total_files == 0

    def test_scan_python_files(self):
        """اكتشاف ملفات Python"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "core_module.py").write_text("def hello():\n    return 'world'\n")
            Path(tmpdir, "helper.js").write_text("function hello() { return 'world'; }")
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert len(pm.source_files) >= 1
            assert len(pm.javascript_files) >= 1

    def test_classify_test_files(self):
        """تصنيف ملفات الاختبار"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "test_core.py").write_text("def test_hello():\n    pass\n")
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert len(pm.test_files) >= 1

    def test_exclude_dirs(self):
        """تجاهل المجلدات المستبعدة"""
        with tempfile.TemporaryDirectory() as tmpdir:
            pycache = Path(tmpdir, "__pycache__")
            pycache.mkdir()
            Path(pycache, "cached.py").write_text("# cache\n")
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert pm.total_files == 0


class TestFilePeek:
    """اختبارات التحليل السريع للملفات"""

    def test_peek_python_file(self):
        """تحليل سريع لملف Python"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp = Path(tmpdir, "module.py")
            fp.write_text("""\"\"\"Test module.\"\"\"\nimport os\n\nclass MyClass:\n    def method(self):\n        return True\n\ndef main():\n    return 1\n""")
            scanner = ProjectScanner()
            peek = scanner.peek_file(str(fp))
            assert peek is not None
            assert peek.has_imports
            assert peek.has_classes
            assert peek.has_functions
            assert peek.import_count >= 1
            assert peek.class_count >= 1
            assert peek.function_count >= 1

    def test_peek_empty_file(self):
        """تحليل ملف فارغ"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fp = Path(tmpdir, "empty.py")
            fp.write_text("")
            scanner = ProjectScanner()
            peek = scanner.peek_file(str(fp))
            assert peek is None


class TestTestGaps:
    """اختبارات فجوات الاختبار"""

    def test_find_gaps(self):
        """اكتشاف ملفات بدون اختبارات"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "core.py").write_text("def core():\n    pass\n")
            Path(tmpdir, "utils.py").write_text("def util():\n    pass\n")
            Path(tmpdir, "test_core.py").write_text("def test_core():\n    pass\n")
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert pm.test_gap is not None
            assert pm.test_gap.total_sources == 2
            assert pm.test_gap.tested_count == 1
            assert pm.test_gap.untested_count == 1

    def test_find_gaps_all_tested(self):
        """كل الملفات مختبرة"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "core.py").write_text("def core():\n    pass\n")
            Path(tmpdir, "test_core.py").write_text("def test_core():\n    pass\n")
            scanner = ProjectScanner()
            pm = scanner.scan(tmpdir)
            assert pm.test_gap.coverage_pct == 100.0


class TestConvenienceFunctions:
    """اختبارات الدوال المساعدة"""

    def test_scan_project(self):
        """scan_project يعمل"""
        pm = scan_project(".")
        assert isinstance(pm, ProjectMap)

    def test_list_source_files(self):
        """list_source_files يعمل"""
        files = list_source_files(".")
        assert isinstance(files, list)

    def test_list_test_files(self):
        """list_test_files يعمل"""
        files = list_test_files(".")
        assert isinstance(files, list)

    def test_find_untested_files(self):
        """find_untested_files يعمل"""
        files = find_untested_files(".")
        assert isinstance(files, list)
