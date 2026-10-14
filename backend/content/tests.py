from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import ContactMessage, SiteSettings


class ContactFormTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        SiteSettings.objects.create(email="contact@example.com")
        self.payload = {
            "name": "Test Visitor",
            "email": "visitor@example.net",
            "phone": "",
            "subject": "Question",
            "message": "Please contact me.",
        }

    @override_settings(EMAIL_HOST="smtp.example.com", DEFAULT_FROM_EMAIL="site@example.com")
    @patch("content.views.EmailMessage")
    def test_submission_is_saved_and_notifies_site_email(self, email_message):
        email_message.return_value.send.return_value = 1
        response = self.client.post("/api/contact/", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["ok"])
        self.assertTrue(response.data["email_notification_sent"])
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(email_message.call_args.args[3], ["contact@example.com"])
        self.assertEqual(email_message.call_args.kwargs["reply_to"], ["visitor@example.net"])
        email_message.return_value.send.assert_called_once_with(fail_silently=False)

    @override_settings(EMAIL_HOST="", DEFAULT_FROM_EMAIL="")
    def test_submission_is_saved_when_email_is_not_configured(self):
        response = self.client.post("/api/contact/", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["ok"])
        self.assertFalse(response.data["email_notification_sent"])
        self.assertEqual(ContactMessage.objects.count(), 1)

    @override_settings(EMAIL_HOST="smtp.example.com", DEFAULT_FROM_EMAIL="site@example.com")
    @patch("content.views.EmailMessage")
    def test_email_failure_does_not_discard_submission(self, email_message):
        email_message.return_value.send.side_effect = OSError("SMTP unavailable")
        with self.assertLogs("content.views", level="ERROR"):
            response = self.client.post("/api/contact/", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["ok"])
        self.assertFalse(response.data["email_notification_sent"])
        self.assertEqual(ContactMessage.objects.count(), 1)
