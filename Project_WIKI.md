# دليل المشروع

## نظرة عامة
هذا المشروع مكتوب بلغة **Multi-file** ويحتوي على **127** دالة و **29** كلاس.

## دليل الدوال

### `analyze_file(filepath)`
تحليل ملف برمجي واستخراج هيكله

### `analyze_directory(directory)`
تحليل مجلد كامل

### `analyze(self)`
تحليل كامل

### `analyze(self)`
تحليل كامل

### `analyze(self)`
الوصف

### `analyze(self)`
الوصف

### `analyze(self)`
الوصف

### `analyze(self)`
الوصف

### `generate_readme_advanced(analysis, style, language, project_name, description, author, repo_url, license_type)`
الوصف

### `generate_api_docs_advanced(analysis, style, language)`
الوصف

### `generate_wiki(analysis, language)`
الوصف

### `generate_changelog(analysis, version)`
الوصف

### `generate_all_docs(source_code, analysis, project_name, style, language, doc_types)`
الوصف

### `get_quality_report(docs)`
الوصف

### `get_badge(label, message, color)`
الوصف

### `get_table(headers, rows)`
الوصف

### `get_code_block(code, language)`
الوصف

### `get_alert(text, alert_type)`
الوصف

### `get_section(title, content, level)`
الوصف

### `check_readme(content)`
الوصف

## دليل الكلاسات

### `class PythonAnalyzer`
محلل متخصص لملفات Python
الطرق: `__init__()`, `analyze()`, `_get_imports()`, `_has_return()`, `_find_raises()`, `_get_function_info()`, `_get_functions()`, `_get_classes()`, `_get_variables()`, `_get_decorators()`, `_get_complexity()`, `_get_decorator_name()`, `_get_base_name()`

### `class JavaScriptAnalyzer`
محلل متخصص لملفات JS/TS
الطرق: `__init__()`, `analyze()`, `_detect_js_type()`, `_get_imports()`, `_get_functions()`, `_get_classes()`, `_get_variables()`, `_get_complexity()`

### `class HTMLAnalyzer`
محلل متخصص لملفات HTML
الطرق: `__init__()`, `analyze()`

### `class CSSAnalyzer`
محلل متخصص لملفات CSS
الطرق: `__init__()`, `analyze()`

### `class JSONAnalyzer`
محلل متخصص لملفات JSON
الطرق: `__init__()`, `analyze()`

### `class GeneralAnalyzer`
محلل عام لأي ملف نصي
الطرق: `__init__()`, `analyze()`

### `class TemplateEngine`
الطرق: `get_badge()`, `get_table()`, `get_code_block()`, `get_alert()`, `get_section()`

### `class QualityChecker`
الطرق: `check_readme()`

### `class KeyInfo`
الطرق: `__init__()`

### `class KeyManager`
الطرق: `__init__()`, `_load_keys()`, `get_key()`, `mark_success()`, `mark_failure()`, `get_stats()`, `print_report()`

## أمثلة استخدام
```python
import module
result = analyze_file()
```

## بداية سريعة
1. تثبيت المتطلبات: `pip install -r requirements.txt`
2. استيراد المكتبات المطلوبة
3. استخدام الدوال والكلاسات حسب الحاجة