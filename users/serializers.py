from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import MyUser

class MyUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 255)
    email = serializers.EmailField(max_length = 255)
    password = serializers.CharField(validators = [validate_password])
    is_active = serializers.BooleanField(default = True)
    is_staff = serializers.BooleanField(default = False)
    date_joined = serializers.DateTimeField(default = timezone.now, read_only = True)

    def validate(self, data):
        try:
            MyUser.objects.get(email = data['email'])
        except MyUser.DoesNotExist:
            return data
        else:
            raise serializers.ValidationError('O usuário já existe')

    def create(self, validated_data):
        return MyUser.objects.create_user(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            password = validated_data.get('password')
        )

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.password = make_password(validated_data['password'])
        instance.is_active = validated_data['is_active']
        instance.is_staff = validated_data['is_staff']
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label = 'Email', max_length = 255, write_only = True)
    password = serializers.CharField(label = 'Password', write_only = True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        if email and password:
            user = authenticate(
                request = self.context.get('request'),
                email = email,
                password = password
            )
            if not user:
                msg = 'Email ou senha incorretos.'
                raise serializers.ValidationError(msg, code = 'authorization')
        else:
            msg = 'Email e senha são requeridos.'
            raise serializers.ValidationError(msg, code = 'authorization')
        attrs['user'] = user
        return attrs
