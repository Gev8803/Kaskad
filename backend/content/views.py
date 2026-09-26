"""API views: consolidated content feed + contact-form intake."""
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactMessageSerializer, build_content


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
        serializer.save()
        return Response(
            {"ok": True, "message": "received"}, status=status.HTTP_201_CREATED
        )
