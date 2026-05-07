"""
Emperor - Supreme Coordinator v2.0.0
Simple CLI: etest [target] [flags]
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, List

# Ensure emperor package is importable
_emperor_dir = Path(__file__).parent
if str(_emperor_dir) not in sys.path:
    sys.path.insert(0, str(_emperor_dir.parent))

# ============================================================
# Version
# ============================================================

__version__ = "2.0.0"

# ============================================================
# Emperor Core
# ============================================================

class Emperor:
    """Supreme coordinator - simple and direct"""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self._memory = None
        self._decree = None
        self._eye = None
        self._brain = None
        self._hand = None
        self._healer = None
        self._guard = None

    @property
    def memory(self):
        if self._memory is None:
            from src.testing.emperor.memory import ImperialMemory
            self._memory = ImperialMemory()
        return self._memory

    @property
    def decree(self):
        if self._decree is None:
            from src.testing.emperor.decree import Decree
            self._decree = Decree(quiet=self.quiet)
        return self._decree

    @property
    def eye(self):
        if self._eye is None:
            from src.testing.emperor.eye import ProjectScanner
            self._eye = ProjectScanner()
        return self._eye

    @property
    def brain(self):
        if self._brain is None:
            from src.testing.emperor.brain import DeepAnalyzer
            self._brain = DeepAnalyzer()
        return self._brain

    @property
    def healer(self):
        if self._healer is None:
            from src.testing.emperor.healer import Healer
            self._healer = Healer(memory=self.memory, decree=self.decree)
        return self._healer

    # ============================================================
    # COMMAND: etest (Analyze + Generate + Fix)
    # ============================================================

    def cmd_test(self, targets: List[str]) -> int:
        """Analyze, generate tests, run, and heal"""
        if not targets:
            targets = ['.']

        all_analyses = []
        total_functions = 0
        total_classes = 0
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_healed = 0
        total_skipped = 0

        self.decree.header("etest - Generating Tests")

        for target in targets:
            target_path = Path(target).resolve()

            if not target_path.exists():
                self.decree.error(f"Not found: {target}")
                continue

            # Single file
            if target_path.is_file() and target_path.suffix == '.py':
                analysis = self._analyze_file(str(target_path))
                if analysis:
                    all_analyses.append(analysis)
                    self._print_analysis(analysis)

            # Directory
            elif target_path.is_dir():
                directory_analyses = self._analyze_directory(str(target_path))
                all_analyses.extend(directory_analyses)
                for a in directory_analyses:
                    self._print_analysis(a)

        if not all_analyses:
            self.decree.warning("No Python files found")
            return 0

        # Generate tests for each analysis
        from src.testing.emperor.hand import TestGenerator, TestFileWriter

        for analysis in all_analyses:
            generator = TestGenerator(analysis, str(Path(analysis.filepath).parent))
            code = generator.generate()
            test_count = generator.get_test_count()

            if test_count > 0:
                writer = TestFileWriter()
                test_path = writer.write_test_file(code, analysis.filepath)
                if test_path:
                    total_tests += test_count
                    self.memory.increment_tests_generated(test_count)
                    print(f"   🤲 {Path(test_path).name}: {test_count} tests")

        if total_tests == 0:
            self.decree.info("No tests generated")
            return 0

        print()
        self.decree.info(f"Running tests...")

        # Run and heal tests
        from src.testing.emperor.healer import TestRunner

        test_dir = Path('tests')
        if test_dir.exists():
            test_files = list(test_dir.rglob('test_*.py'))

            for tf in test_files:
                runner = TestRunner()
                success, output = runner.run_test(str(tf))

                if success:
                    passed = output.count('PASSED')
                    total_passed += passed
                    status = "✅" if passed > 0 else "⚠️"
                    print(f"   {status} {tf.name}: {passed} passed")
                else:
                    failed = output.count('FAILED')
                    total_failed += failed
                    print(f"   ❌ {tf.name}: {failed} failed - healing...")

                    result = self.healer.heal(str(tf), output)
                    if result.success:
                        total_healed += failed
                        total_failed -= failed
                        print(f"      🔧 healed in {result.total_attempts} attempts")
                    else:
                        total_skipped += failed
                        print(f"      📜 could not heal")

        # Summary
        print()
        print(f"   {'─' * 40}")
        print(f"   Tests: {total_tests} | Passed: {total_passed} | Healed: {total_healed} | Skipped: {total_skipped}")
        print(f"   {'─' * 40}")

        self.memory.save()
        print(f"\n✅ Done")
        return 0 if total_skipped == 0 else 1

    # ============================================================
    # COMMAND: etest -f (Fix existing tests)
    # ============================================================

    def cmd_fix(self, targets: List[str]) -> int:
        """Fix existing failing tests without regenerating"""
        if not targets:
            targets = ['tests']

        self.decree.header("etest - Fixing Tests")

        from src.testing.emperor.healer import TestRunner

        total_tests = 0
        total_passed = 0
        total_healed = 0
        total_skipped = 0

        for target in targets:
            target_path = Path(target)

            if not target_path.exists():
                self.decree.error(f"Not found: {target}")
                continue

            # Get test files
            if target_path.is_file():
                test_files = [target_path]
            else:
                test_files = list(target_path.rglob('test_*.py'))

            for tf in test_files:
                runner = TestRunner()
                success, output = runner.run_test(str(tf))

                if success:
                    passed = output.count('PASSED')
                    total_passed += passed
                    total_tests += passed
                    print(f"   ✅ {tf.name}: {passed} passed (untouched)")
                else:
                    passed = output.count('PASSED')
                    failed = output.count('FAILED')
                    total_passed += passed
                    total_tests += passed + failed
                    print(f"   🔧 {tf.name}: {passed} passed, {failed} failed")

                    result = self.healer.heal(str(tf), output)
                    if result.success:
                        total_healed += failed
                        print(f"      ✅ healed in {result.total_attempts} attempts")
                    else:
                        total_skipped += 1
                        print(f"      📜 skipped: {result.diagnosis[:80] if result.diagnosis else 'unknown'}...")

        print()
        print(f"   {'─' * 40}")
        total = total_passed + total_healed + total_skipped
        print(f"   Total: {total} | Passed: {total_passed} | Healed: {total_healed} | Skipped: {total_skipped}")
        print(f"   {'─' * 40}")

        self.memory.save()
        print(f"\n✅ Done")
        return 0 if total_skipped == 0 else 1

    # ============================================================
    # COMMAND: etest -w (Watch)
    # ============================================================

    def cmd_watch(self, targets: List[str]) -> int:
        """Watch files and auto-run on changes"""
        if not targets:
            targets = ['.']

        self.decree.header("etest - Watch Mode")

        from src.testing.emperor.guard import FileWatcher
        from src.testing.emperor.hand import TestGenerator, TestFileWriter
        from src.testing.emperor.healer import TestRunner

        def on_change(filepath: str):
            rel = Path(filepath).relative_to(Path.cwd())
            print(f"\n   📄 {rel}")

            analysis = self._analyze_file(filepath)
            if not analysis:
                return

            generator = TestGenerator(analysis, str(Path(filepath).parent))
            code = generator.generate()
            test_count = generator.get_test_count()

            if test_count == 0:
                return

            writer = TestFileWriter()
            test_path = writer.write_test_file(code, filepath)
            print(f"   🤲 {Path(test_path).name}: {test_count} tests")

            runner = TestRunner()
            success, output = runner.run_test(test_path)
            if success:
                print(f"   ✅ All pass")
            else:
                print(f"   🔧 Healing...")
                result = self.healer.heal(test_path, output)
                if result.success:
                    print(f"   ✅ Healed")
                else:
                    print(f"   📜 Could not heal")

            self.memory.save()

        watcher = FileWatcher(targets[0])
        watcher.on_change(on_change)

        try:
            watcher.start()
        except KeyboardInterrupt:
            print("\n👁️ Watch stopped")

        return 0

    # ============================================================
    # COMMAND: etest -r (Report)
    # ============================================================

    def cmd_report(self) -> int:
        """Show memory statistics"""
        self.decree.header("etest - Report")

        stats = self.memory.get_statistics()

        print(f"   Sessions: {stats['total_runs']}")
        print(f"   Tests generated: {stats['total_tests_generated']}")
        print(f"   Fixes applied: {stats['total_fixes_applied']}")
        print(f"   Fixes failed: {stats['total_fixes_failed']}")
        print(f"   Success rate: {stats['success_rate']}%")
        print(f"   Error patterns: {stats['total_patterns']}")
        print(f"   Files tracked: {stats['files_tracked']}")
        print()

        top_errors = self.memory.get_top_errors(5)
        if top_errors:
            print("   Top errors:")
            for e in top_errors:
                print(f"   - {e['type']}: {e['count']}x")

        problematic = self.memory.get_problematic_files()
        if problematic:
            print(f"\n   Problematic files: {len(problematic)}")
            for f in problematic[:5]:
                rep = self.memory.get_file_reputation(f)
                print(f"   - {f}: {rep['reputation']}")

        return 0

    # ============================================================
    # COMMAND: etest -i (Integration)
    # ============================================================

    def cmd_integration(self, targets: List[str]) -> int:
        """Generate and run integration tests between files"""
        if len(targets) < 2:
            self.decree.error("Need at least 2 files or directories for integration testing")
            return 1

        self.decree.header("etest - Integration Tests")

        from src.testing.emperor.hand import TestGenerator, TestFileWriter
        from src.testing.emperor.healer import TestRunner

        all_analyses = []

        for target in targets:
            target_path = Path(target)
            if target_path.is_file():
                analysis = self._analyze_file(str(target_path))
                if analysis:
                    all_analyses.append(analysis)
            elif target_path.is_dir():
                analyses = self._analyze_directory(str(target_path))
                all_analyses.extend(analyses)

        if len(all_analyses) < 2:
            self.decree.error("Need at least 2 files to integrate")
            return 1

        # Merge analyses for integration
        merged = all_analyses[0]
        for a in all_analyses[1:]:
            merged.functions.extend(a.functions)
            merged.classes.extend(a.classes)

        # Discover relationships between them
        merged.relationships = []
        for i, a1 in enumerate(all_analyses):
            for j, a2 in enumerate(all_analyses):
                if i >= j:
                    continue
                for f1 in a1.functions:
                    for f2 in a2.functions:
                        if f2.name in f1.calls:
                            merged.relationships.append({
                                'caller': f1.name,
                                'callee': f2.name
                            })

        if not merged.relationships:
            self.decree.warning("No relationships found between files")
            return 0

        print(f"   🔗 {len(merged.relationships)} relationships found:")
        for r in merged.relationships:
            print(f"   - {r['caller']} → {r['callee']}")

        # Generate integration tests
        merged.filepath = str(Path(targets[0]).parent / "integration")
        generator = TestGenerator(merged, str(Path(targets[0]).parent))
        code = generator.generate()
        test_count = generator.get_test_count()

        if test_count > 0:
            writer = TestFileWriter()
            test_path = writer.write_test_file(code, merged.filepath)
            print(f"\n   🤲 {Path(test_path).name}: {test_count} integration tests")

            runner = TestRunner()
            success, output = runner.run_test(test_path)
            if success:
                print(f"   ✅ All pass")
            else:
                print(f"   🔧 Healing...")
                result = self.healer.heal(test_path, output)
                if result.success:
                    print(f"   ✅ Healed")
                else:
                    print(f"   📜 Could not heal all")

        self.memory.save()
        print(f"\n✅ Done")
        return 0

    # ============================================================
    # Helpers
    # ============================================================

    def _analyze_file(self, filepath: str) -> Optional[any]:
        """Analyze a single file"""
        return self.brain.analyze_file(filepath)

    def _analyze_directory(self, directory: str) -> List:
        """Analyze all Python files in a directory"""
        analyses = []
        for py_file in Path(directory).rglob('*.py'):
            if 'test_' not in py_file.name and not py_file.name.startswith('_'):
                analysis = self.brain.analyze_file(str(py_file))
                if analysis:
                    analyses.append(analysis)
        return analyses

    def _print_analysis(self, analysis) -> None:
        """Print a single analysis"""
        name = Path(analysis.filepath).name
        funcs = len(analysis.functions)
        classes = len(analysis.classes)
        if funcs > 0 or classes > 0:
            print(f"   🧠 {name}: {funcs} functions, {classes} classes")


# ============================================================
# CLI Interface
# ============================================================

def parse_args(args: List[str]) -> tuple:
    """Parse simplified CLI arguments"""
    flags = {
        'fix': False,
        'watch': False,
        'report': False,
        'integration': False,
    }

    targets = []
    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ('-f', '--fix'):
            flags['fix'] = True
        elif arg in ('-w', '--watch'):
            flags['watch'] = True
        elif arg in ('-r', '--report'):
            flags['report'] = True
        elif arg in ('-i', '--integration'):
            flags['integration'] = True
        elif arg in ('-h', '--help'):
            return None, None, True
        else:
            targets.append(arg)

        i += 1

    return flags, targets, False


def show_help():
    """Show help message"""
    print("""
