import os
import base64
import hashlib
from cryptography.fernet import Fernet
from config import ENV

# ============================================================
# مفتاح التشفير - Fail-Safe Security + Stable Encryption
# ============================================================

_secret = os.getenv("ENCRYPTION_SECRET")
if not _secret:
    if ENV == "prod":
        raise RuntimeError("ENCRYPTION_SECRET must be set in production environment")
    _secret = "docgen-dev-encryption-key-2026-not-for-prod"


def _get_fernet_key(secret_string):
    """
    تحويل سلسلة السر إلى مفتاح Fernet صالح (32 بايت base64)
    يستخدم SHA256 لاشتقاق مفتاح ثابت دائماً من نفس السر
    """
    digest = hashlib.sha256(secret_string.encode()).digest()
    key = base64.urlsafe_b64encode(digest)
    return key


# ============================================================
# SimpleEncryption - Fernet (AES-128-CBC + HMAC)
# ============================================================

class SimpleEncryption:
    def __init__(self, secret=None):
        if secret is None:
            secret = _secret
        self._fernet = Fernet(_get_fernet_key(secret))
        # مفتاح XOR القديم - للإستخدام في فك التشفير فقط (ترحيل)
        self._xor_key = hashlib.sha256(secret.encode()).digest()

    def encrypt(self, plaintext):
        """تشفير النص باستخدام Fernet"""
        if not plaintext:
            return ""
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """فك التشفير - يجرب Fernet أولاً ثم XOR للترحيل من البيانات القديمة"""
        if not ciphertext:
            return ""
        try:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        except Exception:
            return self._xor_decrypt(ciphertext)

    def _xor_decrypt(self, ciphertext):
        """فك تشفير XOR قديم - للترحيل فقط"""
        try:
            encrypted = base64.b64decode(ciphertext.encode('utf-8'))
            decrypted = self._xor(encrypted, self._xor_key)
            return decrypted.decode('utf-8')
        except Exception:
            return ""

    def _xor(self, data, key):
        return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

    def needs_reencryption(self, ciphertext):
        """هل البيانات مشفرة بـ XOR وتحتاج ترقية إلى Fernet؟"""
        if not ciphertext:
            return False
        try:
            self._fernet.decrypt(ciphertext.encode())
            return False
        except Exception:
            return True

    def reencrypt(self, ciphertext):
        """ترقية بيانات قديمة من XOR إلى Fernet"""
        plaintext = self.decrypt(ciphertext)
        if plaintext:
            return self.encrypt(plaintext)
        return ciphertext


# ============================================================
# KeyVault - مخزن مفاتيح آمن
# ============================================================

class KeyVault:
    def __init__(self, secret=None):
        self.cipher = SimpleEncryption(secret or _secret)
        self._keys = {}

    def store(self, name, value):
        """تخزين قيمة مشفرة بـ Fernet"""
        self._keys[name] = self.cipher.encrypt(value)

    def retrieve(self, name):
        """استرجاع وفك تشفير قيمة"""
        encrypted = self._keys.get(name, "")
        return self.cipher.decrypt(encrypted)

    def rotate_key(self, new_secret):
        """تدوير المفتاح - إعادة تشفير كل المخزن بمفتاح جديد"""
        new_cipher = SimpleEncryption(new_secret)
        for name, encrypted in list(self._keys.items()):
            plaintext = self.cipher.decrypt(encrypted)
            if plaintext:
                self._keys[name] = new_cipher.encrypt(plaintext)
        self.cipher = new_cipher

    def upgrade_all(self):
        """ترقية كل البيانات المخزنة من XOR إلى Fernet"""
        for name, encrypted in list(self._keys.items()):
            if self.cipher.needs_reencryption(encrypted):
                self._keys[name] = self.cipher.reencrypt(encrypted)


# ============================================================
# دوال مساعدة
# ============================================================

def hash_data(data, salt=""):
    if salt:
        data = data + ":" + salt
    return hashlib.sha256(data.encode()).hexdigest()


def verify_hash(data, hash_value, salt=""):
    return hash_data(data, salt) == hash_value


def generate_token(length=32):
    return base64.b64encode(os.urandom(length)).decode('utf-8')[:length]


if __name__ == "__main__":
    print("Testing Encryption...")
    cipher = SimpleEncryption()
    original = "Hello World"
    encrypted = cipher.encrypt(original)
    decrypted = cipher.decrypt(encrypted)
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted[:40]}...")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {original == decrypted}")

    vault = KeyVault()
    vault.store("api_key", "test-secret-key-123")
    print(f"Vault OK: {vault.retrieve('api_key')}")
    
    token = generate_token(16)
    print(f"Token: {token}")
    print("Done")
