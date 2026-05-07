"""
Middleware المصادقة - يحمي المسارات
JWT للهوية فقط - user_id و role من التوكن
الحالة المتغيرة من قاعدة البيانات
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from functools import wraps
from flask import request, jsonify, g
from src.auth.jwt import verify_token
from src.auth.models import db


def get_token_from_request():
    """استخراج JWT من الطلب - Header أو Cookie"""
    # المحاولة الأولى: Authorization header
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    # المحاولة الثانية: Cookie
    token = request.cookies.get('token', '')
    if token:
        return token
    
    return None


def login_required(f):
    """
    ديكور: يتحقق من JWT ويجيب المستخدم من قاعدة البيانات
    JWT للهوية فقط - user_id و role
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({
                "success": False,
                "error": "Missing authorization token"
            }), 401
        
        payload = verify_token(token)
        if payload is None:
            return jsonify({
                "success": False,
                "error": "Invalid or expired token"
            }), 401
        
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Invalid token payload"
            }), 401
        
        user = db.get_user(user_id)
        if user is None:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 401
        
        # تخزين للاستخدام في المسار
        g.user_id = user_id
        g.user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    ديكور: يتحقق من صلاحية admin
    يجب استخدامه بعد login_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'user'):
            return jsonify({
                "success": False,
                "error": "Authentication required first"
            }), 401
        
        if g.user.get('role') != 'admin':
            return jsonify({
                "success": False,
                "error": "Admin access required"
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
