import pytest
from users.models import MyUser
from django.utils import timezone
from django.contrib.auth.hashers import check_password

@pytest.mark.django_db
class TestUserModel:
    def test_user_create(self):
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
        assert user.date_joined.date() == timezone.now().date()
        assert check_password(password = 'devid3939!', encoded = user.password) == True

    def test_superuser_create(self):
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
        assert user.date_joined.date() == timezone.now().date()
        assert check_password(password = 'asuna333@@', encoded = user.password) == True
