import os
import datetime
import jwt
from config import ENV

# ============================================================
# المفتاح السري - Fail-Safe Security
# ============================================================

SECRET = os.getenv("JWT_SECRET")
if not SECRET:
    if ENV == "prod":
        raise RuntimeError("JWT_SECRET must be set in production environment")
    SECRET = "docgen-dev-secret-not-for-production"

# ============================================================
# دوال JWT
# ============================================================

def create_token(user_id, role="user"):
    """
    إنشاء JWT token - للهوية فقط
    Args:
        user_id: معرف المستخدم الثابت
        role: صلاحية المستخدم (user/admin)
    Returns:
        JWT token string
    """
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        'user_id': user_id,
        'role': role,
        'iat': now,
        'exp': now + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')


def verify_token(token):
    """
    فك والتحقق من JWT token
    Args:
        token: JWT token string
    Returns:
        payload dict إذا كان التوكن صالحاً، None إذا كان غير صالح
    """
    if not token:
        return None
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
