"""
Hand - Test Generator v1.1.0
Generates pytest test code from code analysis results.
Produces unit tests, class tests, integration tests, and scenario tests.
"""

import os
import ast
from pathlib import Path
from typing import Optional, List, Dict, Any, Set, Tuple
from datetime import datetime, timezone

# ============================================================
# Smart Value Library
# ============================================================

SMART_VALUES: Dict[str, str] = {
    # File paths and directories
    'filename': '"test_file.py"',
    'filepath': '"/tmp/test_file.py"',
    'path': '"/tmp/test"',
    'directory': '"/tmp"',
    'dir': '"/tmp"',
    'folder': '"/tmp"',
    'file': '"test_file.py"',

    # Names and identifiers
    'name': '"test_name"',
    'key': '"test_key"',
    'id': '"test_id"',
    'user_id': '1',
    'username': '"test_user"',
    'email': '"test@example.com"',
    'token': '"abc123xyz"',
    'secret': '"secret123"',
    'api_key': '"sk-test-123"',
    'password': '"secure_pass_123"',
    'hash': '"abc123def456"',

    # Network
    'url': '"https://example.com"',
    'host': '"localhost"',
    'hostname': '"localhost"',
    'ip': '"127.0.0.1"',
    'domain': '"example.com"',
    'port': '8080',
    'endpoint': '"/api/v1"',
    'uri': '"/api/v1/resource"',

    # Data structures
    'data': '{}',
    'config': '{}',
    'headers': '{"Content-Type": "application/json"}',
    'params': '{}',
    'payload': '{}',
    'body': '{}',
    'metadata': '{}',
    'options': '{}',
    'settings': '{}',
    'messages': '[]',
    'items': '[]',
    'results': '[]',
    'records': '[]',
    'entries': '[]',
    'list': '[]',
    'array': '[]',
    'collection': '[]',

    # Text content
    'text': '"hello world"',
    'content': '"test content"',
    'description': '"test description"',
    'message': '"test message"',
    'error': '"test error message"',
    'title': '"Test Title"',
    'label': '"Test Label"',
    'note': '"test note"',
    'comment': '"test comment"',
    'query': '"test query"',
    'search': '"test search"',

    # Numeric
    'count': '10',
    'size': '100',
    'max': '1000',
    'min': '1',
    'length': '50',
    'limit': '100',
    'offset': '0',
    'total': '100',
    'amount': '99',
    'price': '49',
    'rate': '5',
    'score': '85',
    'index': '0',
    'position': '0',
    'page': '1',
    'pages': '10',

    # Time
    'timeout': '30',
    'delay': '5',
    'interval': '10',
    'duration': '60',
    'ttl': '3600',
    'timestamp': '1234567890',
    'date': '"2026-01-15"',
    'datetime': '"2026-01-15T10:30:00"',

    # Boolean
    'flag': 'True',
    'debug': 'False',
    'active': 'True',
    'enabled': 'True',
    'disabled': 'False',
    'visible': 'True',
    'required': 'True',
    'optional': 'False',
    'force': 'False',
    'verbose': 'False',
    'strict': 'True',
    'safe': 'True',
    'secure': 'True',
    'overwrite': 'False',

    # Types
    'string_val': '"test_string"',
    'int_val': '42',
    'float_val': '3.14',
    'bool_val': 'True',
    'list_val': '[]',
    'dict_val': '{}',
    'none_val': 'None',
    'bytes_val': 'b"test_bytes"',
}

# Edge case values by type
EDGE_VALUES: Dict[str, List[str]] = {
    'str': ['""', '   spaces   ', 'aaaaaaaaaa'],
    'int': ['0', '1', '-1', '10**6', '-10**6'],
    'float': ['0.0', '1.0', '-1.0', '3.14159'],
    'bool': ['True', 'False'],
    'list': ['[]', '[1, 2, 3]'],
    'dict': ['{}', '{"key": "value"}'],
    'Optional': ['None'],
}

# ============================================================
# Import Path Resolver
# ============================================================

