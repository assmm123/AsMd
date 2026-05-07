"""
SaaS Usage Tracker - حدود الاشتراكات والتصفير التلقائي
"""

from datetime import datetime
from src.auth.models import db, save_db

# مستويات الاشتراك
TIERS = {
    "free": {"limit": 5, "label": "مجاني"},
    "basic": {"limit": 20, "label": "أساسي"},
    "pro": {"limit": 50, "label": "محترف"},
    "unlimited": {"limit": 100, "label": "غير محدود"},
}

# محفظة الاستقبال
TRUST_WALLET = "TGZWQ6w9R8ACF3eFqzTFiwDLhLezBctR7K"

# أسعار المستويات بالدولار
TIER_PRICES = {
    "basic": 5,
    "pro": 15,
    "unlimited": 30,
}


def reset_daily_if_new_day(user):
    """تصفير العداد إذا تغير اليوم"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if user.get("last_request_date") != today:
        user["daily_requests"] = 0
        user["last_request_date"] = today


def check_quota(user_id):
    """التحقق من حد المستخدم - يرجع (مسموح, رسالة)"""
    user = db.get_user(user_id)
    if not user:
        return False, "User not found"

    reset_daily_if_new_day(user)

    # التحقق من صلاحية الاشتراك
    expires_at = user.get("expires_at")
    if expires_at and datetime.utcnow().isoformat() > expires_at:
        user["tier"] = "free"
        user["expires_at"] = None
        save_db()

    tier = user.get("tier", "free")
    limit = TIERS.get(tier, TIERS["free"])["limit"]
    used = user.get("daily_requests", 0)

    if used >= limit:
        return False, f"Daily limit reached ({limit} requests). Upgrade to continue."

    return True, "OK"


def track_request(user_id):
    """تسجيل طلب وزيادة العداد"""
    user = db.get_user(user_id)
    if not user:
        return

    reset_daily_if_new_day(user)
    user["daily_requests"] = user.get("daily_requests", 0) + 1
    save_db()


def get_usage(user_id):
    """إحصائيات استخدام المستخدم"""
    user = db.get_user(user_id)
    if not user:
        return None

    reset_daily_if_new_day(user)
    tier = user.get("tier", "free")
    limit = TIERS.get(tier, TIERS["free"])["limit"]

    return {
        "tier": tier,
        "tier_label": TIERS[tier]["label"],
        "daily_limit": limit,
        "daily_used": user.get("daily_requests", 0),
        "daily_remaining": max(0, limit - user.get("daily_requests", 0)),
        "expires_at": user.get("expires_at"),
    }


def activate_tier(user_id, tier, duration_days=30):
    """تفعيل اشتراك لمستخدم"""
    from datetime import timedelta

    user = db.get_user(user_id)
    if not user:
        return False

    if tier not in TIERS or tier == "free":
        return False

    user["tier"] = tier
    user["daily_requests"] = 0
    user["expires_at"] = (datetime.utcnow() + timedelta(days=duration_days)).isoformat()
    save_db()
    return True

def track_daily():
    """تسجيل طلب في الإحصائيات اليومية"""
    import json, os
    from datetime import datetime
    today = datetime.utcnow().strftime('%Y-%m-%d')
    usage_file = 'data/daily_usage.json'
    data = {}
    if os.path.exists(usage_file):
        data = json.load(open(usage_file))
    data[today] = data.get(today, 0) + 1
    if not os.path.exists('data'):
        os.makedirs('data')
    json.dump(data, open(usage_file, 'w'))
