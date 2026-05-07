import os
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

MAX_SIZE = 5 * 1024 * 1024
BACKUPS = 7

COLORS = {
    'DEBUG': '\033[36m',
    'INFO': '\033[32m',
    'WARNING': '\033[33m',
    'ERROR': '\033[31m',
    'CRITICAL': '\033[35m',
    'RESET': '\033[0m',
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        c = COLORS.get(record.levelname, '')
        r = COLORS['RESET']
        t = datetime.now().strftime('%H:%M:%S')
        return f"{c}{t} [{record.levelname}] {record.getMessage()}{r}"

class LoggerManager:
    def __init__(self, name="docgen", env="dev"):
        self.name = name
        self.env = env
        self.logger = logging.getLogger(f"{name}_{env}")
        self.logger.setLevel(logging.DEBUG)
        self.stats = {'debug':0,'info':0,'warning':0,'error':0,'critical':0}
        self._setup()
    
    def _setup(self):
        self.logger.handlers.clear()
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if self.env != 'prod' else logging.WARNING)
        ch.setFormatter(ColoredFormatter())
        self.logger.addHandler(ch)
        
        fh = logging.handlers.RotatingFileHandler(
            LOG_DIR / f"{self.name}_{self.env}.log",
            maxBytes=MAX_SIZE, backupCount=BACKUPS
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self.logger.addHandler(fh)
        
        eh = logging.handlers.RotatingFileHandler(
            LOG_DIR / f"{self.name}_{self.env}_errors.log",
            maxBytes=MAX_SIZE, backupCount=BACKUPS
        )
        eh.setLevel(logging.ERROR)
        eh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self.logger.addHandler(eh)
    
    def debug(self, msg): self.logger.debug(msg); self.stats['debug']+=1
    def info(self, msg): self.logger.info(msg); self.stats['info']+=1
    def warning(self, msg): self.logger.warning(msg); self.stats['warning']+=1
    def error(self, msg): self.logger.error(msg); self.stats['error']+=1
    def critical(self, msg): self.logger.critical(msg); self.stats['critical']+=1
    
    def get_stats(self):
        return {**self.stats, 'total': sum(self.stats.values())}

_instances = {}

def get_logger(name="docgen", env=None):
    if env is None:
        try:
            from config import ENV
            env = ENV
        except:
            env = "dev"
    key = f"{name}_{env}"
    if key not in _instances:
        _instances[key] = LoggerManager(name, env)
    return _instances[key]

if __name__ == "__main__":
    log = get_logger("test", "dev")
    log.debug("رسالة تصحيح")
    log.info("رسالة معلومات")
    log.warning("رسالة تحذير")
    log.error("رسالة خطأ")
    log.critical("رسالة خطأ حرج")
    print(f"\nسجلات: {log.get_stats()}")
    print(f"ملفات في: {LOG_DIR}")
    for f in sorted(LOG_DIR.glob("test*")):
        print(f"  {f.name} ({f.stat().st_size}b)")
