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


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for user activation.
    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


def send_activation_email(user, request):
    """
    Send activation email to user.
    """
    try:
        current_site = get_current_site(request)
        email_subject = "Activa tu cuenta en Flete Seguro"
        email_body = render_to_string(
            "accounts/mails/active.html",
            {
                "user": user,
                "domain": current_site.domain,
                "protocol": constants.PROTOCOL,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": TokenGenerator().make_token(user),
            },
        )
        if not settings.TESTING:
            try:
                send_mail(
                    subject=email_subject,
                    message="",
                    from_email=settings.EMAIL_FROM_USER,
                    recipient_list=[user.email],
                    html_message=email_body,
                )
            except Exception as e:
                raise e
    except Exception as e:
        raise e


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
