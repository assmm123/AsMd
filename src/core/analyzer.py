"""
محلل الأكواد المتقدم
يدعم Python, JavaScript, TypeScript, HTML, CSS, JSON
يستخرج الهيكل والإحصائيات والتعقيد
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import Counter
import json

# ============================================================
# إعدادات
# ============================================================

SUPPORTED_LANGUAGES = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.jsx': 'React JSX',
    '.ts': 'TypeScript',
    '.tsx': 'React TSX',
    '.html': 'HTML',
    '.css': 'CSS',
    '.json': 'JSON',
    '.md': 'Markdown',
    '.txt': 'Text',
}

# ============================================================
# محلل Python
# ============================================================

class PythonAnalyzer:
    """محلل متخصص لملفات Python"""
    
    def __init__(self, source: str):
        self.source = source
        self.tree = None
        try:
            self.tree = ast.parse(source)
        except SyntaxError:
            pass
    
    def analyze(self) -> dict:
        """تحليل كامل"""
        if not self.tree:
            return {"error": "خطأ في صيغة Python"}
        
        return {
            "language": "Python",
            "imports": self._get_imports(),
            "functions": self._get_functions(),
            "classes": self._get_classes(),
            "variables": self._get_variables(),
            "decorators": self._get_decorators(),
            "complexity": self._get_complexity(),
        }
    
    def _get_imports(self) -> list:
        """استخراج المكتبات المستوردة"""
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "alias": alias.asname})
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append({"module": f"{module}.{alias.name}", "alias": alias.asname})
        return imports
    


    def _has_return(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
        return False
    
    def _find_raises(self, node):
        raises = []
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                if isinstance(child.exc, ast.Call):
                    if hasattr(child.exc.func, 'id'):
                        raises.append(child.exc.func.id)
        return list(set(raises))

    def _get_function_info(self, node):
        """استخراج معلومات دالة واحدة"""
        func_info = {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'defaults': len(node.args.defaults),
            'has_return': self._has_return(node),
            'raises': self._find_raises(node),
            'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)],
            'lineno': node.lineno
        }
        if isinstance(node, ast.AsyncFunctionDef):
            func_info['async'] = True
        return func_info

    def _get_functions(self) -> list:
        """استخراج الدوال"""
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                func = {
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "defaults_count": len(node.args.defaults),
                    "has_return": any(isinstance(n, ast.Return) and n.value for n in ast.walk(node)),
                    "decorators": [self._get_decorator_name(d) for d in node.decorator_list],
                    "docstring": ast.get_docstring(node),
                    "async": False,
                }
                functions.append(func)
            elif isinstance(node, ast.AsyncFunctionDef):
                func = self._get_function_info(node)
                func["async"] = True
                functions.append(func)
        return functions
    
    def _get_classes(self) -> list:
        """استخراج الكلاسات"""
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                cls = {
                    "name": node.name,
                    "lineno": node.lineno,
                    "bases": [self._get_base_name(b) for b in node.bases],
                    "methods": [],
                    "docstring": ast.get_docstring(node),
                }
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        cls["methods"].append({
                            "name": item.name,
                            "lineno": item.lineno,
                            "args": [arg.arg for arg in item.args.args],
                            "docstring": ast.get_docstring(item),
                        })
                classes.append(cls)
        return classes
    
    def _get_variables(self) -> list:
        """استخراج المتغيرات العامة"""
        variables = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append({
                            "name": target.id,
                            "lineno": node.lineno,
                        })
        return variables
    
    def _get_decorators(self) -> list:
        """استخراج كل الديكورات"""
        decorators = []
        for node in ast.walk(self.tree):
            if hasattr(node, 'decorator_list'):
                for d in node.decorator_list:
                    decorators.append(self._get_decorator_name(d))
        return list(set(decorators))
    
    def _get_complexity(self) -> dict:
        """حساب تعقيد الكود"""
        complexity = 0
        lines = self.source.split('\n')
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler,
                                ast.With, ast.AsyncWith, ast.AsyncFor,
                                ast.BoolOp, ast.Try)):
                complexity += 1
        
        return {
            "cyclomatic_complexity": complexity,
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
            "blank_lines": len([l for l in lines if not l.strip()]),
        }
    
    def _get_decorator_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
        return str(type(node).__name__)
    
    def _get_base_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            if hasattr(node.value, 'id'):
                return f"{node.value.id}.{node.attr}"
            if hasattr(node.value, 'attr'):
                return f"{self._get_base_name(node.value)}.{node.attr}"
            return str(node.attr)
        return str(type(node).__name__)

# ============================================================
# محلل JavaScript/TypeScript
# ============================================================

class JavaScriptAnalyzer:
    """محلل متخصص لملفات JS/TS"""
    
    def __init__(self, source: str):
        self.source = source
    
    def analyze(self) -> dict:
        """تحليل كامل"""
        return {
            "language": self._detect_js_type(),
            "imports": self._get_imports(),
            "functions": self._get_functions(),
            "classes": self._get_classes(),
            "variables": self._get_variables(),
            "complexity": self._get_complexity(),
        }
    
    def _detect_js_type(self) -> str:
        if '.tsx' in str(getattr(self, 'filename', '')):
            return 'React TSX'
        if '.ts' in str(getattr(self, 'filename', '')):
            return 'TypeScript'
        if '.jsx' in str(getattr(self, 'filename', '')):
            return 'React JSX'
        return 'JavaScript'
    
    def _get_imports(self) -> list:
        imports = []
        patterns = [
            r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
            r'require\s*\([\'"](.+?)[\'"]\)',
            r'import\s+[\'"](.+?)[\'"]',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, self.source):
                imports.append({"module": match.group(1)})
        return imports
    
    def _get_functions(self) -> list:
        functions = []
        
        # function declaration
        for match in re.finditer(r'function\s+(\w+)\s*\(([^)]*)\)', self.source):
            functions.append({
                "name": match.group(1),
                "args": [a.strip() for a in match.group(2).split(',') if a.strip()],
                "type": "function",
            })
        
        # arrow functions
        for match in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>', self.source):
            functions.append({
                "name": match.group(1),
                "args": [a.strip() for a in match.group(2).split(',') if a.strip()],
                "type": "arrow",
            })
        
        # async functions
        for match in re.finditer(r'async\s+function\s+(\w+)\s*\(([^)]*)\)', self.source):
            functions.append({
                "name": match.group(1),
                "args": [a.strip() for a in match.group(2).split(',') if a.strip()],
                "type": "async",
            })
        
        return functions
    
    def _get_classes(self) -> list:
        classes = []
        for match in re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?', self.source):
            classes.append({
                "name": match.group(1),
                "extends": match.group(2) if match.lastindex >= 2 else None,
            })
        return classes
    
    def _get_variables(self) -> list:
        variables = []
        for match in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=', self.source):
            variables.append({"name": match.group(1)})
        return variables
    
    def _get_complexity(self) -> dict:
        lines = self.source.split('\n')
        complexity = len(re.findall(r'\b(if|for|while|switch|catch)\b', self.source))
        
        return {
            "cyclomatic_complexity": complexity,
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('//')]),
            "comment_lines": len([l for l in lines if l.strip().startswith('//')]),
            "blank_lines": len([l for l in lines if not l.strip()]),
        }

# ============================================================
# محلل HTML
# ============================================================

class HTMLAnalyzer:
    """محلل متخصص لملفات HTML"""
    
    def __init__(self, source: str):
        self.source = source
    
    def analyze(self) -> dict:
        lines = self.source.split('\n')
        
        tags = re.findall(r'<(\w+)', self.source)
        tag_counts = Counter(tags)
        
        return {
            "language": "HTML",
            "tags": [{"name": tag, "count": count} for tag, count in tag_counts.most_common(20)],
            "scripts": len(re.findall(r'<script', self.source)),
            "styles": len(re.findall(r'<style|link.*stylesheet', self.source)),
            "forms": len(re.findall(r'<form', self.source)),
            "images": len(re.findall(r'<img', self.source)),
            "links": len(re.findall(r'<a\s', self.source)),
            "complexity": {
                "total_lines": len(lines),
                "code_lines": len([l for l in lines if l.strip()]),
                "blank_lines": len([l for l in lines if not l.strip()]),
                "total_tags": len(tags),
                "unique_tags": len(set(tags)),
            }
        }

# ============================================================
# محلل CSS
# ============================================================

class CSSAnalyzer:
    """محلل متخصص لملفات CSS"""
    
    def __init__(self, source: str):
        self.source = source
    
    def analyze(self) -> dict:
        lines = self.source.split('\n')
        
        selectors = re.findall(r'([#\.]?\w+[^{]*)\s*\{', self.source)
        properties = re.findall(r'(\w+-\w+|\w+)\s*:', self.source)
        colors = re.findall(r'(#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))', self.source)
        
        return {
            "language": "CSS",
            "selectors_count": len(selectors),
            "properties_count": len(properties),
            "colors": list(set(colors))[:20],
            "selectors": selectors[:30],
            "complexity": {
                "total_lines": len(lines),
                "code_lines": len([l for l in lines if l.strip()]),
                "blank_lines": len([l for l in lines if not l.strip()]),
            }
        }

# ============================================================
# محلل JSON
# ============================================================

class JSONAnalyzer:
    """محلل متخصص لملفات JSON"""
    
    def __init__(self, source: str):
        self.source = source
    
    def analyze(self) -> dict:
        try:
            data = json.loads(self.source)
            return {
                "language": "JSON",
                "valid": True,
                "type": type(data).__name__,
                "keys": list(data.keys()) if isinstance(data, dict) else [],
                "size": len(data) if isinstance(data, (dict, list)) else 1,
            }
        except json.JSONDecodeError:
            return {
                "language": "JSON",
                "valid": False,
                "error": "صيغة JSON غير صالحة"
            }

# ============================================================
# المحلل العام
# ============================================================

class GeneralAnalyzer:
    """محلل عام لأي ملف نصي"""
    
    def __init__(self, source: str):
        self.source = source
    
    def analyze(self) -> dict:
        lines = self.source.split('\n')
        words = self.source.split()
        
        return {
            "language": "Text",
            "complexity": {
                "total_lines": len(lines),
                "code_lines": len([l for l in lines if l.strip()]),
                "blank_lines": len([l for l in lines if not l.strip()]),
                "total_words": len(words),
                "total_chars": len(self.source),
            }
        }

# ============================================================
# المحلل الرئيسي (واجهة موحدة)
# ============================================================

def analyze_file(filepath: str) -> dict:
    """
    تحليل ملف برمجي واستخراج هيكله
    
    Args:
        filepath: مسار الملف
    
    Returns:
        قاموس بنتيجة التحليل
    """
    path = Path(filepath)
    
    if not path.exists():
        return {"error": f"الملف غير موجود: {filepath}"}
    
    ext = path.suffix.lower()
    
    # قراءة الملف
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
    except Exception as e:
        return {"error": f"خطأ في قراءة الملف: {e}"}
    
    # معلومات أساسية
    result = {
        "filename": path.name,
        "filepath": str(path.absolute()),
        "extension": ext,
        "size_bytes": path.stat().st_size,
        "size_kb": round(path.stat().st_size / 1024, 2),
        "language": SUPPORTED_LANGUAGES.get(ext, 'Unknown'),
    }
    
    # تحليل حسب اللغة
    analyzer = None
    
    if ext == '.py':
        analyzer = PythonAnalyzer(source)
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        analyzer = JavaScriptAnalyzer(source)
    elif ext == '.html':
        analyzer = HTMLAnalyzer(source)
    elif ext == '.css':
        analyzer = CSSAnalyzer(source)
    elif ext == '.json':
        analyzer = JSONAnalyzer(source)
    else:
        analyzer = GeneralAnalyzer(source)
    
    if analyzer:
        result.update(analyzer.analyze())
    
    return result

def analyze_directory(directory: str) -> dict:
    """
    تحليل مجلد كامل
    
    Args:
        directory: مسار المجلد
    
    Returns:
        قاموس بإحصائيات المجلد
    """
    path = Path(directory)
    
    if not path.exists():
        return {"error": f"المجلد غير موجود: {directory}"}
    
    files = []
    total_stats = {
        "total_files": 0,
        "total_lines": 0,
        "total_size_kb": 0,
        "languages": Counter(),
        "file_types": Counter(),
    }
    
    for f in path.rglob('*'):
        if f.is_file() and f.suffix.lower() in SUPPORTED_LANGUAGES:
            analysis = analyze_file(str(f))
            files.append(analysis)
            
            total_stats["total_files"] += 1
            total_stats["total_size_kb"] += analysis.get("size_kb", 0)
            total_stats["languages"][analysis.get("language", "Unknown")] += 1
            total_stats["file_types"][f.suffix.lower()] += 1
            
            if "complexity" in analysis:
                total_stats["total_lines"] += analysis["complexity"].get("total_lines", 0)
    
    return {
        "directory": str(path.absolute()),
        "stats": dict(total_stats),
        "languages_summary": dict(total_stats["languages"]),
        "files_count": len(files),
        "files": files[:10],  # أول 10 ملفات فقط
        "more_files": len(files) - 10 if len(files) > 10 else 0
    }

# ============================================================
# اختبار سريع
# ============================================================

if __name__ == "__main__":
    print("🔍 اختبار محلل الأكواد\n")
    
    # تحليل config.py
    result = analyze_file("config.py")
    if "error" not in result:
        print(f"✅ {result['filename']}")
        print(f"   اللغة: {result['language']}")
        print(f"   الحجم: {result['size_kb']}KB")
        if "functions" in result:
            print(f"   الدوال: {len(result['functions'])}")
        if "complexity" in result:
            print(f"   الأسطر: {result['complexity']['total_lines']}")
    else:
        print(f"❌ {result['error']}")
    
    print("\n✅ اكتمل الاختبار")
