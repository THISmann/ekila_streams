import random
from typing import Dict

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ekilauth.user.models import EkilaUser


class MailManagement:
    @staticmethod
    def send_email(data: Dict[str, str]) -> None:
        subject: str = data["subject"]
        email: str = data["to_email"]
        user: EkilaUser = EkilaUser.objects.get(email=email)
        message = render_to_string(
            template_name="email/reset_password.html",
            context={
                "user": user,
                "link": data["link"],
                "email_for_reply": settings.EMAIL_FOR_REPLY,
            },
        )
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject=subject,
            message=message,
            from_email=email_from,
            recipient_list=[email],
            fail_silently=False,
            html_message=message,
        )

    @staticmethod
    def send_code_for_verification(email: str) -> None:
        subject: str = "[Code OTP] Verification de votre email"
        otp: int = random.randint(settings.MIN_VALUE, settings.MAX_VALUE)
        user: EkilaUser = EkilaUser.objects.get(email=email)
        message = render_to_string(
            template_name="email/verify_email.html",
            context={
                "user": user,
                "code": otp,
                "email_for_reply": settings.EMAIL_FOR_REPLY,
            },
        )
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject=subject,
            message=message,
            from_email=email_from,
            recipient_list=[email],
            fail_silently=False,
            html_message=message,
        )
        user.confirm_number = otp
        user.save()
