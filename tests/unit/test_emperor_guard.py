"""اختبار File Watcher و Project Guard - المنطق الحقيقي"""

import sys, os, tempfile, time
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.testing.emperor.guard import FileWatcher, ProjectGuard, watch_project


class TestFileWatcher:
    """اختبارات مراقب الملفات"""

    def test_create_default(self):
        """إنشاء افتراضي"""
        w = FileWatcher(".")
        assert w is not None
        assert w.source_dir is not None
        assert w.debounce == 2

    def test_create_custom_debounce(self):
        """تخصيص debounce"""
        w = FileWatcher(".", debounce=5)
        assert w.debounce == 5

    def test_scan_finds_python_files(self):
        """اكتشاف ملفات Python"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "module.py").write_text("# test\n")
            (tmp / "script.js").write_text("// test\n")
            time.sleep(0.05)

            w = FileWatcher(str(tmp), debounce=0.5)
            changed = w.scan_once()
            changed_names = [Path(c).name for c in changed]
            assert 'module.py' in changed_names
            assert 'script.js' not in changed_names

    def test_ignores_test_files(self):
        """تجاهل ملفات الاختبار"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "test_core.py").write_text("# test\n")
            (tmp / "core.py").write_text("# real\n")
            time.sleep(0.05)

            w = FileWatcher(str(tmp), debounce=0.5)
            changed = w.scan_once()
            changed_names = [Path(c).name for c in changed]
            assert 'core.py' in changed_names
            assert 'test_core.py' not in changed_names

    def test_ignores_pycache(self):
        """تجاهل __pycache__"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "__pycache__").mkdir()
            (tmp / "__pycache__" / "cached.py").write_text("# cached\n")
            time.sleep(0.05)

            w = FileWatcher(str(tmp), debounce=0.5)
            changed = w.scan_once()
            assert len(changed) == 0

    def test_detects_new_file(self):
        """اكتشاف ملف جديد"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            w = FileWatcher(str(tmp), debounce=0.5)
            w.scan_once()

            # إنشاء ملف جديد
            time.sleep(0.1)
            (tmp / "new_module.py").write_text("# new\n")
            time.sleep(0.05)

            changed = w.scan_once()
            changed_names = [Path(c).name for c in changed]
            assert 'new_module.py' in changed_names

    def test_detects_modified_file(self):
        """اكتشاف تعديل ملف"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "mod.py").write_text("# v1\n")
            time.sleep(0.05)

            w = FileWatcher(str(tmp), debounce=0.5)
            w.scan_once()

            # تعديل الملف
            time.sleep(0.3)
            (tmp / "mod.py").write_text("# v2 modified\n")
            time.sleep(0.3)

            changed = w.scan_once()
            changed_names = [Path(c).name for c in changed]
            assert 'mod.py' in changed_names

    def test_no_false_positive(self):
        """لا إنذارات كاذبة"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "stable.py").write_text("# stable\n")
            time.sleep(0.05)

            w = FileWatcher(str(tmp), debounce=0.5)
            w.scan_once()

            # بدون تغيير
            changed = w.scan_once()
            assert len(changed) == 0

    def test_callback_registered(self):
        """تسجيل callback"""
        w = FileWatcher(".")
        called = []

        def cb(path):
            called.append(path)

        w.on_change(cb)
        assert len(w._callbacks) == 1

    def test_multiple_callbacks(self):
        """تعدد callbacks"""
        w = FileWatcher(".")
        w.on_change(lambda x: None)
        w.on_change(lambda x: None)
        assert len(w._callbacks) == 2


class TestProjectGuard:
    """اختبارات حارس المشروع"""

    def test_create_default(self):
        """إنشاء افتراضي"""
        with tempfile.TemporaryDirectory() as tmpdir:
            g = ProjectGuard(source_dir=tmpdir, test_dir=str(Path(tmpdir) / "tests"))
            assert g is not None
            assert g.auto_heal == True
            assert g.watcher is not None

    def test_create_no_heal(self):
        """بدون إصلاح تلقائي"""
        with tempfile.TemporaryDirectory() as tmpdir:
            g = ProjectGuard(source_dir=tmpdir, auto_heal=False)
            assert g.auto_heal == False

    def test_with_memory(self):
        """مع ذاكرة"""
        with tempfile.TemporaryDirectory() as tmpdir:
            g = ProjectGuard(source_dir=tmpdir, memory={"test": True})
            assert g.memory is not None

    def test_stop_does_not_crash(self):
        """التوقف لا يسبب خطأ"""
        with tempfile.TemporaryDirectory() as tmpdir:
            g = ProjectGuard(source_dir=tmpdir)
            try:
                g.stop()
                assert True
            except Exception:
                assert False
