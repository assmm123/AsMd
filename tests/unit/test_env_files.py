"""اختبار ملفات البيئة - المنطق الحقيقي"""

import os
from pathlib import Path


@pytest.fixture
def test_setup():
    """Auto-generated fixture"""
    # TODO: add proper setup
    yield
    # TODO: add proper teardown

BASE_DIR = Path(__file__).parent.parent.parent


class TestEnvExample:
    """اختبارات .env.example"""

    def test_file_exists(self):
        """الملف موجود"""
        assert os.path.exists(BASE_DIR / '.env.example')

    def test_contains_jwt_secret(self):
        """يحتوي على JWT_SECRET"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'JWT_SECRET' in content

    def test_contains_mail_username(self):
        """يحتوي على MAIL_USERNAME"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'MAIL_USERNAME' in content

    def test_contains_mail_password(self):
        """يحتوي على MAIL_PASSWORD"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'MAIL_PASSWORD' in content

    def test_contains_encryption_secret(self):
        """يحتوي على ENCRYPTION_SECRET"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'ENCRYPTION_SECRET' in content

    def test_contains_docgen_env(self):
        """يحتوي على DOCGEN_ENV"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'DOCGEN_ENV' in content

    def test_no_real_values(self):
        """لا يحتوي على قيم حقيقية"""
        content = open(BASE_DIR / '.env.example').read()
        assert 'your-email@gmail.com' in content or 'change-this' in content


class TestGitignore:
    """اختبارات .gitignore"""

    def test_file_exists(self):
        """الملف موجود"""
        assert os.path.exists(BASE_DIR / '.gitignore')

    def test_ignores_env(self):
        """يتجاهل .env"""
        content = open(BASE_DIR / '.gitignore').read()
        assert '.env' in content

    def test_ignores_users_json(self):
        """يتجاهل users.json"""
        content = open(BASE_DIR / '.gitignore').read()
        assert 'users.json' in content

    def test_ignores_logs(self):
        """يتجاهل مجلد logs"""
        content = open(BASE_DIR / '.gitignore').read()
        assert 'logs/' in content

    def test_ignores_backups(self):
        """يتجاهل مجلد backups"""
        content = open(BASE_DIR / '.gitignore').read()
        assert 'backups/' in content

    def test_ignores_data(self):
        """يتجاهل مجلد data"""
        content = open(BASE_DIR / '.gitignore').read()
        assert 'data/' in content

    def test_ignores_pycache(self):
        """يتجاهل __pycache__"""
        content = open(BASE_DIR / '.gitignore').read()
        assert '__pycache__' in content
