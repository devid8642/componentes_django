import pytest
from .models import MyUser
from .serializers import MyUserSerializer
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

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

@pytest.mark.django_db
class TestUserListView:
    def test_from_staff_user(self, client):
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
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)

    def test_from_common_user(self, client):
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
        url = reverse('users')
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.get(url)
        assert response.status_code == 403

@pytest.mark.django_db
class TestUserCreateView:
    def test_create_view(self, client):
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
class TestGetUserDetailView:
    def test_from_staff_user(self, client):
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
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        url = reverse('users_detail', args = [1])
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)
    
    def test_from_common_user_same_id(self, client):
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
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        url = reverse('users_detail', args = [1])
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)
    
    def test_from_common_user_different_id(self, client):
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
        url = reverse('users_detail', args = [1])
        client.login(email = 'teste@teste.com', password = 'teste3939!')
        response = client.get(url)
        assert response.status_code == 403

@pytest.mark.django_db
class TestPostUserDetailView:
    def test_from_staff_user(self, client):
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
        url = reverse('users_detail', args = [1])
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.post(url, {
            'username': 'roberto',
            'email': 'roberto@gmail.com',
            'password': 'robertoda8721!@'
        })
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)

    def test_from_common_user_same_id(self, client):
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
        url = reverse('users_detail', args = [1])
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.post(url, {
            'username': 'roberto',
            'email': 'roberto@gmail.com',
            'password': 'robertoda8721!@'
        })
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)

    def test_from_common_user_different_id(self, client):
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
        MyUser.objects.create_user(
            username = 'teste',
            email = 'teste@teste.com',
            password = 'teste3939!'
        )
        url = reverse('users_detail', args = [1])
        client.login(email = 'teste@teste.com', password = 'teste3939!')
        pre_user = MyUser.objects.get(id = 1)
        response = client.post(url, {
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': 'teste3939!'
        })
        pos_user = MyUser.objects.get(id = 1)
        assert response.status_code == 403
        assert pre_user == pos_user

@pytest.mark.django_db
class TestDeleteUserDetailView:
    def test_from_staff_user(self, client):
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
        url = reverse('users_detail', args = [1])
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.delete(url)
        assert response.status_code == 204
        assert MyUser.objects.all().count() == 1

    def test_from_common_user_same_id(self, client):
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
        url = reverse('users_detail', args = [1])
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.delete(url)
        assert response.status_code == 204
        assert MyUser.objects.all().count() == 1

    def test_from_common_user_different_id(self, client):
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
        MyUser.objects.create_user(
            username = 'teste',
            email = 'teste@teste.com',
            password = 'teste3939!'
        )
        url = reverse('users_detail', args = [1])
        client.login(email = 'teste@teste.com', password = 'teste3939!')
        response = client.delete(url)
        assert response.status_code == 403
        assert MyUser.objects.all().count() == 3
