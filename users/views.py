from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import MyUser
from .serializers import MyUserSerializer

@api_view(['GET'])
def users(request):
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def users_create(request):
    data = request.data
    expected_data = ['username', 'email', 'password']
    
    for i in expected_data:
        if i not in data.keys():
            return Response({'detail': 'expected data: username, email and password'}, status = status.HTTP_400_BAD_REQUEST)
    del expected_data

    try:
        validate_email(data['email'])
        validate_password(password = data['password'])
    except ValidationError as e:
        return Response({'detail': e}, status = status.HTTP_400_BAD_REQUEST)

    user = MyUser.objects.create_user(
            username = request.data['username'],
            email = request.data['email'],
            password = request.data['password']
    )
    serializer = MyUserSerializer(user)
    return Response(serializer.data, status = status.HTTP_201_CREATED)
