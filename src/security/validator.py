import re
import os
from pathlib import Path

def validate_username(username):
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username: letters, numbers, underscore only"
    return True, ""

def validate_email(email):
    if not email:
        return True, ""
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return False, "Invalid email format"
    return True, ""

def validate_password(password):
    if not password or len(password) < 3:
        return False, "Password must be at least 3 characters"
    if len(password) > 100:
        return False, "Password too long"
    return True, ""

def detect_language(filename):
    """تحديد لغة البرمجة من امتداد الملف"""
    ext = Path(filename).suffix.lower()
    mapping = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'React JSX',
        '.ts': 'TypeScript',
        '.tsx': 'React TSX',
        '.html': 'HTML',
        '.css': 'CSS',
        '.json': 'JSON',
        '.java': 'Java',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.md': 'Markdown',
        '.txt': 'Text',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.mm': 'Objective-C++',
    }
    return mapping.get(ext, 'Unknown')

def validate_file_extension(filename):
    """التحقق من أن امتداد الملف مسموح به"""
    from config import ALLOWED_EXTENSIONS
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

def validate_file_size(content, max_size=5*1024*1024):
    """التحقق من أن حجم الملف تحت الحد المسموح"""
    if isinstance(content, str):
        content = content.encode('utf-8')
    return len(content) <= max_size

def validate_file_content(content):
    """التحقق من أن المحتوى خالي من تهديدات"""
    try:
        from src.security.sanitizer import detect_threats
        threats = detect_threats(content)
        return len(threats) == 0
    except ImportError:
        return True

def sanitize_filename(filename):
    """تنظيف اسم الملف من المسارات الخطيرة"""
    filename = os.path.basename(filename)
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    if not filename:
        filename = 'untitled'
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    return filename

def validate_file(filename, content):
    """التحقق الكامل من الملف"""
    return (validate_file_extension(filename) and
            validate_file_size(content) and
            validate_file_content(content))

def get_file_stats(filepath):
    """الحصول على إحصائيات الملف"""
    path = Path(filepath)
    if path.exists() and path.is_file():
        return {
            "size": path.stat().st_size,
            "extension": path.suffix.lower(),
            "exists": True
        }
    return {
        "size": 0,
        "extension": "",
        "exists": False
    }
