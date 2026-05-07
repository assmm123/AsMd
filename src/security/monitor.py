import time, threading

class SystemMonitor:
    def __init__(self):
        self.stats = {'requests': 0, 'errors': 0, 'start_time': time.time()}
    
    def track_request(self):
        self.stats['requests'] += 1
    
    def track_error(self):
        self.stats['errors'] += 1
    
    def get_stats(self):
        uptime = time.time() - self.stats['start_time']
        return {
            'uptime_hours': round(uptime / 3600, 2),
            'total_requests': self.stats['requests'],
            'total_errors': self.stats['errors'],
            'error_rate': f"{self.stats['errors'] / max(self.stats['requests'], 1) * 100:.1f}%",
            'requests_per_minute': round(self.stats['requests'] / max(uptime / 60, 1), 1)
        }

monitor = SystemMonitor()
