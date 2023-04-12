from rest_framework.serializers import ModelSerializer
from .models import MyUser

class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'password', 'is_active', 'is_staff', 'data_joined']
    