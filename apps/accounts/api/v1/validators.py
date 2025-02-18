# Rest Framework imports
from rest_framework.serializers import ValidationError

# Standard imports
import re

"""
Field validation methods for serializers
"""
def validate_email(value):
    """
    Validate the email using regular expression
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError("INVALID_EMAIL")
    return value


def custom_validate_password(value):
    """
    Validate the password using regular expressions:
    - Password should be at least 12 characters long and at most 128 characters
    - Password should not contain any spaces
    - Password should contain at least one uppercase letter and one digit and one special character
    """
    if len(value) < 12 or len(value) > 128:
        raise ValidationError("INVALID_PASSWORD")
    if " " in value:
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[0-9]", value):
        raise ValidationError("INVALID_PASSWORD")
    if not re.search(r"[!@#$%^&*()_+{}|:<>?]", value):
        raise ValidationError("INVALID_PASSWORD")
    return value

def validate_username(value):
    """
    Validate the username, it should not contain any special characters or digits
    should not be empty or more than 50 characters
    """
    if value:
        if len(value) > 50 or len(value) == 0:
            raise ValidationError("INVALID_USERNAME")
        if not re.match(r"^[a-zA-Z_]*$", value):
            raise ValidationError("INVALID_USERNAME")
    return value