from pytest import fixture
from zoneinfo import ZoneInfo
from users.models import MyUser
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
            return 'Email inválido'
        elif len(data['username']) > 255:
            return 'Usuário Inválido'
    
    return None

def date_format(date):
    return date.astimezone(ZoneInfo('America/Sao_Paulo')).isoformat()

@fixture
def setup_db(scope = 'class'):
    MyUser.objects.create_user(
        username = 'devid',
        email = 'devid@devid.com',
        password = 'devid3939!'
    )
    MyUser.objects.create_user(
        username = 'teste',
        email = 'teste@teste.com',
        password = 'teste3939!'
    )
    MyUser.objects.create_superuser(
        username = 'admin',
        email = 'admin@admin.com',
        password = 'asuna333@@'
    )
