import pytest
from collections import OrderedDict
from users.models import MyUser
from users.serializers import MyUserSerializer
from users.utils import setup_db, date_format

@pytest.mark.django_db
class TestUserSerializer:
    def test_serializer_an_instance(self, setup_db):
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
    
    def test_serializer_multiple_instances(self, setup_db):
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
class TestUserSerializerCreateAndUpdate:
    pass