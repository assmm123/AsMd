"""
Decree - Reports and Announcements v1.1.0
Formatted output, progress tracking, reports, and decrees
"""

import os
import sys
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple

# ============================================================
# Terminal Colors
# ============================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ============================================================
# Icons
# ============================================================

ICONS = {
    'crown': '👑',
    'eye': '👁️',
    'brain': '🧠',
    'hand': '🤲',
    'healer': '🔧',
    'memory': '🧬',
    'guard': '🛡️',
    'success': '✅',
    'fail': '❌',
    'warn': '⚠️',
    'info': 'ℹ️',
    'test': '🧪',
    'file': '📄',
    'folder': '📁',
    'clock': '⏱️',
    'sparkles': '✨',
    'scroll': '📜',
    'target': '🎯',
    'rocket': '🚀',
}

# ============================================================
# Decree System
# ============================================================

class Decree:
    """Report and announcement system"""

    def __init__(self, quiet: bool = False, color: bool = True):
        self.quiet = quiet
        self.color = color
        self.start_time: Optional[datetime] = None
        self.stats = {
            'files_scanned': 0,
            'functions_analyzed': 0,
            'classes_analyzed': 0,
            'tests_generated': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'fixes_applied': 0,
            'fixes_failed': 0,
            'scenarios_found': 0,
        }

    # ============================================================
    # Core Output
    # ============================================================

    def _print(self, text: str, color: str = "", icon: str = ""):
        """Print with color and icon"""
        if self.quiet:
            return
        prefix = f"{icon} " if icon else ""
        if self.color and color:
            print(f"{color}{prefix}{text}{Colors.END}")
        else:
            print(f"{prefix}{text}")

    def _divider(self, char: str = "═", length: int = 60):
        """Horizontal divider"""
        if not self.quiet:
            print(char * length)

    def _now(self) -> str:
        """Current UTC timestamp"""
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # ============================================================
    # Phase Reports
    # ============================================================

    def startup(self, project_name: str = "Unknown"):
        """Session startup announcement"""
        self.start_time = datetime.now(timezone.utc)
        self._divider("═")
        self._print(" Imperial Test Generator ", Colors.HEADER + Colors.BOLD, ICONS['crown'])
        self._print(" Emperor System v1.0.0", Colors.CYAN)
        self._divider("─")
        self._print(f" Project: {project_name}", Colors.BLUE, ICONS['folder'])
        self._print(f" Started: {self._now()}", Colors.DIM, ICONS['clock'])
        self._divider("═")
        print()

    def scan_report(self, files_count: int, source_files: int,
                    test_files: int, other_files: int):
        """Scan phase report"""
        self.stats['files_scanned'] = files_count
        self._print(f" Scanning complete: {files_count} files found", Colors.CYAN, ICONS['eye'])
        self._print(f"   Source: {source_files} | Tests: {test_files} | Other: {other_files}",
                    Colors.DIM)
        print()

    def analysis_report(self, functions: int, classes: int,
                        imports: int, scenarios: int, duration: float = 0):
        """Analysis phase report"""
        self.stats['functions_analyzed'] = functions
        self.stats['classes_analyzed'] = classes
        self.stats['scenarios_found'] = scenarios
        self._print(f" Analysis complete: {functions} functions, {classes} classes",
                    Colors.CYAN, ICONS['brain'])
        if scenarios > 0:
            self._print(f"   Scenarios discovered: {scenarios}", Colors.GREEN, ICONS['sparkles'])
        if duration > 0:
            self._print(f"   Duration: {duration:.2f}s", Colors.DIM)
        print()

    def generation_report(self, tests_generated: int, files_created: int):
        """Test generation report"""
        self.stats['tests_generated'] = tests_generated
        self._print(f" Tests generated: {tests_generated} tests in {files_created} files",
                    Colors.GREEN, ICONS['hand'])
        print()

    def test_run_report(self, passed: int, failed: int, total: int, duration: float = 0):
        """Test execution report"""
        self.stats['tests_passed'] = passed
        self.stats['tests_failed'] = failed
        rate = (passed / max(total, 1)) * 100
        icon = ICONS['success'] if failed == 0 else ICONS['warn']
        color = Colors.GREEN if failed == 0 else Colors.YELLOW
        self._print(f" Tests: {passed}/{total} passed ({rate:.0f}%)", color, icon)
        if failed > 0:
            self._print(f"   Failed: {failed}", Colors.RED)
        if duration > 0:
            self._print(f"   Duration: {duration:.2f}s", Colors.DIM)
        print()

    # ============================================================
    # Healing Reports
    # ============================================================

    def heal_progress(self, attempt: int, max_attempts: int,
                      level: str, strategy: str,
                      success: bool, error_type: str = ""):
        """Healing attempt progress"""
        LEVEL_NAMES = {
            'surface': 'Surface',
            'structural': 'Structural',
            'rewrite': 'Rewrite',
            'memory': 'Memory Search',
            'investigation': 'Deep Investigation',
        }
        level_name = LEVEL_NAMES.get(level, level)
        icon = '✅' if success else '❌'
        color = Colors.GREEN if success else Colors.RED
        self._print(
            f"   [{attempt}/{max_attempts}] {level_name}: {strategy} {icon}",
            color
        )

    def heal_summary(self, total_attempts: int, successful: bool,
                     error_type: str = "", test_name: str = ""):
        """Healing summary"""
        if successful:
            self.stats['fixes_applied'] += 1
            self._print(
                f" Healed: {test_name} ({error_type}) - {total_attempts} attempts",
                Colors.GREEN, ICONS['healer']
            )
        else:
            self.stats['fixes_failed'] += 1
            self._print(
                f" Failed to heal: {test_name} ({error_type}) - {total_attempts} attempts",
                Colors.RED, ICONS['fail']
            )
        print()

    def progress_bar(self, current: int, total: int, label: str = "", width: int = 30):
        """Animated progress bar"""
        if self.quiet:
            return
        filled = int(width * current / max(total, 1))
        bar = '█' * filled + '░' * (width - filled)
        pct = (current / max(total, 1)) * 100
        sys.stdout.write(f'\r{label} [{bar}] {pct:.0f}%')
        sys.stdout.flush()
        if current >= total:
            sys.stdout.write('\n')

    # ============================================================
    # General Messages
    # ============================================================

    def info(self, text: str):
        """Info message"""
        self._print(text, Colors.BLUE, ICONS['info'])

    def success(self, text: str):
        """Success message"""
        self._print(text, Colors.GREEN, ICONS['success'])

    def warning(self, text: str):
        """Warning message"""
        self._print(text, Colors.YELLOW, ICONS['warn'])

    def error(self, text: str):
        """Error message"""
        self._print(text, Colors.RED, ICONS['fail'])

    def header(self, text: str):
        """Imperial header message"""
        self._divider("━")
        self._print(f" {text} ", Colors.HEADER + Colors.BOLD, ICONS['crown'])
        self._divider("━")

    # ============================================================
    # Imperial Skip Decree (after 15 failed attempts)
    # ============================================================

    def issue_skip_decree(self, function_name: str, file_path: str,
                          error_type: str, attempts: int,
                          diagnosis: str, suggestions: List[str],
                          test_file: str = "", test_name: str = ""):
        """Issue a decree when all healing attempts fail"""
        self._divider("═")
        self._print("", Colors.HEADER)
        self._print("  👑  IMPERIAL DECREE  👑", Colors.HEADER + Colors.BOLD)
        self._print("", Colors.HEADER)
        self._divider("─")
        self._print(f"  Function : {function_name}", Colors.RED)
        self._print(f"  File     : {file_path}", Colors.RED)
        self._print(f"  Error    : {error_type}", Colors.RED)
        self._print(f"  Attempts : {attempts} (all levels exhausted)", Colors.RED)
        if test_file:
            self._print(f"  Test     : {test_file}::{test_name}", Colors.RED)
        self._print("", Colors.END)
        self._print(f"  Diagnosis: {diagnosis}", Colors.YELLOW)
        self._print("", Colors.END)
        if suggestions:
            self._print("  Suggestions:", Colors.GREEN)
            for i, s in enumerate(suggestions, 1):
                self._print(f"    {i}. {s}", Colors.GREEN)
        self._print("", Colors.END)
        self._print("  Action: @pytest.mark.skip added - test skipped for review", Colors.DIM)
        self._divider("═")
        print()

    def generate_skip_marker(self, reason: str) -> str:
        """Generate a pytest skip marker"""
        safe_reason = reason.replace('"', "'")
        return f'@pytest.mark.skip(reason="{safe_reason}")'

    # ============================================================
    # Final Report
    # ============================================================

    def final_report(self) -> Dict[str, Any]:
        """Final session report - returns stats dict"""
        elapsed = ""
        duration_seconds = 0.0
        if self.start_time:
            duration_seconds = (datetime.now(timezone.utc) - self.start_time).total_seconds()
            elapsed = f" | {duration_seconds:.1f}s"

        self._divider("═")
        self._print(" Session Complete ", Colors.HEADER + Colors.BOLD, ICONS['crown'])
        self._divider("─")
        self._print(f" Files scanned    : {self.stats['files_scanned']}", Colors.DIM)
        self._print(f" Functions found  : {self.stats['functions_analyzed']}", Colors.DIM)
        self._print(f" Classes found    : {self.stats['classes_analyzed']}", Colors.DIM)
        self._print(f" Tests generated  : {self.stats['tests_generated']}", Colors.GREEN)
        self._print(f" Tests passed     : {self.stats['tests_passed']}", Colors.GREEN)
        self._print(f" Fixes applied    : {self.stats['fixes_applied']}", Colors.GREEN, ICONS['healer'])
        self._print(f" Fixes failed     : {self.stats['fixes_failed']}", Colors.RED, ICONS['fail'])
        self._print(f" Scenarios        : {self.stats['scenarios_found']}", Colors.CYAN)
        self._divider("─")

        # Verdict
        total_fixes = self.stats['fixes_applied'] + self.stats['fixes_failed']
        if total_fixes == 0 and self.stats['tests_failed'] == 0:
            verdict = "ALL TESTS PASS - System is strong!"
            color = Colors.GREEN + Colors.BOLD
            verdict_level = "excellent"
        elif self.stats['fixes_failed'] == 0:
            verdict = "ALL ISSUES RESOLVED"
            color = Colors.GREEN
            verdict_level = "good"
        elif self.stats['fixes_applied'] > self.stats['fixes_failed']:
            verdict = "PARTIAL SUCCESS - Check skipped tests"
            color = Colors.YELLOW
            verdict_level = "warning"
        else:
            verdict = "NEEDS MANUAL INTERVENTION"
            color = Colors.RED
            verdict_level = "critical"

        self._print(f" {ICONS['crown']} {verdict} {ICONS['crown']} ", color)
        self._divider("═")
        print()

        return {
            'verdict': verdict,
            'verdict_level': verdict_level,
            'stats': self.stats.copy(),
            'duration_seconds': duration_seconds,
            'timestamp': self._now(),
        }

    # ============================================================
    # HTML Report
    # ============================================================

    def _render_html_template(self, results: List[Dict], passed: int,
                              failed: int, rate: float) -> str:
        """Render HTML template"""
        rows = []
        for r in results:
            if r.get('skipped'):
                status = 'skipped'
                badge_class = 'badge-skip'
            elif r.get('passed'):
                status = 'pass'
                badge_class = 'badge-pass'
            else:
                status = 'fail'
                badge_class = 'badge-fail'
            d = r.get('duration', '-')
            rows.append(
                f'<tr><td>{r["name"]}</td>'
                f'<td><span class="badge {badge_class}">{status.upper()}</span></td>'
                f'<td>{d}</td></tr>'
            )

        return f'''<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>Test Report</title>
<style>
body{{font-family:sans-serif;background:#0f0f1a;color:#e0e0e0;padding:20px}}
h1{{color:#7c3aed;text-align:center}}
.summary{{background:#1a1a2e;padding:15px;border-radius:8px;margin:15px 0;text-align:center}}
.pass{{color:#22c55e}}.fail{{color:#ef4444}}
table{{width:100%;border-collapse:collapse;margin-top:15px}}
th{{background:#7c3aed;padding:10px}}
td{{padding:8px;border:1px solid #333}}
tr:nth-child(even){{background:#1a1a2e}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px}}
.badge-pass{{background:#064e3b;color:#22c55e}}
.badge-fail{{background:#7f1d1d;color:#fca5a5}}
.badge-skip{{background:#1e3a5f;color:#93c5fd}}
</style>
</head>
<body>
<h1>Test Report</h1>
<div class="summary">
<h2>{passed}/{len(results)} Passed ({rate:.0f}%)</h2>
<p>{self._now()}</p>
</div>
<table>
<tr><th>Test</th><th>Status</th><th>Duration</th></tr>
{''.join(rows)}
</table>
</body>
</html>'''

    def generate_html_report(self, results: List[Dict],
                             output_path: str = "test_report.html") -> Optional[str]:
        """Generate HTML test report"""
        try:
            passed = sum(1 for r in results if r.get('passed') and not r.get('skipped'))
            skipped = sum(1 for r in results if r.get('skipped'))
            failed = len(results) - passed - skipped
            rate = (passed / max(len(results), 1)) * 100

            html = self._render_html_template(results, passed, failed, rate)

            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            self.success(f"HTML report: {output_path}")
            return output_path
        except IOError as e:
            self.error(f"Failed to write HTML report: {e}")
            return None


