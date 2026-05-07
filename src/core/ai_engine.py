import os, re, time, random, logging, threading, json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

import httpx

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('AIEngine')

BASE_URL = 'https://openrouter.ai/api/v1'
DEFAULT_MODEL = 'google/gemini-2.0-flash-lite-001'
MAX_RETRIES = 3
BASE_DELAY = 1.0
MAX_FAILURES = 3
COOLDOWN_MINUTES = 5

class KeyInfo:
    def __init__(self, key):
        self.key = key
        self.masked = key[:15] + '...' + key[-10:] if len(key) > 25 else '***'
        self.uses = 0
        self.successes = 0
        self.failures = 0
        self.last_used = None
        self.active = True
        self.cooldown_until = None
        self.total_tokens = 0

class KeyManager:
    def __init__(self, keys_file=None):
        self.lock = threading.Lock()
        self.keys = {}
        self._load_keys(keys_file)
    
    def _load_keys(self, keys_file=None):
        paths = [keys_file] if keys_file else [
            Path.home() / 'مفاتيح_مرتبة.txt',
            Path.home() / 'openrouter_keys.txt'
        ]
        
        content = ''
        for p in paths:
            if p and Path(p).exists():
                with open(p) as f:
                    content = f.read()
                break
        
        if not content:
            logger.warning('No keys file found')
            return
        
        pattern = r'sk-or-v1-[a-zA-Z0-9]{64}'
        found = list(set(re.findall(pattern, content)))
        
        for key in found:
            self.keys[key] = KeyInfo(key)
        
        logger.info(f'Loaded {len(self.keys)} OpenRouter keys')
    
    def get_key(self):
        with self.lock:
            now = datetime.now()
            available = []
            for key, info in self.keys.items():
                if not info.active:
                    if info.cooldown_until and now > info.cooldown_until:
                        info.active = True
                        info.cooldown_until = None
                    else:
                        continue
                available.append(key)
            
            if not available:
                for key in self.keys:
                    self.keys[key].active = True
                available = list(self.keys.keys())
            
            if not available:
                return None
            
            key = random.choice(available)
            self.keys[key].uses += 1
            self.keys[key].last_used = now
            return key
    
    def mark_success(self, key, tokens=0):
        with self.lock:
            if key in self.keys:
                self.keys[key].successes += 1
                self.keys[key].active = True
                self.keys[key].total_tokens += tokens
    
    def mark_failure(self, key, error=''):
        with self.lock:
            if key in self.keys:
                info = self.keys[key]
                info.failures += 1
                info.last_error = error
                if info.failures >= MAX_FAILURES:
                    info.active = False
                    info.cooldown_until = datetime.now() + timedelta(minutes=COOLDOWN_MINUTES)
                    logger.warning(f'Key disabled: {info.masked}')
    
    def get_stats(self):
        with self.lock:
            total = len(self.keys)
            active = sum(1 for i in self.keys.values() if i.active)
            uses = sum(i.uses for i in self.keys.values())
            successes = sum(i.successes for i in self.keys.values())
            failures = sum(i.failures for i in self.keys.values())
            tokens = sum(i.total_tokens for i in self.keys.values())
            return {
                'total_keys': total,
                'active_keys': active,
                'disabled_keys': total - active,
                'total_uses': uses,
                'total_successes': successes,
                'total_failures': failures,
                'total_tokens': tokens,
                'success_rate': f'{(successes / max(uses, 1)) * 100:.1f}%'
            }
    
    def print_report(self):
        s = self.get_stats()
        print(f'Keys: {s["total_keys"]} | Active: {s["active_keys"]} | Disabled: {s["disabled_keys"]}')
        print(f'Uses: {s["total_uses"]} | Success: {s["success_rate"]} | Tokens: {s["total_tokens"]}')

class AIEngine:
    def __init__(self, keys_file=None):
        self.key_manager = KeyManager(keys_file)
        self.base_url = BASE_URL
        self.default_model = DEFAULT_MODEL
        self.total_requests = 0
        self.total_tokens = 0
    
    def _chat_request(self, api_key, messages, model, temperature, max_tokens):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/doc-generator',
            'X-Title': 'Doc Generator'
        }
        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        response = httpx.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=data,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    
    def chat(self, messages, model=None, temperature=0.7, max_tokens=4000):
        if model is None:
            model = self.default_model
        
        last_error = ''
        
        for attempt in range(MAX_RETRIES):
            key = self.key_manager.get_key()
            if not key:
                return {'success': False, 'error': 'No keys available'}
            
            try:
                result = self._chat_request(key, messages, model, temperature, max_tokens)
                content = result['choices'][0]['message']['content']
                tokens = result.get('usage', {}).get('total_tokens', 0)
                
                self.key_manager.mark_success(key, tokens)
                self.total_requests += 1
                self.total_tokens += tokens
                
                return {
                    'success': True,
                    'content': content,
                    'model': model,
                    'tokens': tokens
                }
                
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg[:200]
                
                is_quota = any(w in error_msg.lower() for w in [
                    'insufficient', 'balance', 'quota', 'billing',
                    'unauthorized', 'invalid', 'expired', 'rate', '429'
                ])
                
                if is_quota:
                    self.key_manager.mark_failure(key, error_msg[:100])
                
                delay = min(BASE_DELAY * (2 ** attempt), 10.0)
                
                if attempt < MAX_RETRIES - 1:
                    time.sleep(delay)
        
        return {'success': False, 'error': last_error}
    
    def generate_docs(self, code, language='Python', doc_type='readme'):
        prompts = {
            'readme': f'Write README.md in Arabic for this {language} project. Include: title, description, features, installation, usage, stats. Code:\n{code[:3000]}',
            'api': f'Write API docs in Arabic for this {language} code. Document all functions with parameters and examples. Code:\n{code[:3000]}',
        }
        prompt = prompts.get(doc_type, prompts['readme'])
        
        return self.chat(
            messages=[
                {'role': 'system', 'content': 'You are an expert programmer. Respond in Arabic with Markdown.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3
        )

_engine_instance = None
_engine_lock = threading.Lock()

def get_engine(keys_file=None):
    global _engine_instance
    with _engine_lock:
        if _engine_instance is None:
            _engine_instance = AIEngine(keys_file)
        return _engine_instance

if __name__ == '__main__':
    print('=' * 50)
    print('AI Engine - Self Test')
    print('=' * 50)
    engine = AIEngine()
    engine.key_manager.print_report()
    
    print('\nTesting chat...')
    result = engine.chat([{'role': 'user', 'content': 'رد بكلمة واحدة فقط: مرحباً'}])
    if result['success']:
        print(f'Response: {result["content"][:200]}')
        print(f'Tokens: {result["tokens"]}')
    else:
        print(f'Error: {result["error"][:150]}')
    
    print('Done')
