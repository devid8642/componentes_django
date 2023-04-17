from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

def data_user_validation(data, expected_data):
    for i in expected_data:
        if i not in data.keys():
            return f'expected data: {expected_data}'
    del expected_data

    try:
        validate_email(data['email'])
        validate_password(password = data['password'])
    except ValidationError as e:
        return e
    else:
        if len(data['email']) > 255:
            return 'Email invalid'
        elif len(data['username']) > 255:
            return 'Username invalid'
    
    return None