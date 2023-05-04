import pytest
from users.utils import setup_db
from users.models import MyUser
from users.serializers import MyUserSerializer
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

@pytest.mark.django_db
class TestUserListView:
    def test_from_staff_user(self, client, setup_db):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many = True)
        url = reverse('users')
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)

    def test_from_common_user(self, client, setup_db):
        url = reverse('users')
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.get(url)
        assert response.status_code == 403
        assert response.content == JSONRenderer().render({'detail': 'Você não tem permissão para executar essa ação.'})

    def test_from_anonymous_user(self, client, setup_db):
        url = reverse('users')
        response = client.get(url)
        assert response.status_code == 403
        assert response.content == JSONRenderer().render({'detail': 'As credenciais de autenticação não foram fornecidas.'})

@pytest.mark.django_db
class TestUserCreateView:
    def test_create_view(self, client):
        url = reverse('users_register')
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
    
    def test_view_when_exist_user(self, client, setup_db):
        url = reverse('users_register')
        response = client.post(url, {
            'username': 'devid',
            'email': 'devid@devid.com',
            'password': 'devid3939!'
        })
        assert response.status_code == 400
        assert response.content == JSONRenderer().render({'non_field_errors': ['O usuário já existe.']})

@pytest.mark.django_db
class TestGetUserDetailView:
    def test_from_staff_user(self, client, setup_db):
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        url = reverse('users_detail', args = [1])
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)
    
    def test_from_common_user_same_id(self, client, setup_db):
        user = MyUser.objects.get(id = 1)
        serializer = MyUserSerializer(user)
        url = reverse('users_detail', args = [1])
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.get(url)
        assert response.status_code == 200
        assert response.content == JSONRenderer().render(serializer.data)
    
    def test_from_common_user_different_id(self, client, setup_db):
        url = reverse('users_detail', args = [1])
        client.login(email = 'teste@teste.com', password = 'teste3939!')
        response = client.get(url)
        assert response.status_code == 403
        assert response.content == JSONRenderer().render({'detail': 'Você não tem permissões para acessar os dados de outro usuário.'})

@pytest.mark.django_db
class TestPostUserDetailView:
    def test_from_staff_user(self, client, setup_db):
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

    def test_from_common_user_same_id(self, client, setup_db):
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

    def test_from_common_user_different_id(self, client, setup_db):
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
        assert response.content == JSONRenderer().render({'detail': 'Você não tem permissões para acessar os dados de outro usuário.'})

@pytest.mark.django_db
class TestDeleteUserDetailView:
    def test_from_staff_user(self, client, setup_db):
        url = reverse('users_detail', args = [1])
        client.login(email = 'admin@admin.com', password = 'asuna333@@')
        response = client.delete(url)
        assert response.status_code == 204
        assert MyUser.objects.all().count() == 2

    def test_from_common_user_same_id(self, client, setup_db):
        url = reverse('users_detail', args = [1])
        client.login(email = 'devid@devid.com', password = 'devid3939!')
        response = client.delete(url)
        assert response.status_code == 204
        assert MyUser.objects.all().count() == 2

    def test_from_common_user_different_id(self, client, setup_db):
        url = reverse('users_detail', args = [1])
        client.login(email = 'teste@teste.com', password = 'teste3939!')
        response = client.delete(url)
        assert response.status_code == 403
        assert MyUser.objects.all().count() == 3
        assert response.content == JSONRenderer().render({'detail': 'Você não tem permissões para acessar os dados de outro usuário.'})
