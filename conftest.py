import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def test_settings(settings):
    # Tests run with DEBUG off, so switch off HTTPS redirects and use plain static
    # storage (the manifest only exists after collectstatic).
    settings.SECURE_SSL_REDIRECT = False
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    cache.clear()
    yield
    cache.clear()
