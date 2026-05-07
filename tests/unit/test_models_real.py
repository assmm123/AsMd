"""اختبار models.py - المنطق الحقيقي"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

from src.auth.models import db, save_db, load_db, hash_password

class TestHashPassword:
    """اختبارات دالة تشفير كلمة المرور"""

    def test_hash_returns_string(self):
        """التشفير يرجع سلسلة نصية"""
        result = hash_password('test123')
        assert isinstance(result, str)

    def test_hash_contains_separator(self):
        """الناتج يحتوي على فاصل : بين salt و key"""
        result = hash_password('test123')
        assert ':' in result

    def test_hash_is_different_each_time(self):
        """كل مرة تشفير تعطي نتيجة مختلفة"""
        pw1 = hash_password('test123')
        pw2 = hash_password('test123')
        assert pw1 != pw2


class TestCreateUser:
    """اختبارات إنشاء مستخدم جديد"""

    def test_create_user_success(self):
        """إنشاء مستخدم بنجاح"""
        user = db.create_user('testuser', 'pass123', 'test@test.com')
        assert user is not None
        assert user['username'] == 'testuser'
        assert user['email'] == 'test@test.com'
        assert user['role'] == 'user'
        assert user['provider'] == 'email'
        # تنظيف
        del db.users['testuser']

    def test_create_duplicate_user_fails(self):
        """لا يمكن إنشاء مستخدم مكرر"""
        db.create_user('testuser2', 'pass123', 'test@test.com')
        dup = db.create_user('testuser2', 'x', 'x@x.com')
        assert dup is None
        # تنظيف
        del db.users['testuser2']

    def test_create_user_has_created_at(self):
        """المستخدم الجديد فيه تاريخ إنشاء"""
        user = db.create_user('testuser3', 'pass123', 'test@test.com')
        assert 'created_at' in user
        assert user['created_at'] is not None
        # تنظيف
        del db.users['testuser3']


class TestAuthenticate:
    """اختبارات المصادقة"""

    def test_authenticate_success(self):
        """مصادقة ناجحة"""
        db.create_user('authuser', 'mypassword', 'auth@test.com')
        result = db.authenticate('authuser', 'mypassword')
        assert result is not None
        assert result['username'] == 'authuser'
        # تنظيف
        del db.users['authuser']

    def test_authenticate_wrong_password(self):
        """كلمة مرور خاطئة ترجع None"""
        db.create_user('authuser2', 'correct', 'auth@test.com')
        result = db.authenticate('authuser2', 'wrong')
        assert result is None
        # تنظيف
        del db.users['authuser2']

    def test_authenticate_wrong_username(self):
        """اسم مستخدم غير موجود يرجع None"""
        result = db.authenticate('nonexistent', 'password')
        assert result is None


class TestGetUser:
    """اختبارات استرجاع المستخدم"""

    def test_get_user_exists(self):
        """استرجاع مستخدم موجود"""
        db.create_user('getuser', 'pass123', 'get@test.com')
        user = db.get_user('getuser')
        assert user is not None
        assert user['email'] == 'get@test.com'
        # تنظيف
        del db.users['getuser']

    def test_get_user_not_exists(self):
        """استرجاع مستخدم غير موجود يرجع None"""
        user = db.get_user('noone')
        assert user is None


class TestPersistence:
    """اختبارات الحفظ والاسترجاع"""

    def test_save_and_load(self):
        """حفظ ثم استرجاع البيانات"""
        db.create_user('saveuser', 'pass123', 'save@test.com')
        save_db()
        assert os.path.exists('data/users.json')

        # تحميل والتأكد
        load_db()
        user = db.get_user('saveuser')
        assert user is not None
        assert user['username'] == 'saveuser'
        # تنظيف
        del db.users['saveuser']
        save_db()


class TestGoogleUser:
    """اختبارات مستخدم Google"""

    def test_create_google_user(self):
        """إنشاء مستخدم عبر Google"""
        user = db.create_google_user('g123', 'google@test.com', 'Google User')
        assert user is not None
        assert user['provider'] == 'google'
        assert user['google_id'] == 'g123'
        assert user['password'] is None
        # تنظيف
        del db.users['google']
