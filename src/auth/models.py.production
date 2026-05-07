import hashlib
import os
import json
from datetime import datetime, timezone

# ============================================================
# إعدادات
# ============================================================

DB_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
DB_FILE = os.path.join(DB_DIR, 'users.json')

os.makedirs(DB_DIR, exist_ok=True)

# ============================================================
# دوال مساعدة
# ============================================================

def hash_password(password):
    """تشفير كلمة المرور بـ PBKDF2 مع salt عشوائي"""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ':' + key.hex()


def generate_activation_code(tier):
    """توليد كود تفعيل حسب المستوى"""
    import random
    import string

    prefix_map = {
        "basic": "DOC-BASIC",
        "pro": "DOC-PRO",
        "unlimited": "DOC-UNLIM",
    }
    prefix = prefix_map.get(tier, "DOC-FREE")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{suffix}"


# ============================================================
# قاعدة بيانات المستخدمين
# ============================================================

class UserDB:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password, email=''):
        """إنشاء مستخدم جديد"""
        if username in self.users:
            return None
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        self.users[username] = {
            'username': username,
            'password': salt.hex() + ':' + key.hex(),
            'email': email,
            'role': 'user',
            'tier': 'free',
            'daily_requests': 0,
            'last_request_date': None,
            'expires_at': None,
            'activation_code': None,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'provider': 'email'
        }
        return self.users[username]

    def create_google_user(self, google_id, email, name):
        """إنشاء مستخدم عبر Google OAuth"""
        username = email.split('@')[0]
        if username in self.users:
            return self.users[username]
        self.users[username] = {
            'username': username,
            'password': None,
            'email': email,
            'name': name,
            'role': 'user',
            'tier': 'free',
            'daily_requests': 0,
            'last_request_date': None,
            'expires_at': None,
            'activation_code': None,
            'google_id': google_id,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'provider': 'google'
        }
        return self.users[username]

    def authenticate(self, username, password):
        """التحقق من اسم المستخدم وكلمة المرور"""
        user = self.users.get(username)
        if user and user.get('password'):
            salt = bytes.fromhex(user['password'].split(':')[0])
            key = bytes.fromhex(user['password'].split(':')[1])
            if hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000) == key:
                return user
        return None

    def get_user(self, username):
        """استرجاع مستخدم بالاسم"""
        return self.users.get(username)

    def get_all_users(self):
        """استرجاع كل المستخدمين"""
        return list(self.users.values())


# ============================================================
# قاعدة بيانات عالمية
# ============================================================

db = UserDB()

# ============================================================
# دوال الحفظ والاسترجاع
# ============================================================

def save_db():
    """حفظ قاعدة البيانات إلى ملف JSON"""
    with open(DB_FILE, 'w') as f:
        json.dump(db.users, f, indent=2)

def load_db():
    """تحميل قاعدة البيانات من ملف JSON"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            db.users = json.load(f)

load_db()