def resolve_import_path(filepath: str) -> str:
    """Calculate the Python import path for a source file"""
    full_path = Path(filepath).resolve()
    current_dir = Path.cwd().resolve()

    # Find the module root by looking for indicators
    module_root = None
    for parent in full_path.parents:
        if ((parent / '__init__.py').exists() or
            (parent / 'setup.py').exists() or
            (parent / 'pyproject.toml').exists()):
            module_root = parent.parent
            break

    if module_root is None:
        module_root = current_dir

    try:
        rel_path = full_path.relative_to(module_root)
    except ValueError:
        module_root = current_dir
        try:
            rel_path = full_path.relative_to(module_root)
        except ValueError:
            return Path(filepath).stem

    import_path = str(rel_path.with_suffix('')).replace(os.sep, '.')
    return import_path


# ============================================================
# Smart Argument Value Generator
# ============================================================

class SmartValueGenerator:
    """Generates intelligent default values for function arguments"""

    @classmethod
    def generate(cls, arg_name: str, type_hint: Optional[str] = None) -> str:
        """Generate a smart value for an argument"""
        name_lower = arg_name.lower()

        # Check smart values dictionary
        if name_lower in SMART_VALUES:
            return SMART_VALUES[name_lower]

        # Check partial matches
        for key, value in SMART_VALUES.items():
            if key in name_lower or name_lower in key:
                return value

        # Type-hint based
        if type_hint:
            type_val = cls._value_from_type(type_hint)
            if type_val is not None:
                return type_val

        # Keyword-based inference
        if any(kw in name_lower for kw in ['file', 'path', 'dir', 'folder']):
            return '"/tmp/test_file.py"'
        if any(kw in name_lower for kw in ['url', 'uri', 'endpoint', 'href', 'link']):
            return '"https://example.com"'
        if any(kw in name_lower for kw in ['name', 'key', 'id', 'slug']):
            return '"test_name"'
        if 'email' in name_lower:
            return '"test@example.com"'
        if any(kw in name_lower for kw in ['token', 'secret', 'password', 'hash']):
            return '"abc123xyz"'
        if any(kw in name_lower for kw in ['token', 'secret', 'password']):
            return '"secret123"'
        if any(kw in name_lower for kw in ['host', 'ip', 'domain']):
            return '"localhost"'
        if 'port' in name_lower:
            return '8080'
        if any(kw in name_lower for kw in ['count', 'size', 'max', 'length', 'total', 'limit']):
            return '100'
        if any(kw in name_lower for kw in ['flag', 'debug', 'active', 'enabled', 'visible', 'force']):
            return 'True'
        if any(kw in name_lower for kw in ['list', 'items', 'array', 'collection', 'entries']):
            return '[]'
        if any(kw in name_lower for kw in ['data', 'config', 'dict', 'body', 'payload', 'params',
                                            'headers', 'metadata', 'options', 'settings']):
            return '{}'
        if any(kw in name_lower for kw in ['code', 'source']):
            return '"print(1)"'
        if any(kw in name_lower for kw in ['message', 'text', 'content', 'description',
                                            'title', 'label', 'note']):
            return '"test_text"'
        if any(kw in name_lower for kw in ['timeout', 'delay', 'ttl', 'duration']):
            return '30'
        if any(kw in name_lower for kw in ['timestamp', 'date', 'time']):
            return '1234567890'
        if 'page' in name_lower:
            return '1'

        # Fallback
        return '"test_value"'

    @classmethod
    def _value_from_type(cls, type_hint: str) -> Optional[str]:
        """Generate a value based on type hint"""
        hint = type_hint.strip()

        # Remove Optional wrapper
        if hint.startswith('Optional[') and hint.endswith(']'):
            return 'None'

        # Direct type mapping
        type_map = {
            'str': '"test_string"',
            'int': '42',
            'float': '3.14',
            'bool': 'True',
            'bytes': 'b"test_bytes"',
            'list': '[]',
            'dict': '{}',
            'tuple': '()',
            'set': 'set()',
            'None': 'None',
            'Any': '"test_value"',
        }

        if hint in type_map:
            return type_map[hint]

        # Handle Union[..., None] as Optional
        if hint.startswith('Union[') and 'None' in hint:
            return 'None'

        return None

    @classmethod
    def generate_edge_values(cls, arg_name: str,
                             type_hint: Optional[str] = None) -> List[str]:
        """Generate edge case values for testing"""
        values = []

        if type_hint:
            hint = type_hint.strip()
            if hint.startswith('Optional['):
                values.append('None')
                hint = hint[9:-1].strip()

            if hint in EDGE_VALUES:
                values.extend(EDGE_VALUES[hint])

        # Default edge cases
        if not values:
            name_lower = arg_name.lower()
            if any(kw in name_lower for kw in ['str', 'text', 'name', 'message']):
                values = ['""', 'aaaaaaaaaa']
            elif any(kw in name_lower for kw in ['int', 'count', 'size', 'num']):
                values = ['0', '-1']
            elif any(kw in name_lower for kw in ['list', 'items', 'array']):
                values = ['[]', '[1]']

        return values


