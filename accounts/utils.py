from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from shared.constants import constants


class EmailHandler:
    @staticmethod
    def send_email(user, request, subject_template, body_template):
        try:
            current_site = get_current_site(request)
            email_subject = subject_template.format(site=current_site)
            email_body = render_to_string(
                body_template,
                {
                    "user": user,
                    "domain": current_site.domain,
                    "protocol": constants.PROTOCOL,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": PasswordResetTokenGenerator().make_token(user),
                },
            )
            if not settings.TESTING:
                send_mail(
                    subject=email_subject,
                    message="",
                    from_email=settings.EMAIL_FROM_USER,
                    recipient_list=[user.email],
                    html_message=email_body,
                )
        except Exception as e:
            raise e


def send_activation_email(user, request):
    """
    Send activation email to user.
    """
    EmailHandler.send_email(
        user, request, "Activa tu cuenta en Flete Seguro", "accounts/mails/active.html"
    )


def send_reset_email(user, request):
    """
    Send reset email to user.
    """
    EmailHandler.send_email(
        user,
        request,
        "Reinicia tu contraseña de Flete Seguro",
        "accounts/mails/reset-password.html",
    )
