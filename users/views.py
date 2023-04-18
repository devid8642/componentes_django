from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import MyUser
from .serializers import MyUserSerializer
from .utils import data_user_validation

@api_view(['GET'])
def users(request):
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['POST'])
def users_create(request):
    data = request.data
    expected_data = ['username', 'email', 'password']
    validation = data_user_validation(data, expected_data)
    if validation != None:
        return Response({'detail': validation}, status = status.HTTP_400_BAD_REQUEST)
    user = MyUser.objects.create_user(
            username = request.data['username'],
            email = request.data['email'],
            password = request.data['password']
    )
    serializer = MyUserSerializer(user)
    return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
def users_detail(request, id):
    try:
        user = MyUser.objects.get(id = id)
    except MyUser.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MyUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        expected_data = ['username', 'email', 'password']
        validation = data_user_validation(data, expected_data)
        if validation != None:
            return Response({'detail': validation}, status = status.HTTP_400_BAD_REQUEST)
        user.username = data['username']
        user.email = data['email']
        user.password = make_password(data['password'])
        user.save()
        user = MyUser.objects.get(id = id)
        serializer = MyUserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
