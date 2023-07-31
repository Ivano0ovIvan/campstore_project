from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator


def validate_positive_number(value):
    if value <= 0:
        raise ValidationError('Value must be a positive number.')


def validate_name(value):
    if not value.replace(' ', '').replace('-', '').isalpha():
        raise ValidationError("Name can only contain alphabetic characters, spaces, and hyphens.")


def validate_name_length(value, min_length=2, max_length=50):
    if len(value) < min_length or len(value) > max_length:
        raise ValidationError(f"Name must be between {min_length} and {max_length} characters long.")


def validate_phone_number(value):
    phone_number = ''.join(filter(lambda char: char.isdigit() or char == '+', value))

    if phone_number != value:
        raise ValidationError("Phone number can only contain digits and '+'.")

    if not 9 <= len(phone_number) <= 15:
        raise ValidationError("Please enter a valid phone number.")