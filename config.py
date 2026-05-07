"""
إعدادات النظام المركزية
يدعم 3 بيئات: dev / test / prod
يحمي المفاتيح الحساسة في ملف .env
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# تحميل البيئة
# ============================================================

# تحديد البيئة من متغير النظام أو افتراضياً dev
ENV = os.getenv("DOCGEN_ENV", "dev")

# تحميل ملف .env المناسب
env_file = Path(__file__).parent / f".env.{ENV}"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(Path(__file__).parent / ".env")

# ============================================================
# إعدادات المسارات
# ============================================================

BASE_DIR = Path(__file__).parent.absolute()
SRC_DIR = BASE_DIR / "src"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"
TEMP_DIR = BASE_DIR / "temp"
TESTS_DIR = BASE_DIR / "tests"
DOCS_DIR = BASE_DIR / "docs"
BACKUP_DIR = BASE_DIR / "backups"

# تأكد من وجود المجلدات الضرورية
UPLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# ============================================================
# إعدادات الذكاء الاصطناعي
# ============================================================

# OpenRouter (المصدر الرئيسي)
AI_PROVIDER = os.getenv("AI_PROVIDER", "openrouter")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-lite-001")

# نموذج احتياطي
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "openai/gpt-3.5-turbo")

# ============================================================
# إعدادات الأمان
# ============================================================

# أنواع الملفات المسموحة
ALLOWED_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', 
                      '.java', '.php', '.rb', '.go', '.rs', '.swift',
                      '.c', '.cpp', '.h', '.json', '.xml', '.yaml', '.yml'}

# أنواع الملفات الممنوعة
BLOCKED_EXTENSIONS = {'.exe', '.dll', '.so', '.sh', '.bat', '.cmd', '.msi',
                      '.apk', '.bin', '.o', '.obj', '.pyc', '.class'}

# حجم الملف الأقصى (5 ميجابايت)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(5 * 1024 * 1024)))

# مدة الاحتفاظ بالملفات المؤقتة (ساعة)
TEMP_FILE_TTL = int(os.getenv("TEMP_FILE_TTL", "3600"))

# ============================================================
# إعدادات الجودة
# ============================================================

# الحد الأدنى لجودة التوثيق (%)
MIN_QUALITY_SCORE = float(os.getenv("MIN_QUALITY_SCORE", "7.0"))

# محاولات إعادة التوليد إذا كانت الجودة منخفضة
MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))

# ============================================================
# إعدادات السيرفر
# ============================================================

# المنفذ (يختلف حسب البيئة)
PORT_MAP = {
    "dev": int(os.getenv("DEV_PORT", "5000")),
    "test": int(os.getenv("TEST_PORT", "5001")),
    "prod": int(os.getenv("PROD_PORT", "8080"))
}
PORT = PORT_MAP.get(ENV, 5000)

# وضع التصحيح
DEBUG_MAP = {
    "dev": True,
    "test": True,
    "prod": False
}
DEBUG = DEBUG_MAP.get(ENV, False)

# المضيف (محلي فقط في الإنتاج)
HOST_MAP = {
    "dev": "127.0.0.1",
    "test": "127.0.0.1",
    "prod": "127.0.0.1"  # لا يستمع للخارج
}
HOST = HOST_MAP.get(ENV, "127.0.0.1")

# ============================================================
# إعدادات قاعدة البيانات
# ============================================================

DB_MAP = {
    "dev": os.getenv("DEV_DB", str(BASE_DIR / "data" / "dev.db")),
    "test": os.getenv("TEST_DB", str(BASE_DIR / "data" / "test.db")),
    "prod": os.getenv("PROD_DB", str(BASE_DIR / "data" / "prod.db"))
}
DATABASE_URL = DB_MAP.get(ENV)

# تأكد من وجود مجلد البيانات
Path(DATABASE_URL).parent.mkdir(exist_ok=True, parents=True)

# ============================================================
# إعدادات السجلات
# ============================================================

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"docgen_{ENV}.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if ENV == "prod" else "DEBUG")

# ============================================================
# إعدادات PWA
# ============================================================

PWA_NAME = "Doc Generator"
PWA_SHORT_NAME = "DocGen"
PWA_DESCRIPTION = "مولد توثيق احترافي بالذكاء الاصطناعي"
PWA_THEME_COLOR = "#0f0f0f"
PWA_BG_COLOR = "#1a1a1a"
PWA_ICONS_DIR = STATIC_DIR / "icons"

# ============================================================
# إعدادات التوثيق المولد
# ============================================================

# أنواع التوثيق المدعومة
DOC_TYPES = {
    "readme": "README.md",
    "docstrings": "كود موثق",
    "api": "API Documentation",
    "full": "توثيق كامل",
    "contributing": "CONTRIBUTING.md"
}

# اللغات المدعومة
SUPPORTED_LANGUAGES = {
    "ar": "العربية",
    "en": "English"
}

# قوالب التوثيق
TEMPLATES = {
    "readme_ar": TEMPLATES_DIR / "readme_ar.md",
    "readme_en": TEMPLATES_DIR / "readme_en.md",
    "api": TEMPLATES_DIR / "api_docs.md",
}

# ============================================================
# دوال مساعدة
# ============================================================

def get_config() -> dict:
    """يرجع كل الإعدادات كقاموس"""
    return {
        "env": ENV,
        "debug": DEBUG,
        "port": PORT,
        "host": HOST,
        "ai_provider": AI_PROVIDER,
        "model": OPENROUTER_MODEL,
        "max_file_size": MAX_FILE_SIZE,
        "min_quality": MIN_QUALITY_SCORE,
        "database": DATABASE_URL,
        "log_file": LOG_FILE,
    }

def is_production() -> bool:
    """هل البيئة إنتاج؟"""
    return ENV == "prod"

def is_development() -> bool:
    """هل البيئة تطوير؟"""
    return ENV == "dev"

def print_config():
    """طباعة الإعدادات الحالية (بدون مفاتيح)"""
    print(f"""
╔══════════════════════════════════════════╗
║        📚 Doc Generator Config           ║
╠══════════════════════════════════════════╣
║  البيئة:      {ENV:<28}║
║  المنفذ:      {PORT:<28}║
║  التصحيح:     {str(DEBUG):<28}║
║  النموذج:     {OPENROUTER_MODEL:<28}║
║  الحد الأقصى:  {MAX_FILE_SIZE//1024}KB{'':<24}║
║  الجودة:      ≥{MIN_QUALITY_SCORE}/10{'':<22}║
║  API Key:     {'✅ موجود' if OPENROUTER_API_KEY else '❌ غير موجود':<28}║
╚══════════════════════════════════════════╝
    """)

# ============================================================
# تشغيل مباشر (للاختبار)
# ============================================================

if __name__ == "__main__":
    print_config()
