"""Fixtures مشتركة للاختبارات"""
import pytest
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app as flask_app


@pytest.fixture
def app():
    """تطبيق Flask للاختبار"""
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Flask test client"""
    return app.test_client()
