"""
Brain - Deep Code Analyzer v1.1.0
AST-based analysis of Python and JavaScript files.
Extracts functions, classes, types, exceptions, relationships, and scenarios.
"""

import ast
import re
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field

# ============================================================
# Constants
# ============================================================

BUILTIN_TYPES = {'str', 'int', 'float', 'bool', 'bytes', 'list', 'dict',
                 'tuple', 'set', 'None', 'Optional', 'Union', 'Any'}

TYPE_MAP = {
    'str': 'string_val', 'int': 42, 'float': 3.14, 'bool': True,
    'bytes': 'bytes_val', 'list': [], 'dict': {}, 'tuple': (),
    'set': set(), 'None': None,
}

# JavaScript regex patterns
JS_FUNCTION_RE = re.compile(
    r'(?:function\s+(\w+)\s*\(([^)]*)\)|'
    r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>|'
    r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function\s*\(([^)]*)\))'
)
JS_CLASS_RE = re.compile(r'class\s+(\w+)(?:\s+extends\s+(\w+))?')
JS_METHOD_RE = re.compile(r'(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*\{')

# ============================================================
# Data Structures
# ============================================================

@dataclass
class ArgInfo:
    """Function argument information"""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None
    inferred_type: Optional[str] = None


@dataclass
class FunctionInfo:
    """Analyzed function information"""
    name: str
    args: List[ArgInfo] = field(default_factory=list)
    return_type: Optional[str] = None
    raises: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    is_async: bool = False
    is_method: bool = False
    complexity: int = 1
    line_count: int = 0
    docstring: str = ""
    source: str = ""


@dataclass
class ClassInfo:
    """Analyzed class information"""
    name: str
    bases: List[str] = field(default_factory=list)
    methods: List[FunctionInfo] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    docstring: str = ""


@dataclass
class FileAnalysis:
    """Complete file analysis result"""
    filepath: str
    language: str = "python"
    functions: List[FunctionInfo] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    relationships: List[Dict] = field(default_factory=list)
    scenarios: List[List[str]] = field(default_factory=list)
    docstring: str = ""
    total_lines: int = 0


# ============================================================
# Python Analyzer
# ============================================================

