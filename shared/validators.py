from django.core.exceptions import ValidationError
import re


def phone_validator(value):
    """
    Validates a phone number.

    The phone number must be a 10-digit number without any special characters.
    """
    # Define the regular expression for a valid phone number (10 digits).
    phone_pattern = re.compile(r"^\d{10}$")

    # If the value does not match the regular expression, raise ValidationError.
    if not phone_pattern.match(value):
        raise ValidationError(
            "El número telefónico debe tener exactamente 10 dígitos.",
            params={"value": value},
        )


def cp_validator(value):
    """
    Validates a Mexican postal code (Código Postal).

    The postal code must be a 5-digit number.
    """
    # Ensure the postal code is exactly 5 digits.
    if not (isinstance(value, str) and value.isdigit() and len(value) == 5):
        raise ValidationError(
            "El código postal debe ser un número de 5 dígitos.",
            params={"value": value},
        )


def rfc_validator(value):
    """
    Validates a Mexican RFC.

    The RFC must follow the format rules for both personas físicas and personas morales.
    """
    # Define the regular expression for a valid RFC.
    rfc_pattern = re.compile(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$")

    # If the value does not match the regular expression, raise ValidationError.
    if not rfc_pattern.match(value):
        raise ValidationError(
            "El RFC debe tener un formato válido. Ejemplo: ABCD123456XYZ para personas físicas o ABC123456XYZ para personas morales.",
            params={"value": value},
        )
