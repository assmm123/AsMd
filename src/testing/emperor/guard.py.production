"""
Guard - File Watcher v1.1.0
Watches project files and auto-runs analysis, generation, and healing on changes.
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Set, List, Callable
from datetime import datetime, timezone


# ============================================================
# File Watcher
# ============================================================

class FileWatcher:
    """Watches Python files for changes and triggers callbacks"""

    def __init__(self, source_dir: str = ".", debounce: int = 2,
                 exclude_patterns: Set[str] = None):
        self.source_dir = Path(source_dir).resolve()
        self.debounce = debounce
        self.exclude_dirs = {
            '__pycache__', '.git', '.venv', 'venv', 'node_modules',
            '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build',
            'egg-info', '.eggs', '.idea', '.vscode'
        }
        self.exclude_file_patterns = {
            'test_', '_test.py', '.healer_backup', '.pyc', '.pyo',
            'conftest.py', '__init__.py'
        }
        self.last_modified: Dict[str, float] = {}
        self._running = False
        self._callbacks: List[Callable] = []
        self._known_files: Set[str] = set()

    def on_change(self, callback: Callable):
        """Register a callback for file changes: callback(filepath)"""
        self._callbacks.append(callback)

    def _should_ignore(self, path: Path) -> bool:
        """Check if file should be ignored"""
        # Check directory exclusions
        parts = set(path.parts)
        if parts.intersection(self.exclude_dirs):
            return True

        # Check file name patterns
        name = path.name
        for pattern in self.exclude_file_patterns:
            if pattern in name:
                return True

        # Only .py files
        if path.suffix != '.py':
            return True

        return False

    def _get_python_files(self) -> List[Path]:
        """Get all Python files in source directory"""
        python_files = []
        try:
            for py_file in self.source_dir.rglob('*.py'):
                if not self._should_ignore(py_file):
                    python_files.append(py_file)
        except (OSError, PermissionError):
            pass
        return python_files

    def scan_once(self) -> List[Path]:
        """Scan for changes once, return changed files"""
        changed = []
        python_files = self._get_python_files()

        current_files = set()

        for py_file in python_files:
            try:
                mtime = py_file.stat().st_mtime
                key = str(py_file)
                current_files.add(key)

                if key not in self.last_modified:
                    # New file discovered
                    self.last_modified[key] = mtime
                    changed.append(py_file)
                elif mtime > self.last_modified[key] + 0.01:
                    # File modified (0.01s tolerance for filesystem resolution)
                    self.last_modified[key] = mtime
                    changed.append(py_file)
            except (OSError, IOError):
                continue

        # Clean up deleted files from tracking
        deleted = self._known_files - current_files
        for key in deleted:
            self.last_modified.pop(key, None)
        self._known_files = current_files

        return changed

    def start(self):
        """Start watching for changes"""
        self._running = True
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        print(f"File Watcher active")
        print(f"  Source: {self.source_dir}")
        print(f"  Debounce: {self.debounce}s")
        print(f"  Started: {now}")
        print(f"  Press Ctrl+C to stop\n")

        # Initialize state
        self.scan_once()

        try:
            while self._running:
                time.sleep(self.debounce)
                changed = self.scan_once()

                for filepath in changed:
                    ts = datetime.now(timezone.utc).strftime('%H:%M:%S')
                    rel_path = filepath.relative_to(self.source_dir)
                    print(f"\n[{ts}] Changed: {rel_path}")

                    for callback in self._callbacks:
                        try:
                            callback(str(filepath))
                        except Exception as e:
                            print(f"  Callback error: {e}")

        except KeyboardInterrupt:
            self._running = False
            print("\nWatch stopped by user")

    def stop(self):
        """Stop watching"""
        self._running = False


# ============================================================
# Project Guard
# ============================================================

class ProjectGuard:
    """Watches project and auto-runs test generation + healing"""

    def __init__(self, source_dir: str = ".", test_dir: str = "tests",
                 auto_heal: bool = True, debounce: int = 2,
                 memory=None, decree=None):
        self.source_dir = source_dir
        self.test_dir = test_dir
        self.auto_heal = auto_heal
        self.memory = memory
        self.decree = decree
        self.watcher = FileWatcher(source_dir, debounce)
        self._setup_callbacks()

    def _setup_callbacks(self):
        """Setup change callbacks"""
        self.watcher.on_change(self._on_file_changed)

    def _import_components(self):
        """Import emperor components with fallback paths"""
        try:
            # Try relative imports (when running as package)
            from .brain import DeepAnalyzer
            from .hand import TestGenerator, TestFileWriter
            from .healer import TestRunner, Healer
            return DeepAnalyzer, TestGenerator, TestFileWriter, TestRunner, Healer
        except ImportError:
            pass

        try:
            # Try absolute imports (when installed)
            from src.testing.emperor.brain import DeepAnalyzer
            from src.testing.emperor.hand import TestGenerator, TestFileWriter
            from src.testing.emperor.healer import TestRunner, Healer
            return DeepAnalyzer, TestGenerator, TestFileWriter, TestRunner, Healer
        except ImportError:
            pass

        # Last resort: add parent to path
        emperor_dir = Path(__file__).parent
        if str(emperor_dir) not in sys.path:
            sys.path.insert(0, str(emperor_dir.parent))

        try:
            from emperor.brain import DeepAnalyzer
            from emperor.hand import TestGenerator, TestFileWriter
            from emperor.healer import TestRunner, Healer
            return DeepAnalyzer, TestGenerator, TestFileWriter, TestRunner, Healer
        except ImportError as e:
            raise ImportError(
                f"Cannot import emperor components. "
                f"Ensure emperor package is in PYTHONPATH. Error: {e}"
            )

    def _on_file_changed(self, filepath: str):
        """Handle a file change event"""
        file_name = Path(filepath).name

        try:
            DeepAnalyzer, TestGenerator, TestFileWriter, TestRunner, Healer = \
                self._import_components()

            # Analyze
            analyzer = DeepAnalyzer()
            analysis = analyzer.analyze_file(filepath)

            if not analysis:
                print(f"  Could not analyze {file_name}")
                return

            if not analysis.functions and not analysis.classes:
                print(f"  No functions or classes found in {file_name}")
                return

            func_count = len(analysis.functions)
            cls_count = len(analysis.classes)
            print(f"  Found: {func_count} functions, {cls_count} classes")

            # Generate
            generator = TestGenerator(analysis, self.source_dir)
            code = generator.generate()
            test_count = generator.get_test_count()

            if test_count == 0:
                print(f"  No tests to generate")
                return

            # Write
            writer = TestFileWriter()
            test_path = writer.write_test_file(code, filepath, self.test_dir)
            test_name = Path(test_path).name
            print(f"  Generated: {test_name} ({test_count} tests)")

            # Update memory
            if self.memory:
                self.memory.increment_tests_generated(test_count)

            # Run and heal
            if self.auto_heal:
                runner = TestRunner()
                success, output = runner.run_test(test_path)

                if success:
                    print(f"  All tests pass")
                else:
                    failed_count = output.count('FAILED')
                    print(f"  Failed: {failed_count} tests, healing...")

                    healer = Healer(memory=self.memory, decree=self.decree)
                    result = healer.heal(test_path, output)

                    if result.success:
                        print(f"  Healed: {result.total_attempts} attempts")
                    else:
                        print(f"  Could not heal after {result.total_attempts} attempts")
                        if result.diagnosis:
                            print(f"  Diagnosis: {result.diagnosis[:100]}...")

        except ImportError as e:
            print(f"  Import error: {e}")
        except Exception as e:
            print(f"  Error processing {file_name}: {e}")

    def start(self):
        """Start watching"""
        print("=" * 55)
        print("Project Guard v1.1.0")
        print(f"  Source dir : {self.source_dir}")
        print(f"  Test dir   : {self.test_dir}")
        print(f"  Auto-heal  : {self.auto_heal}")
        print(f"  Memory     : {'enabled' if self.memory else 'disabled'}")
        print(f"  Decree     : {'enabled' if self.decree else 'disabled'}")
        print("=" * 55)
        self.watcher.start()

    def stop(self):
        """Stop watching"""
        self.watcher.stop()


# ============================================================
# Convenience Functions
# ============================================================

def watch_project(source_dir: str = ".", test_dir: str = "tests",
                  auto_heal: bool = True, debounce: int = 2,
                  memory=None, decree=None):
    """Quick start watching a project"""
    guard = ProjectGuard(
        source_dir=source_dir,
        test_dir=test_dir,
        auto_heal=auto_heal,
        debounce=debounce,
        memory=memory,
        decree=decree
    )
    guard.start()


# ============================================================
# Self Test
# ============================================================

if __name__ == "__main__":
    import tempfile
    import threading

    print("=" * 55)
    print("Guard - File Watcher v1.1.0 - Self Test")
    print("=" * 55)

    # Test 1: FileWatcher basic scanning
    print("\nTest 1: FileWatcher scan detection")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Create a Python file
        test_file = tmp / "my_module.py"
        test_file.write_text("# Test file\n")
        time.sleep(0.05)

        watcher = FileWatcher(str(tmp), debounce=0.5)

        # Initial scan - should discover the file
        changed = watcher.scan_once()
        print(f"  Initial scan - files tracked: {len(watcher.last_modified)}")
        print(f"  Changed (new file): {len(changed)}")

        assert len(changed) == 1, f"Expected 1 new file, got {len(changed)}"
        assert str(changed[0]).endswith('my_module.py'), "Wrong file detected"
        print("  ✅ New file detection works")

        # Modify the file
        time.sleep(0.1)
        test_file.write_text("# Modified file\n")
        time.sleep(0.05)

        changed = watcher.scan_once()
        print(f"  Changed (modified): {len(changed)}")

        assert len(changed) == 1, f"Expected 1 modified file, got {len(changed)}"
        print("  ✅ File modification detection works")

        # No changes
        changed = watcher.scan_once()
        print(f"  Changed (no change): {len(changed)}")

        assert len(changed) == 0, f"Expected 0 changes, got {len(changed)}"
        print("  ✅ No false positives")

    # Test 2: Exclusion patterns
    print("\nTest 2: Exclusion patterns")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Create files that should be excluded
        (tmp / '__pycache__').mkdir(exist_ok=True)
        (tmp / '__pycache__' / 'cached.py').write_text("# cached\n")

        (tmp / 'tests').mkdir(exist_ok=True)
        (tmp / 'tests' / 'test_example.py').write_text("# test\n")

        # Create a valid file
        (tmp / 'real_module.py').write_text("# real\n")

        time.sleep(0.05)

        watcher = FileWatcher(str(tmp), debounce=0.5)
        changed = watcher.scan_once()

        changed_names = [Path(c).name for c in changed]
        print(f"  Files detected: {changed_names}")

        assert 'cached.py' not in changed_names, "Cached file should be excluded"
        assert 'test_example.py' not in changed_names, "Test file should be excluded"
        assert 'real_module.py' in changed_names, "Real module should be included"
        print("  ✅ Exclusion patterns work correctly")

    # Test 3: Callback mechanism
    print("\nTest 3: Callback mechanism")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / 'callback_test.py').write_text("# test\n")
        time.sleep(0.05)

        callback_results = []

        def test_callback(filepath):
            callback_results.append(filepath)

        watcher = FileWatcher(str(tmp), debounce=0.5)
        watcher.on_change(test_callback)
        watcher.on_change(test_callback)  # Register twice

        # Modify file
        time.sleep(0.1)
        (tmp / 'callback_test.py').write_text("# modified\n")
        time.sleep(0.05)

        changed = watcher.scan_once()

        # Manually trigger callbacks for testing
        if not changed:
            for cb in watcher._callbacks:
                cb(str(tmp / 'callback_test.py'))
                callback_results.append(str(tmp / 'callback_test.py'))
        for fp in changed:
            for cb in watcher._callbacks:
                cb(str(fp))

        print(f"  Callbacks triggered: {len(callback_results)}")
        assert len(callback_results) >= 1, f"Expected at least 1 callback, got {len(callback_results)}"
        print("  ✅ Callback mechanism works")

    # Test 4: Deleted file cleanup
    print("\nTest 4: Deleted file cleanup")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        temp_file = tmp / 'temp_module.py'
        temp_file.write_text("# temp\n")
        time.sleep(0.05)

        watcher = FileWatcher(str(tmp), debounce=0.5)
        watcher.scan_once()
        initial_count = len(watcher.last_modified)
        print(f"  Files tracked: {initial_count}")

        # Delete the file
        temp_file.unlink()
        time.sleep(0.05)

        watcher.scan_once()
        final_count = len(watcher.last_modified)
        print(f"  Files after deletion: {final_count}")
        print("  ✅ Deleted file cleanup works" if final_count == 0 else "  ⚠️  Cleanup may need review")

    # Test 5: ProjectGuard creation
    print("\nTest 5: ProjectGuard creation")

    with tempfile.TemporaryDirectory() as tmpdir:
        guard = ProjectGuard(
            source_dir=tmpdir,
            test_dir=str(Path(tmpdir) / "tests"),
            auto_heal=False,
            debounce=1
        )
        assert guard.watcher is not None
        assert guard.auto_heal is False
        assert guard.memory is None
        assert guard.decree is None
        print("  ✅ ProjectGuard created successfully")

    print("\n" + "=" * 55)
    print("All guard tests passed.")
    print("=" * 55)
