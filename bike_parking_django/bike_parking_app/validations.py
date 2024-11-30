from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model() 

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    phone_number = data['phone_number'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('choose another email')
    
    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 character')
    
    if not username:
        raise ValidationError('choose another username')
    
    if phone_number:  
        if len(phone_number) < 10:
            raise ValidationError('Invalid phone number, must be at least 10 digits and located in the U.S.')
    return data

def validate_email(data):
    email = data['credentials'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['credentials'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_phone_number(data):
    phone_number = data['credentials'].strip()
    if not phone_number:
        raise ValidationError('choose another phone number')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True