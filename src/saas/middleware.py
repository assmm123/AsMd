"""
SaaS Middleware - فحص حدود الاستخدام
JWT للهوية فقط - الحالة من قاعدة البيانات
"""

from functools import wraps
from flask import request, jsonify, g
from src.saas.usage import check_quota, track_request


def require_quota(f):
    """
    ديكور: يتحقق من حد المستخدم قبل تنفيذ الطلب
    يوضع بعد @login_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = getattr(g, 'user_id', None)
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        allowed, msg = check_quota(user_id)
        if not allowed:
            return jsonify({
                "success": False,
                "error": msg,
                "upgrade_url": "/upgrade"
            }), 429

        # تسجيل الطلب
        track_request(user_id)

        return f(*args, **kwargs)

    return decorated_function

# Auto-log activity on each request
def log_request(action='طلب'):
    from flask import g
    from src.saas.logger import log_activity
    user_id = getattr(g, 'user_id', None)
    if user_id:
        log_activity(user_id, action)
