"""اختبار jwt.py - المنطق الحقيقي"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.auth.jwt import create_token, verify_token


class TestCreateToken:
    """اختبارات إنشاء التوكن"""

    def test_returns_string(self):
        """create_token يرجع string"""
        token = create_token('user123')
        assert isinstance(token, str)

    def test_contains_two_dots(self):
        """JWT يحتوي على نقطتين فاصلتين"""
        token = create_token('user123')
        parts = token.split('.')
        assert len(parts) == 3

    def test_different_users_different_tokens(self):
        """مستخدمين مختلفين = توكنات مختلفة"""
        t1 = create_token('user1')
        t2 = create_token('user2')
        assert t1 != t2


class TestVerifyToken:
    """اختبارات فك التوكن"""

    def test_returns_dict(self):
        """verify_token يرجع dict"""
        token = create_token('user123')
        payload = verify_token(token)
        assert isinstance(payload, dict)

    def test_contains_required_fields(self):
        """الـ payload يحتوي على الحقول المطلوبة"""
        token = create_token('user123')
        payload = verify_token(token)
        assert 'user_id' in payload
        assert 'role' in payload
        assert 'iat' in payload
        assert 'exp' in payload

    def test_user_id_match(self):
        """user_id في payload يطابق المدخل"""
        token = create_token('user123')
        payload = verify_token(token)
        assert payload['user_id'] == 'user123'

    def test_default_role_is_user(self):
        """الدور الافتراضي user"""
        token = create_token('user123')
        payload = verify_token(token)
        assert payload['role'] == 'user'

    def test_admin_role(self):
        """دور admin يشتغل"""
        token = create_token('admin1', role='admin')
        payload = verify_token(token)
        assert payload['role'] == 'admin'

    def test_invalid_token_returns_none(self):
        """توكن غير صالح يرجع None"""
        assert verify_token('invalid.token.here') is None

    def test_empty_token_returns_none(self):
        """توكن فارغ يرجع None"""
        assert verify_token('') is None

    def test_none_token_returns_none(self):
        """None يرجع None"""
        assert verify_token(None) is None
