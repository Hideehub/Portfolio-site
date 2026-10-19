from unittest import mock

import pytest
from django.core import mail
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import ContactMessage

pytestmark = pytest.mark.django_db

URL = reverse("contact:submit")
VALID = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "message": "Hello, I'd like to talk about a project.",
    "website": "",
}


@pytest.fixture
def email_on(settings):
    settings.MAILERS = {"default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"}}
    settings.CONTACT_RECIPIENT_EMAIL = "owner@example.com"


class TestContactForm:
    def test_valid(self):
        assert ContactForm(data=VALID).is_valid()

    @pytest.mark.parametrize(
        "field, value",
        [("name", "   "), ("email", "not-an-email"), ("message", "too short")],
    )
    def test_invalid_fields(self, field, value):
        form = ContactForm(data={**VALID, field: value})
        assert not form.is_valid()
        assert field in form.errors

    def test_required_fields(self):
        form = ContactForm(data={})
        assert not form.is_valid()
        assert set(form.errors) == {"name", "email", "message"}


class TestContactView:
    def test_valid_submission_saves_and_sends_email(self, client, email_on):
        response = client.post(URL, VALID)
        assert response.status_code == 302
        assert response["Location"] == "/#contact"
        saved = ContactMessage.objects.get()
        assert saved.email == "ada@example.com"
        assert not saved.is_read
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["owner@example.com"]
        assert mail.outbox[0].reply_to == ["ada@example.com"]

    def test_success_message_shown(self, client):
        response = client.post(URL, VALID, follow=True)
        assert b"Thanks for your message" in response.content

    def test_no_email_when_recipient_not_configured(self, client, email_on, settings):
        settings.CONTACT_RECIPIENT_EMAIL = ""
        client.post(URL, VALID)
        assert ContactMessage.objects.count() == 1
        assert mail.outbox == []

    def test_no_email_when_no_mailer_configured(self, client, email_on, settings):
        settings.MAILERS = {}
        client.post(URL, VALID)
        assert ContactMessage.objects.count() == 1
        assert mail.outbox == []

    def test_email_failure_still_saves(self, client, email_on, caplog):
        with mock.patch(
            "django.core.mail.backends.locmem.EmailBackend.send_messages", side_effect=OSError("SMTP down")
        ):
            response = client.post(URL, VALID)
        assert response.status_code == 302
        assert ContactMessage.objects.count() == 1
        assert "Failed to send contact notification" in caplog.text

    def test_invalid_submission_shows_errors(self, client, email_on):
        response = client.post(URL, {**VALID, "email": "nope"})
        assert response.status_code == 400
        assert b'aria-invalid="true"' in response.content
        assert ContactMessage.objects.count() == 0
        assert mail.outbox == []

    def test_honeypot_discards_silently(self, client, email_on):
        response = client.post(URL, {**VALID, "website": "http://spam.example"})
        assert response.status_code == 302
        assert ContactMessage.objects.count() == 0
        assert mail.outbox == []

    def test_rate_limit_per_ip(self, client, settings):
        settings.CONTACT_RATE_LIMIT = 3
        for _ in range(3):
            assert client.post(URL, VALID, REMOTE_ADDR="10.0.0.1").status_code == 302
        response = client.post(URL, VALID, REMOTE_ADDR="10.0.0.1")
        assert response.status_code == 429
        assert b"try again later" in response.content
        assert ContactMessage.objects.count() == 3
        # A different IP is unaffected.
        assert client.post(URL, VALID, REMOTE_ADDR="10.0.0.2").status_code == 302

    def test_rate_limit_uses_forwarded_ip(self, client, settings):
        settings.CONTACT_RATE_LIMIT = 1
        client.post(URL, VALID, HTTP_X_FORWARDED_FOR="203.0.113.5, 10.0.0.9")
        response = client.post(URL, VALID, HTTP_X_FORWARDED_FOR="203.0.113.5, 10.0.0.9")
        assert response.status_code == 429

    def test_get_redirects_to_contact_section(self, client):
        response = client.get(URL)
        assert response.status_code == 302
        assert response["Location"] == "/#contact"
