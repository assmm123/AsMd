"""Activity Logger - تتبع العمليات"""
import json, os
from datetime import datetime

LOG_FILE = 'data/activity_log.json'

def log_activity(username, action):
    """تسجيل نشاط مستخدم"""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            logs = json.load(open(LOG_FILE))
        except:
            logs = []
    logs.append({
        'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
        'user': username,
        'action': action
    })
    logs = logs[-100:]
    os.makedirs('data', exist_ok=True)
    json.dump(logs, open(LOG_FILE, 'w'))

def get_recent_logs(limit=10):
    """استرجاع آخر العمليات"""
    if os.path.exists(LOG_FILE):
        try:
            logs = json.load(open(LOG_FILE))
            return logs[-limit:][::-1]
        except:
            pass
    return []
