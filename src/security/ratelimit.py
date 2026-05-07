import time
import threading
from collections import defaultdict

REQUESTS_PER_MINUTE = 30
REQUESTS_PER_HOUR = 200
REQUESTS_PER_DAY = 1000
BAN_DURATION = 300

class RateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.ips = {}
    
    def _get_ip_data(self, ip):
        if ip not in self.ips:
            self.ips[ip] = {
                'minute_requests': [],
                'hour_requests': [],
                'day_requests': [],
                'banned_until': 0,
                'total_requests': 0,
                'violations': 0
            }
        return self.ips[ip]
    
    def _clean_old(self, data):
        now = time.time()
        data['minute_requests'] = [t for t in data['minute_requests'] if t > now - 60]
        data['hour_requests'] = [t for t in data['hour_requests'] if t > now - 3600]
        data['day_requests'] = [t for t in data['day_requests'] if t > now - 86400]
    
    def check(self, ip):
        with self.lock:
            now = time.time()
            data = self._get_ip_data(ip)
            
            if data['banned_until'] > now:
                remaining = int(data['banned_until'] - now)
                return False, f"Banned. Try after {remaining}s"
            
            self._clean_old(data)
            
            if len(data['minute_requests']) >= REQUESTS_PER_MINUTE:
                data['violations'] += 1
                if data['violations'] >= 3:
                    data['banned_until'] = now + BAN_DURATION
                    return False, "Banned for 5 minutes"
                return False, "Rate limit: 30/min"
            
            if len(data['hour_requests']) >= REQUESTS_PER_HOUR:
                return False, "Rate limit: 200/hour"
            
            if len(data['day_requests']) >= REQUESTS_PER_DAY:
                return False, "Rate limit: 1000/day"
            
            data['minute_requests'].append(now)
            data['hour_requests'].append(now)
            data['day_requests'].append(now)
            data['total_requests'] += 1
            
            return True, "OK"
    
    def get_stats(self, ip):
        with self.lock:
            data = self._get_ip_data(ip)
            self._clean_old(data)
            return {
                'ip': ip,
                'minute': len(data['minute_requests']),
                'hour': len(data['hour_requests']),
                'total': data['total_requests'],
                'banned': data['banned_until'] > time.time()
            }
    
    def reset(self, ip):
        with self.lock:
            if ip in self.ips:
                self.ips[ip]['banned_until'] = 0
                self.ips[ip]['violations'] = 0

_limiter = RateLimiter()

def get_limiter():
    return _limiter

def check_rate_limit(ip):
    return _limiter.check(ip)

if __name__ == "__main__":
    limiter = RateLimiter()
    for i in range(31):
        ok, msg = limiter.check("127.0.0.1")
        if not ok:
            print(f"Request {i+1}: {msg}")
            break
    print("Done")
