"""
Eye - Project Scanner v1.1.0
Project scanning, file discovery, classification, quick analysis, and gap detection
"""

import os
import ast
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field

# ============================================================
# Constants
# ============================================================

SOURCE_EXTENSIONS = {'.py'}
JS_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx'}
CONFIG_EXTENSIONS = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'}
WEB_EXTENSIONS = {'.html', '.css', '.scss', '.less'}
DATA_EXTENSIONS = {'.csv', '.tsv', '.xml', '.sql', '.sqlite', '.db'}
DOC_EXTENSIONS = {'.md', '.rst', '.txt'}

TEST_PATTERNS = ['test_', '_test', 'tests/']
EXCLUDE_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'node_modules',
    '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build',
    'egg-info', '.eggs', '.idea', '.vscode'
}

MAX_FILE_SIZE_KB = 500
PEEK_LINES = 60

# ============================================================
# Data Structures
# ============================================================

@dataclass
class ScannedFile:
    """A scanned file with metadata"""
    path: str
    name: str
    extension: str
    size_kb: float
    classification: str  # source, test, config, data, document, javascript, web, unknown


@dataclass
class FilePeek:
    """Quick analysis of a file's content"""
    path: str
    has_imports: bool = False
    has_classes: bool = False
    has_functions: bool = False
    has_async: bool = False
    has_type_hints: bool = False
    is_executable: bool = False
    import_count: int = 0
    class_count: int = 0
    function_count: int = 0
    docstring: str = ""


@dataclass
class TestGapReport:
    """Report on test coverage gaps"""
    total_sources: int = 0
    tested_count: int = 0
    untested_count: int = 0
    coverage_pct: float = 0.0
    untested_files: List[str] = field(default_factory=list)
    tested_files: List[str] = field(default_factory=list)


@dataclass
class ProjectMap:
    """Complete project map"""
    source_dir: str
    total_files: int = 0
    source_files: List[ScannedFile] = field(default_factory=list)
    test_files: List[ScannedFile] = field(default_factory=list)
    config_files: List[ScannedFile] = field(default_factory=list)
    javascript_files: List[ScannedFile] = field(default_factory=list)
    web_files: List[ScannedFile] = field(default_factory=list)
    data_files: List[ScannedFile] = field(default_factory=list)
    doc_files: List[ScannedFile] = field(default_factory=list)
    other_files: List[ScannedFile] = field(default_factory=list)
    directory_tree: Dict = field(default_factory=dict)
    is_python_package: bool = False
    has_src_layout: bool = False
    test_gap: Optional[TestGapReport] = None
    file_peeks: Dict[str, FilePeek] = field(default_factory=dict)


# ============================================================
# Project Scanner
# ============================================================

