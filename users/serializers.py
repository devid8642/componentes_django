from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import MyUser

class MyUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 255)
    email = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 128)
    is_active = serializers.BooleanField(default = True)
    is_staff = serializers.BooleanField(default = False)
    date_joined = serializers.DateTimeField(default = timezone.now, read_only = True)

    def create(self, **validated_data):
        return MyUser.objects.create(**validated_data)

    def update(self, instance, **validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email ', instance.email)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance
