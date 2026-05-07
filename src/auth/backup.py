import shutil, os
from datetime import datetime

def backup_database():
    src = os.path.join(os.path.dirname(__file__), 'users.json')
    if os.path.exists(src):
        dst = os.path.join(os.path.dirname(__file__), f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        shutil.copy(src, dst)
        return dst
    return None

def auto_backup():
    import threading
    backup_database()
    threading.Timer(3600, auto_backup).start()
