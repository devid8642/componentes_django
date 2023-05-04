from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import MyUser
from .serializers import MyUserSerializer, LoginSerializer
from .utils import data_user_validation

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAdminUser])
def users(request):
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([AllowAny])
def users_create(request):
    data = request.data
    serializer = MyUserSerializer(data = data)
    serializer.is_valid(raise_exception = True)
    user = serializer.save()
    serializer = MyUserSerializer(user)
    return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def users_detail(request, id):
    if request.user.is_staff or request.user.id == id:
        try:
            user = MyUser.objects.get(id = id)
        except MyUser.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = MyUserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data
            serializer = MyUserSerializer(user, data = data)
            serializer.is_valid(raise_exception = True)
            user = serializer.save()
            serializer = MyUserSerializer(user)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
    else:
        return Response({'detail': 'Você não tem permissões para acessar os dados de outro usuário.'}, status = status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([AllowAny])
def loginn(request):
    serializer = LoginSerializer(
        data = request.data,
        context = {'request': request}
    )
    serializer.is_valid(raise_exception = True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(None, status = status.HTTP_202_ACCEPTED)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def logoutt(request):
    logout(request)
    return Response(None, status = status.HTTP_204_NO_CONTENT)