# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt = {
            reverse("accounts:signin"),
            reverse("accounts:signup"),
            reverse("accounts:password_reset"),
            reverse("accounts:password_reset_done"),
            reverse("accounts:password_reset_complete"),
        }

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and request.path_info not in self.exempt
            and not request.path_info.startswith("/admin/")
        ):
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