class ProjectScanner:
    """Scans and classifies files in a project directory"""

    def __init__(self, exclude_dirs: Set[str] = None, max_file_size_kb: int = MAX_FILE_SIZE_KB):
        self.exclude_dirs = exclude_dirs or EXCLUDE_DIRS
        self.max_file_size = max_file_size_kb * 1024

    # ============================================================
    # Main Scan
    # ============================================================

    def scan(self, source_dir: str, quick_peek: bool = True, find_gaps: bool = True) -> ProjectMap:
        """Full project scan"""
        source_path = Path(source_dir).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"Directory not found: {source_dir}")

        project_map = ProjectMap(source_dir=str(source_path))

        # Walk the directory tree
        for root, dirs, files in os.walk(str(source_path)):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    stat = os.stat(filepath)
                    if stat.st_size > self.max_file_size:
                        continue

                    size_kb = stat.st_size / 1024
                    ext = Path(filename).suffix.lower()
                    classification = self._classify(filepath, filename, ext)

                    file_entry = ScannedFile(
                        path=filepath,
                        name=filename,
                        extension=ext,
                        size_kb=round(size_kb, 2),
                        classification=classification
                    )

                    self._add_to_category(project_map, file_entry)

                except (OSError, IOError):
                    continue

        # Post-scan analysis
        project_map.total_files = self._count_all(project_map)
        project_map.is_python_package = self._is_python_package(source_path)
        project_map.has_src_layout = self._has_src_layout(source_path)
        project_map.directory_tree = self._build_tree(source_path)

        if quick_peek:
            project_map.file_peeks = self.peek_source_files(project_map.source_files)

        if find_gaps:
            project_map.test_gap = self.find_test_gaps_from_map(project_map)

        return project_map

    # ============================================================
    # Classification
    # ============================================================

    def _classify(self, filepath: str, filename: str, ext: str) -> str:
        """Classify a single file"""
        path_lower = filepath.lower()
        name_lower = filename.lower()

        # ملفات تبدأ بـ test_ أو تنتهي بـ _test أو داخل مجلد tests/
        if name_lower.startswith('test_') or '_test.' in name_lower or '/tests/' in path_lower or '\\tests\\' in path_lower:
            return 'test'

        # Source code
        if ext in SOURCE_EXTENSIONS:
            return 'source'

        # JavaScript (separate from Python source)
        if ext in JS_EXTENSIONS:
            return 'javascript'

        # Configuration
        if ext in CONFIG_EXTENSIONS:
            return 'config'

        # Web
        if ext in WEB_EXTENSIONS:
            return 'web'

        # Data
        if ext in DATA_EXTENSIONS:
            return 'data'

        # Documentation
        if ext in DOC_EXTENSIONS:
            return 'document'

        return 'unknown'

    def _add_to_category(self, pm: ProjectMap, entry: ScannedFile):
        """Add file to correct category"""
        category_map = {
            'source': pm.source_files,
            'test': pm.test_files,
            'config': pm.config_files,
            'javascript': pm.javascript_files,
            'web': pm.web_files,
            'data': pm.data_files,
            'document': pm.doc_files,
        }
        target = category_map.get(entry.classification, pm.other_files)
        target.append(entry)

    def _count_all(self, pm: ProjectMap) -> int:
        """Count all files in project map"""
        return (
            len(pm.source_files) +
            len(pm.test_files) +
            len(pm.config_files) +
            len(pm.javascript_files) +
            len(pm.web_files) +
            len(pm.data_files) +
            len(pm.doc_files) +
            len(pm.other_files)
        )

    # ============================================================
    # Quick Content Analysis (Peek)
    # ============================================================

    def peek_source_files(self, source_files: List[ScannedFile]) -> Dict[str, FilePeek]:
        """Quick analysis of Python source files"""
        peeks = {}
        for sf in source_files:
            peek = self.peek_file(sf.path)
            if peek:
                peeks[sf.path] = peek
        return peeks

    def peek_file(self, filepath: str) -> Optional[FilePeek]:
        """Quick analysis of a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                return None

            peek = FilePeek(path=filepath)

            # Use AST for accurate analysis
            try:
                tree = ast.parse(content)
                peek.import_count = sum(1 for node in ast.walk(tree)
                                        if isinstance(node, (ast.Import, ast.ImportFrom)))
                peek.class_count = sum(1 for node in ast.walk(tree)
                                       if isinstance(node, ast.ClassDef))
                peek.function_count = sum(1 for node in ast.walk(tree)
                                          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
                peek.has_async = any(isinstance(node, ast.AsyncFunctionDef) for node in ast.walk(tree))
                peek.has_type_hints = any(node.returns is not None for node in ast.walk(tree)
                                          if isinstance(node, ast.FunctionDef))
                peek.docstring = ast.get_docstring(tree) or ""

                # Check for executable pattern
                peek.is_executable = any(
                    isinstance(node, ast.If) and
                    hasattr(node.test, 'left') and
                    hasattr(node.test.left, 'id') and
                    node.test.left.id == '__name__'
                    for node in ast.walk(tree)
                )
            except SyntaxError:
                # Fallback to string matching
                lines = content.split('\n')
                peek.import_count = sum(1 for l in lines if l.strip().startswith(('import ', 'from ')))
                peek.class_count = sum(1 for l in lines if l.strip().startswith('class '))
                peek.function_count = sum(1 for l in lines if l.strip().startswith(('def ', 'async def ')))
                peek.has_async = any('async def ' in l for l in lines)
                peek.has_type_hints = any('->' in l for l in lines)
                peek.is_executable = any('__name__' in l and '__main__' in l for l in lines)

            peek.has_imports = peek.import_count > 0
            peek.has_classes = peek.class_count > 0
            peek.has_functions = peek.function_count > 0

            return peek

        except (IOError, UnicodeDecodeError):
            return None

    # ============================================================
    # Test Gap Detection
    # ============================================================

    def find_test_gaps(self, source_dir: str) -> TestGapReport:
        """Find source files without corresponding test files"""
        pm = self.scan(source_dir, quick_peek=False, find_gaps=False)
        return self.find_test_gaps_from_map(pm)

    def find_test_gaps_from_map(self, pm: ProjectMap) -> TestGapReport:
        """Find test gaps from an existing project map"""
        report = TestGapReport()
        report.total_sources = len(pm.source_files)

        if report.total_sources == 0:
            return report

        # Build sets of base names
        source_names = {}
        for sf in pm.source_files:
            stem = Path(sf.path).stem
            source_names[stem] = sf.path

        tested_names = set()
        for tf in pm.test_files:
            name = Path(tf.path).stem
            for prefix in ['test_', '_test']:
                if name.startswith(prefix):
                    tested_names.add(name[len(prefix):])
                    break
                if name.endswith(prefix):
                    tested_names.add(name[:-len(prefix)])
                    break
            # Also check without prefix (some test files match exactly)
            if name in source_names:
                tested_names.add(name)

        # Find untested
        for stem, path in source_names.items():
            if stem in tested_names:
                report.tested_files.append(path)
            else:
                report.untested_files.append(path)

        report.tested_count = len(report.tested_files)
        report.untested_count = len(report.untested_files)
        report.coverage_pct = round((report.tested_count / report.total_sources) * 100, 1)

        return report

    # ============================================================
    # Project Structure Detection
    # ============================================================

    def _is_python_package(self, path: Path) -> bool:
        """Check if directory is a Python package"""
        return ((path / '__init__.py').exists() or
                (path / 'setup.py').exists() or
                (path / 'pyproject.toml').exists())

    def _has_src_layout(self, path: Path) -> bool:
        """Check if project uses src/ layout"""
        src_path = path / 'src'
        return src_path.exists() and src_path.is_dir()

    def _build_tree(self, path: Path, max_depth: int = 10, current_depth: int = 0) -> Dict:
        """Build a simplified directory tree"""
        if current_depth > max_depth:
            return {'...': 'max depth reached'}

        tree = {}
        try:
            items = sorted(path.iterdir())
        except (OSError, PermissionError):
            return {}

        dirs = []
        py_files = []
        other_files = []

        for item in items:
            if item.name in self.exclude_dirs or item.name.startswith('.'):
                continue
            try:
                if item.is_dir():
                    dirs.append(item)
                elif item.suffix == '.py':
                    py_files.append(item.name)
                else:
                    other_files.append(item.name)
            except (OSError, PermissionError):
                continue

        if py_files:
            tree['py'] = py_files[:15]
        if other_files:
            tree['files'] = other_files[:10]

        for d in dirs:
            subtree = self._build_tree(d, max_depth, current_depth + 1)
            if subtree:
                tree[d.name + '/'] = subtree

        return tree

    # ============================================================
    # Summary
    # ============================================================

    def get_summary(self, pm: ProjectMap) -> str:
        """Generate a text summary of the project map"""
        lines = [
            f"Project: {pm.source_dir}",
            f"  Python source files: {len(pm.source_files)}",
            f"  Test files: {len(pm.test_files)}",
            f"  Config files: {len(pm.config_files)}",
            f"  JavaScript files: {len(pm.javascript_files)}",
            f"  Web files: {len(pm.web_files)}",
            f"  Data files: {len(pm.data_files)}",
            f"  Documentation files: {len(pm.doc_files)}",
            f"  Other files: {len(pm.other_files)}",
            f"  Total: {pm.total_files}",
            f"  Is Python package: {pm.is_python_package}",
            f"  Has src/ layout: {pm.has_src_layout}",
        ]

        if pm.test_gap:
            tg = pm.test_gap
            lines.append(f"  Test coverage: {tg.coverage_pct}% ({tg.tested_count}/{tg.total_sources})")
            if tg.untested_files:
                lines.append(f"  Untested files: {tg.untested_count}")
                for f in tg.untested_files[:5]:
                    lines.append(f"    - {Path(f).name}")

        return '\n'.join(lines)


# ============================================================
# Convenience Functions
# ============================================================

def scan_project(source_dir: str) -> ProjectMap:
    """Quick project scan"""
    scanner = ProjectScanner()
    return scanner.scan(source_dir)


def list_source_files(source_dir: str) -> List[str]:
    """List all Python source files"""
    pm = scan_project(source_dir)
    return [f.path for f in pm.source_files]


def list_test_files(source_dir: str) -> List[str]:
    """List all test files"""
    pm = scan_project(source_dir)
    return [f.path for f in pm.test_files]


def find_untested_files(source_dir: str) -> List[str]:
    """Find source files without tests"""
    pm = scan_project(source_dir)
    return pm.test_gap.untested_files if pm.test_gap else []


# ============================================================
# Self Test
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Eye - Project Scanner v1.1.0 - Self Test")
    print("=" * 60)

    scanner = ProjectScanner()
    pm = scanner.scan(".")

    print(f"\n{scanner.get_summary(pm)}")

    # Show first few source files with peeks
    if pm.source_files:
        print(f"\nFirst 5 source files with analysis:")
        for sf in pm.source_files[:5]:
            peek = pm.file_peeks.get(sf.path)
            if peek:
                print(f"  {sf.name} ({sf.size_kb}KB)")
                print(f"    imports={peek.import_count}, classes={peek.class_count}, "
                      f"functions={peek.function_count}, async={peek.has_async}, "
                      f"hints={peek.has_type_hints}, executable={peek.is_executable}")

    # Show test files
    if pm.test_files:
        print(f"\nTest files found: {len(pm.test_files)}")
        for tf in pm.test_files[:5]:
            print(f"  {Path(tf.path).name}")

    # Show untested files
    if pm.test_gap and pm.test_gap.untested_files:
        print(f"\nUntested source files:")
        for f in pm.test_gap.untested_files[:10]:
            print(f"  {Path(f).name}")

    # Show directory tree (top level only)
    if pm.directory_tree:
        print(f"\nDirectory structure (top level):")
        for key, value in list(pm.directory_tree.items())[:10]:
            if isinstance(value, dict):
                print(f"  {key} ({len(value)} items)")
            else:
                print(f"  {key}: {value}")

    print(f"\nTest complete.")
