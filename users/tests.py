import pytest
from .models import MyUser
from django.contrib.auth.hashers import check_password


@pytest.mark.django_db
def test_user_create():
    MyUser.objects.create_user(
        username = 'devid',
        email = 'devid@devid.com',
        password = 'devid3939!'
    )
    user = MyUser.objects.get(email = 'devid@devid.com')
    assert user.username == 'devid'
    assert user.email == 'devid@devid.com'
    assert user.is_active == True
    assert user.is_staff == False
    assert check_password(password = 'devid3939!', encoded = user.password) == True 

@pytest.mark.django_db
def test_superuser_create():
    MyUser.objects.create_superuser(
        username = 'admin',
        email = 'admin@admin.com',
        password = 'asuna333@@'
    )
    user = MyUser.objects.get(email = 'admin@admin.com')
    assert user.username == 'admin'
    assert user.email == 'admin@admin.com'
    assert user.is_active == True
    assert user.is_staff == True
    assert check_password(password = 'asuna333@@', encoded = user.password) == True
