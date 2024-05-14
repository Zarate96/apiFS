import googlemaps
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from shared.constants import constants
from rest_framework import serializers
from .schemas.responses import custom_response

gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)


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


def validate_address(address) -> str:
    """
    Validate the given address using Google Maps API.
    """
    geocode_result = gmaps.geocode(address)
    try:
        direccion_google = geocode_result[0]["formatted_address"]
        if len(geocode_result) == 0 or len(direccion_google) < 50:
            raise serializers.ValidationError(f"The address {address} is not valid")
        return direccion_google
    except Exception as e:
        raise serializers.ValidationError(str(e))
