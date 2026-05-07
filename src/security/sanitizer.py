"""
منظف المدخلات - Input Sanitizer
يمنع: SQL Injection, XSS, Command Injection, Path Traversal
"""

import re
import html
from typing import Tuple, Any

# ============================================================
# أنماط خطيرة
# ============================================================

SQL_INJECTION_PATTERNS = [
    r"(\bSELECT\b.*\bFROM\b|\bINSERT\b.*\bINTO\b|\bUPDATE\b.*\bSET\b|\bDELETE\b.*\bFROM\b)",
    r"(\bDROP\b.*\bTABLE\b|\bALTER\b.*\bTABLE\b|\bCREATE\b.*\bTABLE\b)",
    r"(--|\#|\/\*|\*\/)",
    r"(\bUNION\b.*\bSELECT\b)",
    r"(\bOR\b.*=.*\bOR\b|\bAND\b.*=.*\bAND\b)",
    r"(;\s*\bDROP\b|\;\s*\bDELETE\b)",
]

XSS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"javascript\s*:",
    r"on\w+\s*=\s*[\"'][^\"']*[\"']",
    r"<iframe[^>]*>",
    r"<embed[^>]*>",
    r"<object[^>]*>",
    r"eval\s*\([^)]*\)",
    r"document\.cookie",
    r"document\.write\s*\(",
]

COMMAND_INJECTION_PATTERNS = [
    r"[;&|`$]",
    r"\$\(.*\)",
    r"`[^`]*`",
    r"system\s*\(",
    r"exec\s*\(",
    r"passthru\s*\(",
    r"shell_exec\s*\(",
]

PATH_TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"\.\.\\",
    r"~",
    r"\0",
    r"%00",
]

# ============================================================
# دوال التنظيف
# ============================================================

def sanitize_text(text: str, max_length: int = 5000) -> Tuple[str, list]:
    """
    تنظيف النص العام
    
    Args:
        text: النص المراد تنظيفه
        max_length: أقصى طول مسموح
    
    Returns:
        (النص المنظف, قائمة التحذيرات)
    """
    warnings = []
    
    if not isinstance(text, str):
        return str(text)[:max_length], ["WARNING: Non-string input converted"]
    
    # قص النص إذا طويل جداً
    if len(text) > max_length:
        text = text[:max_length]
        warnings.append(f"WARNING: Text truncated to {max_length} chars")
    
    # تنظيف HTML entities
    text = html.escape(text, quote=False)
    
    # إزالة أحرف null
    text = text.replace('\0', '')
    
    # إزالة أحرف التحكم (ماعدا الأسطر الجديدة والتبويب)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    return text, warnings

def sanitize_filename(filename: str) -> Tuple[str, list]:
    """
    تنظيف اسم الملف
    
    Args:
        filename: اسم الملف
    
    Returns:
        (الاسم المنظف, تحذيرات)
    """
    warnings = []
    
    if not filename:
        return "untitled", ["WARNING: Empty filename"]
    
    # إزالة المسارات
    filename = re.sub(r'[\\/]', '_', filename)
    
    # إزالة path traversal
    if '..' in filename:
        filename = filename.replace('..', '')
        warnings.append("WARNING: Path traversal removed")
    
    # إزالة أحرف خطيرة
    filename = re.sub(r'[<>:"|?*\x00-\x1f]', '_', filename)
    
    # إزالة المسافات الزائدة
    filename = filename.strip()
    
    # حد أقصى للطول
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + '.' + ext
    
    # لا تبدأ بنقطة (ملف مخفي)
    if filename.startswith('.'):
        filename = '_' + filename[1:]
        warnings.append("WARNING: Hidden file renamed")
    
    if not filename:
        filename = "untitled"
    
    return filename, warnings

def sanitize_code(code: str, max_length: int = 100000) -> Tuple[str, list]:
    """
    تنظيف الكود البرمجي
    
    Args:
        code: الكود
        max_length: أقصى طول
    
    Returns:
        (الكود المنظف, تحذيرات)
    """
    warnings = []
    
    if len(code) > max_length:
        code = code[:max_length]
        warnings.append(f"WARNING: Code truncated to {max_length} chars")
    
    # إزالة أحرف null
    code = code.replace('\0', '')
    
    # فحص command injection
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            warnings.append(f"WARNING: Potential command injection detected")
    
    return code, warnings

def sanitize_url(url: str) -> Tuple[str, list]:
    """
    تنظيف الرابط
    """
    warnings = []
    
    if not isinstance(url, str):
        return "", ["ERROR: Invalid URL"]
    
    url = url.strip()
    
    # إزالة javascript:
    if url.lower().startswith('javascript:'):
        return "", ["ERROR: javascript: URL blocked"]
    
    # السماح فقط بـ http/https
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        warnings.append("WARNING: https:// added")
    
    return url, warnings

def detect_threats(text: str) -> dict:
    """
    كشف التهديدات في النص
    
    Returns:
        قاموس بنوع التهديد وخطورته
    """
    threats = {}
    
    # فحص SQL Injection
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            threats['sql_injection'] = 'HIGH'
            break
    
    # فحص XSS
    for pattern in XSS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            threats['xss'] = 'HIGH'
            break
    
    # فحص Command Injection
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            threats['command_injection'] = 'CRITICAL'
            break
    
    # فحص Path Traversal
    for pattern in PATH_TRAVERSAL_PATTERNS:
        if re.search(pattern, text):
            threats['path_traversal'] = 'MEDIUM'
            break
    
    return threats

def deep_clean(text: str, max_length: int = 5000) -> str:
    """
    تنظيف عميق - يستخدم قبل التخزين أو العرض
    
    Args:
        text: النص الخام
        max_length: أقصى طول
    
    Returns:
        نص نظيف وآمن
    """
    # 1. كشف التهديدات
    threats = detect_threats(text)
    
    # 2. تنظيف أساسي
    text, _ = sanitize_text(text, max_length)
    
    # 3. إزالة أي HTML متبقي
    text = html.escape(text)
    
    # 4. تنظيف نهائي
    text = text.strip()
    
    return text, threats

# ============================================================
# اختبار
# ============================================================

if __name__ == "__main__":
    print("Testing Sanitizer...")
    
    # اختبار XSS
    xss = '<script>alert("hack")</script>'
    clean, threats = deep_clean(xss)
    print(f"XSS Test: {clean[:50]} | Threats: {threats}")
    
    # اختبار SQL Injection
    sqli = "SELECT * FROM users WHERE id = 1 OR 1=1"
    t = detect_threats(sqli)
    print(f"SQLi Test: {t}")
    
    # اختبار Path Traversal
    path = "../../../etc/passwd"
    clean, w = sanitize_filename(path)
    print(f"Path Test: {clean} | Warnings: {w}")
    
    # اختبار أمر خطير
    cmd = "rm -rf / ; cat /etc/shadow"
    t = detect_threats(cmd)
    print(f"Command Test: {t}")
    
    print("Done")