class PythonAnalyzer:
    """Deep analysis of Python source code using AST"""

    def analyze_file(self, filepath: str) -> Optional[FileAnalysis]:
        """Analyze a Python file completely"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source)
            analysis = FileAnalysis(filepath=filepath, language="python")
            analysis.total_lines = len(source.split('\n'))
            analysis.docstring = ast.get_docstring(tree) or ""

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):
                        func = self._analyze_function(node, source, is_method=False)
                        analysis.functions.append(func)
                elif isinstance(node, ast.AsyncFunctionDef):
                    if not node.name.startswith('_'):
                        func = self._analyze_async_function(node, source, is_method=False)
                        analysis.functions.append(func)
                elif isinstance(node, ast.ClassDef):
                    cls = self._analyze_class(node, source)
                    analysis.classes.append(cls)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    analysis.imports.extend(self._extract_imports(node))

            # Post-analysis: discover relationships and scenarios
            analysis.relationships = self._discover_relationships(analysis)
            analysis.scenarios = self._discover_scenarios(analysis)

            return analysis

        except (SyntaxError, IOError, UnicodeDecodeError):
            return None

    def _analyze_function(self, node: ast.FunctionDef, source: str,
                          is_method: bool = False) -> FunctionInfo:
        """Analyze a single function"""
        func = FunctionInfo(
            name=node.name,
            is_async=False,
            is_method=is_method,
            docstring=ast.get_docstring(node) or "",
            line_count=node.end_lineno - node.lineno + 1 if node.end_lineno else 0,
            source=ast.get_source_segment(source, node) if hasattr(ast, 'get_source_segment') else "",
        )

        # Arguments
        func.args = self._extract_args(node)

        # Return type
        if node.returns:
            func.return_type = self._extract_type_annotation(node.returns)

        # Decorators
        func.decorators = [self._extract_decorator_name(d) for d in node.decorator_list]

        # Exceptions raised
        func.raises = self._extract_raises(node)

        # Function calls
        func.calls = self._extract_calls(node)

        # Complexity
        func.complexity = self._calculate_complexity(node)

        return func

    def _analyze_async_function(self, node: ast.AsyncFunctionDef, source: str,
                                is_method: bool = False) -> FunctionInfo:
        """Analyze an async function"""
        func = self._analyze_function(node, source, is_method)  # type: ignore
        func.is_async = True
        return func

    def _analyze_class(self, node: ast.ClassDef, source: str) -> ClassInfo:
        """Analyze a class"""
        cls = ClassInfo(
            name=node.name,
            docstring=ast.get_docstring(node) or "",
            bases=[self._extract_type_annotation(b) for b in node.bases],
            decorators=[self._extract_decorator_name(d) for d in node.decorator_list],
        )

        for child in node.body:
            if isinstance(child, ast.FunctionDef) and not child.name.startswith('_'):
                method = self._analyze_function(child, source, is_method=True)
                cls.methods.append(method)
            elif isinstance(child, ast.AsyncFunctionDef) and not child.name.startswith('_'):
                method = self._analyze_async_function(child, source, is_method=True)
                cls.methods.append(method)

        # Properties
        cls.properties = [
            child.attr for child in node.body
            if isinstance(child, ast.Assign) and
            any(isinstance(t, ast.Name) and t.id == child.targets[0].attr
                for t in child.targets if hasattr(child.targets[0], 'attr'))
        ]

        return cls

    # ============================================================
    # Argument Extraction
    # ============================================================

    def _extract_args(self, node: ast.FunctionDef) -> List[ArgInfo]:
        """Extract function arguments with type info"""
        args = []

        for arg in node.args.args:
            arg_info = ArgInfo(name=arg.arg)

            # Type hint
            if arg.annotation:
                arg_info.type_hint = self._extract_type_annotation(arg.annotation)

            # Infer type from usage
            arg_info.inferred_type = self._infer_type_from_body(node, arg.arg)

            args.append(arg_info)

        # Default values
        defaults = node.args.defaults
        offset = len(args) - len(defaults)
        for i, default in enumerate(defaults):
            idx = offset + i
            if idx < len(args):
                args[idx].default_value = self._extract_default_value(default)

        return args

    def _extract_type_annotation(self, node) -> str:
        """Extract type annotation as string"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Subscript):
            base = self._extract_type_annotation(node.value)
            slice_val = self._extract_type_annotation(node.slice)
            return f"{base}[{slice_val}]"
        elif isinstance(node, ast.Tuple):
            return ', '.join(self._extract_type_annotation(e) for e in node.elts)
        elif isinstance(node, ast.Attribute):
            return f"{node.value.id}.{node.attr}" if hasattr(node.value, 'id') else node.attr
        return "Any"

    def _extract_default_value(self, node) -> str:
        """Extract default value as string"""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.List):
            return '[]'
        elif isinstance(node, ast.Dict):
            return '{}'
        elif isinstance(node, ast.Call):
            return f"{self._extract_default_value(node.func)}()"
        return "..."

    def _extract_decorator_name(self, node) -> str:
        """Extract decorator name"""
        if isinstance(node, ast.Name):
            return f"@{node.id}"
        elif isinstance(node, ast.Attribute):
            return f"@{node.attr}"
        elif isinstance(node, ast.Call):
            return self._extract_decorator_name(node.func)
        return "@unknown"

    # ============================================================
    # Exception and Call Extraction
    # ============================================================

    def _extract_raises(self, node: ast.FunctionDef) -> List[str]:
        """Extract exceptions raised in function body"""
        raises = set()

        class RaiseVisitor(ast.NodeVisitor):
            def visit_Raise(self, raise_node):
                if raise_node.exc:
                    if isinstance(raise_node.exc, ast.Call):
                        if hasattr(raise_node.exc.func, 'id'):
                            raises.add(raise_node.exc.func.id)
                        elif hasattr(raise_node.exc.func, 'attr'):
                            raises.add(raise_node.exc.func.attr)
                    elif isinstance(raise_node.exc, ast.Name):
                        raises.add(raise_node.exc.id)
                self.generic_visit(raise_node)

        RaiseVisitor().visit(node)
        return sorted(raises)

    def _extract_calls(self, node: ast.FunctionDef) -> List[str]:
        """Extract function calls made within the function"""
        calls = set()

        class CallVisitor(ast.NodeVisitor):
            def visit_Call(self, call_node):
                if isinstance(call_node.func, ast.Name):
                    calls.add(call_node.func.id)
                elif isinstance(call_node.func, ast.Attribute):
                    calls.add(call_node.func.attr)
                self.generic_visit(call_node)

        CallVisitor().visit(node)
        return sorted(calls)

    # ============================================================
    # Type Inference
    # ============================================================

    def _infer_type_from_body(self, node: ast.FunctionDef, arg_name: str) -> Optional[str]:
        """Infer argument type from usage in function body"""
        for child in ast.walk(node):
            # Binary operations: arg + something → numeric
            if isinstance(child, ast.BinOp) and isinstance(child.left, ast.Name):
                if child.left.id == arg_name:
                    if isinstance(child.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                        return 'int'

            # Comparisons: arg > something → numeric
            if isinstance(child, ast.Compare) and isinstance(child.left, ast.Name):
                if child.left.id == arg_name:
                    return 'int'

            # Method calls: arg.method() → look at method
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                if (isinstance(child.func.value, ast.Name) and
                        child.func.value.id == arg_name):
                    method = child.func.attr
                    if method in ('upper', 'lower', 'strip', 'split', 'replace', 'format'):
                        return 'str'
                    elif method in ('append', 'extend', 'pop', 'remove'):
                        return 'list'
                    elif method in ('keys', 'values', 'items', 'get', 'update'):
                        return 'dict'

            # Subscript: arg[...] → dict or list
            if isinstance(child, ast.Subscript) and isinstance(child.value, ast.Name):
                if child.value.id == arg_name:
                    if isinstance(child.slice, ast.Index):
                        return 'list'
                    return 'dict'

        return None

    # ============================================================
    # Complexity
    # ============================================================

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity (McCabe)"""
        complexity = 1

        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.count = 0

            def visit_If(self, n):
                self.count += 1
                self.generic_visit(n)

            def visit_While(self, n):
                self.count += 1
                self.generic_visit(n)

            def visit_For(self, n):
                self.count += 1
                self.generic_visit(n)

            def visit_ExceptHandler(self, n):
                self.count += 1
                self.generic_visit(n)

            def visit_BoolOp(self, n):
                self.count += len(n.values) - 1
                self.generic_visit(n)

        visitor = ComplexityVisitor()
        visitor.visit(node)
        return complexity + visitor.count

    # ============================================================
    # Import Extraction
    # ============================================================

    def _extract_imports(self, node) -> List[str]:
        """Extract import statements"""
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            names = ', '.join(a.name for a in node.names)
            imports.append(f"from {module} import {names}")
        return imports

    # ============================================================
    # Relationships
    # ============================================================

    def _discover_relationships(self, analysis: FileAnalysis) -> List[Dict]:
        """Discover relationships between functions"""
        relationships = []
        all_functions = {f.name: f for f in analysis.functions}
        call_graph = {f.name: set(f.calls) for f in analysis.functions}

        for func_name, calls in call_graph.items():
            for called in calls:
                if called in all_functions:
                    relationships.append({
                        'type': 'calls',
                        'caller': func_name,
                        'callee': called,
                    })

        return relationships

    # ============================================================
    # Scenario Discovery
    # ============================================================

    def _discover_scenarios(self, analysis: FileAnalysis) -> List[List[str]]:
        """Discover function call chains (scenarios)"""
        scenarios = []
        all_functions = {f.name: f for f in analysis.functions}
        call_graph = {f.name: f.calls for f in analysis.functions}
        visited_global = set()

        def build_chain(start: str, chain: List[str], visited_local: set) -> Optional[List[str]]:
            if start in visited_local:
                return chain if len(chain) >= 3 else None
            visited_local.add(start)
            visited_global.add(start)

            calls = call_graph.get(start, [])
            for called in calls:
                if called in all_functions:
                    result = build_chain(called, chain + [called], visited_local.copy())
                    if result and len(result) >= 3:
                        return result
            return chain if len(chain) >= 3 else None

        for func_name in all_functions:
            if func_name not in visited_global:
                chain = build_chain(func_name, [func_name], set())
                if chain and len(chain) >= 3:
                    scenarios.append(chain)

        return scenarios


# ============================================================
# JavaScript Analyzer
# ============================================================

class JavaScriptAnalyzer:
    """Basic JavaScript analysis using regex patterns"""

    def analyze_file(self, filepath: str) -> Optional[FileAnalysis]:
        """Analyze a JavaScript file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            analysis = FileAnalysis(filepath=filepath, language="javascript")
            analysis.total_lines = len(source.split('\n'))

            # Find functions
            for match in JS_FUNCTION_RE.finditer(source):
                name = match.group(1) or match.group(3) or match.group(5)
                params_str = match.group(2) or match.group(4) or match.group(6)
                if name and not name.startswith('_'):
                    params = [p.strip().split('=')[0].strip() for p in (params_str or '').split(',') if p.strip()]
                    func = FunctionInfo(
                        name=name,
                        args=[ArgInfo(name=p) for p in params],
                    )
                    analysis.functions.append(func)

            # Find classes
            for match in JS_CLASS_RE.finditer(source):
                cls_name = match.group(1)
                bases = [match.group(2)] if match.group(2) else []
                cls = ClassInfo(name=cls_name, bases=bases)
                analysis.classes.append(cls)

            return analysis

        except (IOError, UnicodeDecodeError):
            return None


# ============================================================
# Main Analyzer (delegates to Python or JS)
# ============================================================

class DeepAnalyzer:
    """Main analyzer that delegates to language-specific analyzers"""

    def __init__(self):
        self.python_analyzer = PythonAnalyzer()
        self.js_analyzer = JavaScriptAnalyzer()

    def analyze_file(self, filepath: str) -> Optional[FileAnalysis]:
        """Analyze any supported file"""
        ext = Path(filepath).suffix.lower()

        if ext == '.py':
            return self.python_analyzer.analyze_file(filepath)
        elif ext in ('.js', '.jsx', '.ts', '.tsx'):
            return self.js_analyzer.analyze_file(filepath)
        return None

    def analyze_directory(self, directory: str,
                          recursive: bool = True) -> List[FileAnalysis]:
        """Analyze all Python files in a directory"""
        results = []
        path = Path(directory)

        pattern = '**/*.py' if recursive else '*.py'
        for filepath in path.glob(pattern):
            if 'test_' not in filepath.name and not filepath.name.startswith('_'):
                analysis = self.analyze_file(str(filepath))
                if analysis:
                    results.append(analysis)

        return results


# ============================================================
# Convenience Functions
# ============================================================

def analyze_file(filepath: str) -> Optional[FileAnalysis]:
    """Quick single file analysis"""
    analyzer = DeepAnalyzer()
    return analyzer.analyze_file(filepath)


def analyze_directory(directory: str, recursive: bool = True) -> List[FileAnalysis]:
    """Quick directory analysis"""
    analyzer = DeepAnalyzer()
    return analyzer.analyze_directory(directory, recursive)


def get_analysis_summary(analysis: FileAnalysis) -> Dict[str, Any]:
    """Generate a summary dict from a FileAnalysis"""
    return {
        'filepath': analysis.filepath,
        'language': analysis.language,
        'functions_count': len(analysis.functions),
        'classes_count': len(analysis.classes),
        'imports_count': len(analysis.imports),
        'relationships_count': len(analysis.relationships),
        'scenarios_count': len(analysis.scenarios),
        'total_lines': analysis.total_lines,
        'function_names': [f.name for f in analysis.functions],
        'class_names': [c.name for c in analysis.classes],
        'scenarios': analysis.scenarios,
    }


# ============================================================
# Self Test
# ============================================================

if __name__ == "__main__":
    import tempfile

    print("=" * 60)
    print("Brain - Deep Code Analyzer v1.1.0 - Self Test")
    print("=" * 60)

    # Sample Python code
    sample_code = '''
"""Sample module for testing"""

import os
from typing import Optional, List

def greet(name: str, greeting: str = "Hello") -> str:
    """Greet a user by name"""
    if not name:
        raise ValueError("Name cannot be empty")
    result = f"{greeting}, {name}!"
    print(result)
    return result

def process_items(items: List[str], max_count: int = 100) -> int:
    """Process a list of items"""
    count = 0
    for item in items:
        if count >= max_count:
            break
        count += 1
        if not item:
            raise TypeError("Item cannot be None")
    return count

def register_user(username: str, password: str) -> Optional[dict]:
    """Register a new user"""
    if not username or not password:
        raise ValueError("Missing credentials")
    hashed = hash_password(password)
    user = save_user(username, hashed)
    return user

def hash_password(password: str) -> str:
    """Hash a password"""
    return f"hashed_{password}"

def save_user(username: str, password_hash: str) -> dict:
    """Save user to database"""
    return {"username": username, "hash": password_hash}

class UserService:
    """Service for user management"""

    def __init__(self, db_url: str):
        self.db_url = db_url

    def create_user(self, name: str, email: str) -> dict:
        """Create a new user"""
        if "@" not in email:
            raise ValueError("Invalid email")
        return {"id": 1, "name": name, "email": email}

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        if user_id <= 0:
            return False
        return True
'''

    # Write sample to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(sample_code)
        temp_path = f.name

    try:
        analyzer = DeepAnalyzer()
        analysis = analyzer.analyze_file(temp_path)

        if analysis:
            print(f"\nFile: {analysis.filepath}")
            print(f"Language: {analysis.language}")
            print(f"Lines: {analysis.total_lines}")
            print(f"Docstring: {analysis.docstring[:50]}...")

            print(f"\nFunctions ({len(analysis.functions)}):")
            for func in analysis.functions:
                args_str = ', '.join(
                    f"{a.name}:{a.type_hint or a.inferred_type or '?'}"
                    for a in func.args
                )
                print(f"  {func.name}({args_str})")
                print(f"    Returns: {func.return_type or 'None'}")
                print(f"    Raises: {func.raises}")
                print(f"    Calls: {func.calls}")
                print(f"    Complexity: {func.complexity}")

            print(f"\nClasses ({len(analysis.classes)}):")
            for cls in analysis.classes:
                print(f"  {cls.name}")
                for method in cls.methods:
                    print(f"    {method.name}() - complexity={method.complexity}")

            print(f"\nRelationships ({len(analysis.relationships)}):")
            for rel in analysis.relationships:
                print(f"  {rel['caller']} → {rel['callee']}")

            print(f"\nScenarios ({len(analysis.scenarios)}):")
            for i, scenario in enumerate(analysis.scenarios, 1):
                print(f"  Scenario {i}: {' → '.join(scenario)}")

            print(f"\nImports ({len(analysis.imports)}):")
            for imp in analysis.imports:
                print(f"  {imp}")

            # Summary
            summary = get_analysis_summary(analysis)
            print(f"\nSummary: {summary['functions_count']} functions, "
                  f"{summary['classes_count']} classes, "
                  f"{summary['scenarios_count']} scenarios")

        else:
            print("ERROR: Analysis returned None")

    finally:
        os.unlink(temp_path)

    # Test JavaScript
    js_code = '''
function greet(name) {
    return "Hello " + name;
}

class Calculator {
    add(a, b) {
        return a + b;
    }

    subtract(a, b) {
        return a - b;
    }
}
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        js_path = f.name

    try:
        js_analysis = analyzer.analyze_file(js_path)
        if js_analysis:
            print(f"\nJavaScript Analysis:")
            print(f"  Functions: {[f.name for f in js_analysis.functions]}")
            print(f"  Classes: {[c.name for c in js_analysis.classes]}")
    finally:
        os.unlink(js_path)

    print("\nSelf test complete.")