# ============================================================
# Test Code Generator
# ============================================================

class TestGenerator:
    """Generates pytest test code from analysis results"""

    def __init__(self, file_analysis, source_dir: str = "."):
        self.analysis = file_analysis
        self.source_dir = source_dir
        self.import_path = resolve_import_path(file_analysis.filepath)
        self.lines: List[str] = []
        self.test_count = 0

    # ============================================================
    # Main Generation
    # ============================================================

    def generate(self) -> str:
        """Generate complete test file content"""
        self.lines = []
        self.test_count = 0

        # Header
        self._generate_header()

        # Imports
        self._generate_imports()

        # Unit tests for standalone functions
        for func in self.analysis.functions:
            self._generate_function_tests(func)

        # Class tests
        for cls in self.analysis.classes:
            self._generate_class_tests(cls)

        # Integration tests
        if self.analysis.relationships:
            self._generate_integration_tests()

        # Scenario tests
        if self.analysis.scenarios:
            self._generate_scenario_tests()

        return '\n'.join(self.lines)

    # ============================================================
    # Header
    # ============================================================

    def _generate_header(self):
        """Generate file header with metadata"""
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        source_name = Path(self.analysis.filepath).name

        self.lines.extend([
            f'"""',
            f'Tests for {source_name}',
            f'',
            f'Generated: {now}',
            f'Functions: {len(self.analysis.functions)}',
            f'Classes: {len(self.analysis.classes)}',
            f'Import: {self.import_path}',
            f'"""',
            '',
        ])

    # ============================================================
    # Imports
    # ============================================================

    def _generate_imports(self):
        """Generate import statements"""
        self.lines.extend([
            'import pytest',
            'import sys',
            'import os',
            'from unittest.mock import Mock, patch, MagicMock, AsyncMock',
            '',
            '# Add project root to path',
            'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))',
            '',
        ])

        # Function imports
        func_names = [f.name for f in self.analysis.functions]
        if func_names:
            names_str = ', '.join(func_names)
            self.lines.append(f'from {self.import_path} import {names_str}')
            self.lines.append('')

        # Class imports
        class_names = [c.name for c in self.analysis.classes]
        if class_names:
            names_str = ', '.join(class_names)
            self.lines.append(f'from {self.import_path} import {names_str}')
            self.lines.append('')

    # ============================================================
    # Function Tests (Unit)
    # ============================================================

    def _generate_function_tests(self, func) -> None:
        """Generate unit tests for a single function"""
        func_name = func.name
        args = getattr(func, 'args', [])
        return_type = getattr(func, 'return_type', None)
        raises = getattr(func, 'raises', [])
        is_async = getattr(func, 'is_async', False)

        # Class wrapper
        class_name = f'Test{func_name.replace("_", " ").title().replace(" ", "")}'
        self.lines.append(f'class {class_name}:')
        self.lines.append(f'    """Tests for {func_name}"""')
        self.lines.append('')

        # Test: exists
        self._add_test_method('test_exists', [
            f'"""Verify {func_name} is callable"""',
            f'assert callable({func_name})',
        ], is_async)
        self.test_count += 1

        # Test: valid input
        if args:
            valid_args = [SmartValueGenerator.generate(a.name, a.type_hint) for a in args]
            args_str = ', '.join(valid_args)

            test_lines = [f'"""Test {func_name} with valid inputs"""']

            if is_async:
                test_lines.append(f'result = await {func_name}({args_str})')
            else:
                test_lines.append(f'result = {func_name}({args_str})')

            if return_type and return_type != 'None':
                test_lines.append('assert result is not None')
            else:
                test_lines.append(f'# {func_name} returns None or no return')
                test_lines.append(f'# Verify no exception raised')

            self._add_test_method('test_valid_input', test_lines, is_async)
            self.test_count += 1

        # Test: return type
        if return_type and return_type not in ('None', 'NoneType'):
            valid_args = [SmartValueGenerator.generate(a.name, a.type_hint) for a in args]
            args_str = ', '.join(valid_args) if valid_args else ''
            test_lines = [
                f'"""Test {func_name} return type is {return_type}"""',
                f'result = {func_name}({args_str})' if not is_async else f'result = await {func_name}({args_str})',
            ]
            python_type = self._type_hint_to_python_type(return_type)
            if python_type:
                test_lines.append(f'assert isinstance(result, {python_type})')
            self._add_test_method('test_return_type', test_lines, is_async)
            self.test_count += 1

        # Test: None return for Optional
        if return_type and 'Optional' in return_type:
            test_lines = [
                f'"""Test {func_name} can return None"""',
                f'# Optional return type allows None',
            ]
            self._add_test_method('test_can_return_none', test_lines, is_async)
            self.test_count += 1

        # Test: exceptions
        for exc in raises:
            test_lines = [
                f'"""Test {func_name} raises {exc}"""',
                f'with pytest.raises({exc}):',
                f'    {func_name}()  # TODO: provide invalid input to trigger {exc}',
            ]
            self._add_test_method(f'test_raises_{exc.lower()}', test_lines, is_async)
            self.test_count += 1

        # Test: edge cases
        for i, arg in enumerate(args):
            edge_values = SmartValueGenerator.generate_edge_values(arg.name, arg.type_hint)
            for j, edge_val in enumerate(edge_values):
                edge_args = []
                for k, a in enumerate(args):
                    if k == i:
                        edge_args.append(edge_val)
                    else:
                        edge_args.append(SmartValueGenerator.generate(a.name, a.type_hint))

                args_str = ', '.join(edge_args)
                test_lines = [
                    f'"""Test {func_name} with edge value for {arg.name}: {edge_val}"""',
                    f'result = {func_name}({args_str})' if not is_async else f'result = await {func_name}({args_str})',
                ]
                self._add_test_method(f'test_edge_{arg.name}_{j}', test_lines, is_async)
                self.test_count += 1
                if self.test_count >= 50:  # Safety limit
                    break

        self.lines.append('')

    # ============================================================
    # Class Tests
    # ============================================================

    def _generate_class_tests(self, cls) -> None:
        """Generate tests for a class"""
        class_name = cls.name
        methods = getattr(cls, 'methods', [])

        # Class test wrapper
        test_class_name = f'Test{class_name}'
        self.lines.append(f'class {test_class_name}:')
        self.lines.append(f'    """Tests for {class_name}"""')
        self.lines.append('')

        # Test: create default
        self._add_test_method('test_create_default', [
            f'"""Verify {class_name} can be instantiated"""',
            f'obj = {class_name}()',
            f'assert obj is not None',
            f'assert isinstance(obj, {class_name})',
        ])
        self.test_count += 1

        # Test: create with args (if __init__ has parameters)
        init_method = next((m for m in methods if m.name == '__init__'), None)
        if init_method and hasattr(init_method, 'args') and init_method.args:
            init_args = [a for a in init_method.args if a.name != 'self']
            if init_args:
                valid_args = [SmartValueGenerator.generate(a.name, a.type_hint) for a in init_args]
                args_str = ', '.join(valid_args)
                self._add_test_method('test_create_with_args', [
                    f'"""Verify {class_name} can be instantiated with arguments"""',
                    f'obj = {class_name}({args_str})',
                    f'assert obj is not None',
                ])
                self.test_count += 1

        # Test: each public method
        for method in methods:
            if method.name.startswith('__') and method.name != '__init__':
                continue

            method_name = method.name
            method_args = getattr(method, 'args', [])
            is_async = getattr(method, 'is_async', False)

            # Test: method exists
            self._add_test_method(f'test_{method_name}_exists', [
                f'"""Verify {class_name}.{method_name} exists"""',
                f'obj = {class_name}()',
                f'assert hasattr(obj, "{method_name}")',
                f'assert callable(obj.{method_name})',
            ])
            self.test_count += 1

            # Test: method valid
            if method_args:
                actual_args = [a for a in method_args if a.name != 'self']
                if actual_args:
                    valid_args = [SmartValueGenerator.generate(a.name, a.type_hint) for a in actual_args]
                    args_str = ', '.join(valid_args)

                    test_lines = [
                        f'"""Test {class_name}.{method_name} with valid inputs"""',
                        f'obj = {class_name}()',
                    ]
                    if is_async:
                        test_lines.append(f'result = await obj.{method_name}({args_str})')
                    else:
                        test_lines.append(f'result = obj.{method_name}({args_str})')
                    test_lines.append('assert result is not None')

                    self._add_test_method(f'test_{method_name}_valid', test_lines, is_async)
                    self.test_count += 1

        self.lines.append('')

    # ============================================================
    # Integration Tests
    # ============================================================

    def _generate_integration_tests(self) -> None:
        """Generate integration tests for related function pairs"""
        if not self.analysis.relationships:
            return

        self.lines.append('# ============================================================')
        self.lines.append('# Integration Tests')
        self.lines.append('# ============================================================')
        self.lines.append('')

        for rel in self.analysis.relationships[:5]:  # Limit to 5
            caller = rel.get('caller', '')
            callee = rel.get('callee', '')

            self.lines.append(f'class Test{caller}_{callee}_Integration:')
            self.lines.append(f'    """Integration tests: {caller} → {callee}"""')
            self.lines.append('')

            # Test: caller calls callee
            self._add_test_method(f'test_{caller}_calls_{callee}', [
                f'"""Verify {caller} calls {callee}"""',
                f'with patch("{self.import_path}.{callee}") as mock_{callee}:',
                f'    mock_{callee}.return_value = None',
                f'    {caller}({self._get_mock_args(caller)})',
                f'    mock_{callee}.assert_called()',
            ])
            self.test_count += 1

            # Test: full flow with mock
            self._add_test_method(f'test_{caller}_{callee}_flow', [
                f'"""Test full flow: {caller} with mocked {callee}"""',
                f'with patch("{self.import_path}.{callee}") as mock_{callee}:',
                f'    mock_{callee}.return_value = "mocked_result"',
                f'    result = {caller}({self._get_mock_args(caller)})',
                f'    assert result is not None',
            ])
            self.test_count += 1

            self.lines.append('')

    # ============================================================
    # Scenario Tests
    # ============================================================

    def _generate_scenario_tests(self) -> None:
        """Generate scenario tests for function chains"""
        if not self.analysis.scenarios:
            return

        self.lines.append('# ============================================================')
        self.lines.append('# Scenario Tests')
        self.lines.append('# ============================================================')
        self.lines.append('')

        for i, scenario in enumerate(self.analysis.scenarios[:3]):  # Limit to 3
            scenario_name = '_'.join(scenario[:3])
            self.lines.append(f'class TestScenario_{scenario_name}:')
            self.lines.append(f'    """Scenario: {" → ".join(scenario)}"""')
            self.lines.append('')

            test_lines = [
                f'"""Full scenario: {" → ".join(scenario)}"""',
                '# Step through the complete flow',
            ]

            for func_name in scenario:
                func = self._find_function(func_name)
                if func and hasattr(func, 'args') and func.args:
                    args = [SmartValueGenerator.generate(a.name, a.type_hint) for a in func.args]
                    args_str = ', '.join(args)
                    test_lines.append(f'result_{func_name} = {func_name}({args_str})')
                    test_lines.append(f'assert result_{func_name} is not None')
                else:
                    test_lines.append(f'# {func_name}() - called in scenario')
                    test_lines.append(f'{func_name}()')

            self._add_test_method('test_full_scenario', test_lines)
            self.test_count += 1
            self.lines.append('')

    # ============================================================
    # Helpers
    # ============================================================

    def _add_test_method(self, name: str, body_lines: List[str],
                         is_async: bool = False) -> None:
        """Add a test method with proper formatting"""
        self.lines.append(f'    def {name}(self):')

        for i, line in enumerate(body_lines):
            if i == 0:
                self.lines.append(f'        {line}')
            else:
                self.lines.append(f'        {line}')

        self.lines.append('')

    def _find_function(self, name: str):
        """Find a function in the analysis by name"""
        for func in self.analysis.functions:
            if func.name == name:
                return func

        for cls in self.analysis.classes:
            for method in getattr(cls, 'methods', []):
                if method.name == name:
                    return method

        return None

    def _get_mock_args(self, func_name: str) -> str:
        """Get mock arguments for a function"""
        func = self._find_function(func_name)
        if func and hasattr(func, 'args') and func.args:
            return ', '.join(
                SmartValueGenerator.generate(a.name, a.type_hint)
                for a in func.args
            )
        return ''

    @staticmethod
    def _type_hint_to_python_type(type_hint: str) -> Optional[str]:
        """Convert a type hint string to a Python type for isinstance check"""
        mapping = {
            'str': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'bytes': 'bytes',
            'list': 'list',
            'dict': 'dict',
            'tuple': 'tuple',
            'set': 'set',
        }
        hint = type_hint.strip()
        if hint.startswith('Optional['):
            hint = hint[9:-1].strip()
        return mapping.get(hint)

    def get_test_count(self) -> int:
        """Return the number of generated tests"""
        return self.test_count