╔══════════════════════════════════════════════╗
║           👑 etest v2.0.0                    ║
║     Intelligent Test Generator               ║
╚══════════════════════════════════════════════╝

Usage: etest [targets...] [flags]

Flags:
  (none)     Analyze, generate tests, run, and heal
  -f         Fix existing failing tests
  -w         Watch files and auto-run on changes
  -r         Show memory report
  -i         Generate integration tests
  -h         Show this help

Examples:
  etest                          # Full project
  etest src/auth.py              # Single file
  etest src/                     # Directory
  etest src/models/ src/api/     # Multiple directories
  etest -f                       # Fix all tests
  etest -f tests/test_auth.py    # Fix specific test file
  etest -w                       # Watch mode
  etest -w src/                  # Watch specific directory
  etest -r                       # Show report
  etest -i src/auth.py src/db.py # Integration test
  etest -i src/services/         # Integration for directory

For more: https://github.com/emperor-test-gen
""")


def main(args: List[str] = None) -> int:
    """Main entry point"""
    if args is None:
        args = sys.argv[1:]

    # Remove 'etest' if it's the first argument
    if args and args[0] == 'etest':
        args = args[1:]

    # Parse
    flags, targets, show_help_flag = parse_args(args)

    if show_help_flag or (not flags['fix'] and not flags['watch'] and
                          not flags['report'] and not flags['integration'] and not targets):
        show_help()
        return 0

    # Create emperor
    emperor = Emperor()

    try:
        # Route command
        if flags['fix']:
            return emperor.cmd_fix(targets)
        elif flags['watch']:
            return emperor.cmd_watch(targets)
        elif flags['report']:
            return emperor.cmd_report()
        elif flags['integration']:
            return emperor.cmd_integration(targets if targets else ['.'])
        else:
            return emperor.cmd_test(targets if targets else ['.'])

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"\nFatal error: {e}")
        return 1


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    sys.exit(main())