# ============================================================
# Self Test
# ============================================================


# ============================================================
# Global Instance
# ============================================================

_decree_instance = None

def get_decree(quiet: bool = False):
    """Get or create global decree instance"""
    global _decree_instance
    if _decree_instance is None:
        _decree_instance = Decree(quiet=quiet)
    return _decree_instance


if __name__ == "__main__":

    print("=" * 60)
    print("Decree System v1.1.0 - Self Test")
    print("=" * 60)

    decree = Decree()

    # Phase reports
    decree.startup("TestProject")
    decree.scan_report(42, 30, 8, 4)
    decree.analysis_report(150, 25, 40, 5, 1.5)
    decree.generation_report(200, 15)
    decree.test_run_report(180, 20, 200, 3.2)

    # Healing
    decree.heal_progress(1, 15, "surface", "fix_types", True, "TypeError")
    decree.heal_progress(5, 15, "structural", "add_mocks", False, "ImportError")
    decree.heal_summary(3, True, "TypeError", "test_auth")
    decree.heal_summary(15, False, "TypeError", "test_complex")

    # Progress bar demo
    print("Progress bar demo:")
    import time
    for i in range(1, 11):
        decree.progress_bar(i, 10, "Healing", 20)
        time.sleep(0.05)

    # Skip decree
    decree.issue_skip_decree(
        function_name="complex_calculation",
        file_path="src/math.py",
        error_type="TypeError",
        attempts=15,
        diagnosis="Function uses dynamic type inference without annotations",
        suggestions=[
            "Add type hints to function arguments",
            "Split function into smaller single-purpose functions",
            "Add input validation at function entry"
        ],
        test_file="tests/test_math.py",
        test_name="test_complex_calculation"
    )

    # Skip marker
    marker = decree.generate_skip_marker("Dynamic type inference - needs review")
    print(f"Skip marker: {marker}\n")

    # Final report
    result = decree.final_report()
    print(f"Verdict: {result['verdict']}")
    print(f"Level: {result['verdict_level']}")
    print(f"Duration: {result['duration_seconds']:.1f}s")

    # HTML report
    test_results = [
        {'name': 'test_one', 'passed': True, 'duration': '0.1s'},
        {'name': 'test_two', 'passed': False, 'duration': '0.2s'},
        {'name': 'test_three', 'passed': True, 'duration': '0.1s'},
        {'name': 'test_skip', 'passed': False, 'skipped': True, 'duration': '-'},
    ]
    path = decree.generate_html_report(test_results)
    if path and os.path.exists(path):
        print(f"\nHTML report size: {os.path.getsize(path)} bytes")
        os.remove(path)

    print("\nSelf test complete.")
