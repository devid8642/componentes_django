import pytest
from collections import OrderedDict
from users.models import MyUser
from users.serializers import MyUserSerializer
from users.utils import setup_db, date_format

@pytest.mark.django_db
class TestUserSerializing:
    def test_with_an_instance(self, setup_db):
        user = MyUser.objects.get(id = 1)
        expected_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': date_format(user.date_joined)
        }
        serializer = MyUserSerializer(user)
        assert serializer.data == expected_dict
    
    def test_with_multiple_instances(self, setup_db):
        users = MyUser.objects.all()
        expected_list = []
        expected_atributes = [
            'id',
            'username',
            'email',
            'password',
            'is_active',
            'is_staff',
            'date_joined'
        ]
        for user in users:
            user_list_atributes = []
            for atribute in expected_atributes:
                if atribute == 'date_joined':
                    date = date_format(user.__dict__[atribute])
                    user_list_atributes.append((f'{atribute}', date))
                else:
                    user_list_atributes.append((f'{atribute}', user.__dict__[atribute]))
            expected_list.append(OrderedDict(user_list_atributes))
        serializer = MyUserSerializer(users, many = True)
        assert serializer.data == expected_list



@pytest.mark.django_db
class TestUserDesrializing:
    def test_create(self):
        data = {
            'username': 'devid',
            'email': 'devid@devid.com',
            'password': 'devid3939!'
        }
        serializer = MyUserSerializer(data = data)
        assert serializer.is_valid() == True
        user = serializer.save()
        assert user == MyUser.objects.get(email = 'devid@devid.com')

    def test_update(self, setup_db):
        data = {
            'username': 'roberto',
            'email': 'roberto@roberto.com',
            'password': 'roberto3939!'
        }
        user = MyUser.objects.get(email = 'devid@devid.com')
        serializer = MyUserSerializer(user, data = data)
        assert serializer.is_valid() == True
        user = serializer.save()
        assert user == MyUser.objects.get(email = 'roberto@roberto.com')

    def test_validate(self, setup_db):
        '''
        possible_errors = [
            'Este campo é obrigatório.',
            'O usuário já existe.',
            'Insira um endereço de email válido.',
            'Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres.',
            'Esta senha é inteiramente numérica.'
        ]
        '''
        data1 = {}
        data2 = {
            'username': 'devid',
            'email': 'devid',
            'password': 'dd'
        }
        data3 = {
            'password': '12345678'
        }
        data4 = {
            'username': 'devid',
            'email': 'devid@devid.com',
            'password': 'devid3939!'
        }
        serializers = [
            MyUserSerializer(data = data1),
            MyUserSerializer(data = data2),
            MyUserSerializer(data = data3),
            MyUserSerializer(data = data4)
        ]
        for serializer in serializers:
            assert serializer.is_valid() == False