# ============================================================
# File Writer
# ============================================================

class TestFileWriter:
    """Writes generated test code to files"""

    @staticmethod
    def write_test_file(content: str, source_filepath: str,
                        test_dir: str = "tests") -> str:
        """Write test content to the appropriate test file"""
        # Calculate test file path
        source_path = Path(source_filepath).resolve()
        source_stem = source_path.stem

        # Find the project root and calculate relative path
        project_root = TestFileWriter._find_project_root(source_path)
        try:
            rel_path = source_path.relative_to(project_root)
        except ValueError:
            rel_path = Path(source_path.name)

        test_filename = f"test_{source_stem}.py"
        test_path = Path(test_dir) / rel_path.parent / test_filename

        # Create directory if needed
        test_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(test_path)

    @staticmethod
    def _find_project_root(source_path: Path) -> Path:
        """Find the project root directory"""
        current = source_path.parent
        while current != current.parent:
            if ((current / 'setup.py').exists() or
                (current / 'pyproject.toml').exists() or
                (current / '__init__.py').exists()):
                return current
            current = current.parent
        return source_path.parent

    @staticmethod
    def update_existing_test_file(existing_path: str, new_tests: Dict[str, str]) -> bool:
        """Add missing tests to an existing test file"""
        try:
            with open(existing_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find existing test methods
            existing_tests = set()
            for line in content.split('\n'):
                if line.strip().startswith('def test_'):
                    test_name = line.strip().split('(')[0].replace('def ', '')
                    existing_tests.add(test_name)

            # Add missing tests at the end
            added = 0
            for test_name, test_code in new_tests.items():
                if test_name not in existing_tests:
                    content += f'\n    {test_code}\n'
                    added += 1

            if added > 0:
                with open(existing_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

            return False

        except (IOError, UnicodeDecodeError):
            return False


# ============================================================
# Convenience Functions
# ============================================================

def generate_tests(analysis,
                   source_dir: str = ".",
                   test_dir: str = "tests",
                   write: bool = True) -> Tuple[str, str, int]:
    """Generate tests from analysis and optionally write to file"""
    generator = TestGenerator(analysis, source_dir)
    content = generator.generate()

    filepath = ""
    if write:
        writer = TestFileWriter()
        filepath = writer.write_test_file(content, analysis.filepath, test_dir)

    return content, filepath, generator.get_test_count()


# ============================================================
# Self Test
# ============================================================

if __name__ == "__main__":
    import tempfile
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("=" * 60)
    print("Test Generator - Self Test")
    print("=" * 60)

    # Create mock analysis
    from dataclasses import dataclass

    @dataclass
    class MockArg:
        name: str
        type_hint: Optional[str] = None

    @dataclass
    class MockFunc:
        name: str
        args: List[MockArg] = None
        return_type: Optional[str] = None
        raises: List[str] = None
        is_async: bool = False

        def __post_init__(self):
            if self.args is None:
                self.args = []
            if self.raises is None:
                self.raises = []

    @dataclass
    class MockClass:
        name: str
        methods: List[MockFunc] = None

        def __post_init__(self):
            if self.methods is None:
                self.methods = []

    @dataclass
    class MockAnalysis:
        filepath: str
        functions: List[MockFunc] = None
        classes: List[MockClass] = None
        relationships: List[Dict] = None
        scenarios: List[List[str]] = None

        def __post_init__(self):
            if self.functions is None:
                self.functions = []
            if self.classes is None:
                self.classes = []
            if self.relationships is None:
                self.relationships = []
            if self.scenarios is None:
                self.scenarios = []

    # Build mock analysis
    mock = MockAnalysis(
        filepath="src/auth_service.py",
        functions=[
            MockFunc(
                name="hash_password",
                args=[MockArg("password", "str")],
                return_type="str",
                raises=["ValueError"],
            ),
            MockFunc(
                name="authenticate",
                args=[MockArg("username", "str"), MockArg("password", "str")],
                return_type="Optional[dict]",
                raises=["ValueError"],
            ),
        ],
        classes=[
            MockClass(
                name="UserService",
                methods=[
                    MockFunc("__init__", [MockArg("self"), MockArg("db_url", "str")]),
                    MockFunc("create_user", [MockArg("self"), MockArg("name", "str"), MockArg("email", "str")]),
                ],
            ),
        ],
        relationships=[
            {"caller": "authenticate", "callee": "hash_password"},
        ],
        scenarios=[
            ["hash_password", "authenticate"],
        ],
    )

    # Generate tests
    generator = TestGenerator(mock, ".")
    code = generator.generate()

    print(f"\nGenerated {generator.get_test_count()} tests")
    print(f"\nGenerated code preview (first 80 lines):")
    print("-" * 60)
    for line in code.split('\n')[:80]:
        print(line)
    if len(code.split('\n')) > 80:
        print(f"... ({len(code.split('n'))} total lines)")

    # Test smart value generator
    print("\n" + "=" * 60)
    print("Smart Value Generator Test")
    print("-" * 60)
    test_cases = [
        ("filename", None),
        ("port", None),
        ("username", "str"),
        ("count", "int"),
        ("data", "dict"),
        ("active", "bool"),
        ("url", None),
    ]
    for name, hint in test_cases:
        value = SmartValueGenerator.generate(name, hint)
        print(f"  {name}:{hint or '?'} → {value}")

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name

    # Validate syntax
    try:
        with open(temp_path, 'r') as f:
            ast.parse(f.read())
        print(f"\nSyntax check: PASSED")
    except SyntaxError as e:
        print(f"\nSyntax check: FAILED - {e}")
    finally:
        os.unlink(temp_path)

    print("\nSelf test complete.")
