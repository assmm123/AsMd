"""اختبار encryption.py - المنطق الحقيقي"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.security.encryption import SimpleEncryption, KeyVault, hash_data, verify_hash, generate_token


class TestSimpleEncryption:
    """اختبارات التشفير"""

    def test_encrypt_returns_string(self):
        """encrypt يرجع string"""
        s = SimpleEncryption()
        result = s.encrypt("hello")
        assert isinstance(result, str)

    def test_encrypt_different_from_plaintext(self):
        """الناتج المشفر يختلف عن النص الأصلي"""
        s = SimpleEncryption()
        encrypted = s.encrypt("hello")
        assert encrypted != "hello"

    def test_decrypt_reverses_encrypt(self):
        """فك التشفير يرجع النص الأصلي"""
        s = SimpleEncryption()
        original = "Hello World 123"
        encrypted = s.encrypt(original)
        decrypted = s.decrypt(encrypted)
        assert decrypted == original

    def test_empty_string(self):
        """نص فارغ يرجع نص فارغ"""
        s = SimpleEncryption()
        assert s.encrypt("") == ""
        assert s.decrypt("") == ""

    def test_arabic_text(self):
        """نص عربي يشتغل"""
        s = SimpleEncryption()
        original = "مرحبا بالعالم"
        encrypted = s.encrypt(original)
        decrypted = s.decrypt(encrypted)
        assert decrypted == original

    def test_different_secrets_different_results(self):
        """مفاتيح مختلفة تعطي نتائج مختلفة"""
        s1 = SimpleEncryption("secret1")
        s2 = SimpleEncryption("secret2")
        encrypted = s1.encrypt("hello")
        assert s2.decrypt(encrypted) != "hello"


class TestKeyVault:
    """اختبارات مخزن المفاتيح"""

    def test_store_and_retrieve(self):
        """تخزين واسترجاع"""
        vault = KeyVault()
        vault.store("test_key", "test_value")
        assert vault.retrieve("test_key") == "test_value"

    def test_retrieve_nonexistent(self):
        """استرجاع مفتاح غير موجود يرجع نص فارغ"""
        vault = KeyVault()
        result = vault.retrieve("does_not_exist")
        assert result == ""


class TestHashFunctions:
    """اختبارات التجزئة"""

    def test_hash_returns_string(self):
        """hash_data يرجع string"""
        result = hash_data("hello")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_same_input_same_hash(self):
        """نفس المدخل = نفس التجزئة"""
        h1 = hash_data("hello")
        h2 = hash_data("hello")
        assert h1 == h2

    def test_different_input_different_hash(self):
        """مدخل مختلف = تجزئة مختلفة"""
        h1 = hash_data("hello")
        h2 = hash_data("world")
        assert h1 != h2

    def test_verify_hash(self):
        """verify_hash يتحقق بشكل صحيح"""
        data = "test_data"
        h = hash_data(data)
        assert verify_hash(data, h) == True
        assert verify_hash("wrong", h) == False

    def test_hash_with_salt(self):
        """تجزئة مع salt تختلف عن بدون salt"""
        h1 = hash_data("hello")
        h2 = hash_data("hello", salt="mysalt")
        assert h1 != h2


class TestGenerateToken:
    """اختبارات توليد التوكن"""

    def test_returns_string(self):
        """generate_token يرجع string"""
        token = generate_token()
        assert isinstance(token, str)

    def test_default_length(self):
        """الطول الافتراضي 32"""
        token = generate_token()
        assert len(token) == 32

    def test_custom_length(self):
        """طول مخصص"""
        token = generate_token(16)
        assert len(token) == 16

    def test_different_tokens(self):
        """كل مرة توكن مختلف"""
        t1 = generate_token()
        t2 = generate_token()
        assert t1 != t2
