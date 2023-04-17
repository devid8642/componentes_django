import pytest
from .models import MyUser
from .serializers import MyUserSerializer
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.urls import reverse
from rest_framework.renderers import JSONRenderer


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
    assert user.date_joined.date() == timezone.now().date()
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
    assert user.date_joined.date() == timezone.now().date()
    assert check_password(password = 'asuna333@@', encoded = user.password) == True

@pytest.mark.django_db
def test_users_list(client):
    MyUser.objects.create_user(
        username = 'devid',
        email = 'devid@devid.com',
        password = 'devid3939!'
    )
    MyUser.objects.create_superuser(
        username = 'admin',
        email = 'admin@admin.com',
        password = 'asuna333@@'
    )
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many = True)
    url = reverse('users')
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == JSONRenderer().render(serializer.data)

@pytest.mark.django_db
def test_user_create(client):
    url = reverse('users_create')
    response = client.post(url, {
        'username': 'devid',
        'email': 'devid@devid.com',
        'password': 'devid3939!'
    })
    assert response.status_code == 201
    user = MyUser.objects.get(email = 'devid@devid.com')
    serializer = MyUserSerializer(user)
    expected_response = JSONRenderer().render(serializer.data)
    assert response.content == expected_response

@pytest.mark.django_db
def test_user_detail_get():
    pass

@pytest.mark.django_db
def test_user_detail_put():
    pass

@pytest.mark.django_db
def test_user_detail_delete():
    pass
