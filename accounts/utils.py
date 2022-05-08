import django
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as mail_valid


def validate_email(value: str):
    """Validate a single email"""
    message_invalid = "Enter a valid email"

    if not value:
        return False, message_invalid

    # Validate regex using validate_email from django
    try:
        mail_valid(value)
    except ValidationError:
        return False, message_invalid

    return True, ""
