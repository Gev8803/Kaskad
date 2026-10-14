"""API views: consolidated content feed + contact-form intake."""
import logging
import smtplib

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteSettings
from .serializers import ContactMessageSerializer, build_content

logger = logging.getLogger(__name__)


class ContentView(APIView):
    """GET /api/content/ -> the whole website content bundle (public, read-only)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # public endpoint; avoid session/CSRF coupling

    def get(self, request):
        data = build_content(request)
        resp = Response(data)
        # No caching: admin edits must appear on the next page reload.
        resp["Cache-Control"] = "no-cache, no-store, must-revalidate"
        resp["Pragma"] = "no-cache"
        resp["Expires"] = "0"
        return resp


class ContactCreateView(CreateAPIView):
    """POST /api/contact/ -> store a contact-form submission (public, throttled)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # public form; no session/CSRF requirement
    serializer_class = ContactMessageSerializer
    throttle_scope = "contact"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        recipient = SiteSettings.load().email
        notification_sent = False
        if settings.EMAIL_HOST and settings.DEFAULT_FROM_EMAIL and recipient:
            subject = message.subject.strip() or "New website contact message"
            subject = subject.replace("\r", " ").replace("\n", " ")
            body = "\n".join((
                f"Name: {message.name}",
                f"Email: {message.email or 'Not provided'}",
                f"Phone: {message.phone or 'Not provided'}",
                f"Subject: {message.subject or 'Not provided'}",
                "",
                message.message,
            ))
            try:
                EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    reply_to=[message.email] if message.email else None,
                ).send(fail_silently=False)
                notification_sent = True
            except (OSError, smtplib.SMTPException):
                logger.exception(
                    "Contact message %s was saved, but its email notification failed.",
                    message.pk,
                )
        return Response(
            {
                "ok": True,
                "message": "received",
                "email_notification_sent": notification_sent,
            },
            status=status.HTTP_201_CREATED,
        )
