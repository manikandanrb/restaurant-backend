from django.conf import settings
from django.shortcuts import render
from rest_framework import response, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views
from rest_framework.decorators import api_view
from users.models import User
from users.serializers import AuthenticationSerializer, SignupSerializer, UserProfileSerializer


@api_view(['POST'])
def signup(request):
    data = request.data.copy()
    signup_serializer = SignupSerializer(data=data, context={'request': request})
    signup_serializer.is_valid(raise_exception=True)
    signup_serializer.save()
    return response.Response(status=status.HTTP_200_OK, data={'message': 'Success'})
    

@api_view(['POST'])
def login(request):
    data = request.data.copy()
    login_serializer = AuthenticationSerializer(data=data, context={'request': request})
    login_serializer.is_valid(raise_exception=True)
    user = login_serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    data = {
        'token': token.key
    }
    return response.Response(status=status.HTTP_200_OK, data=data)


@api_view(['POST'])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = None

    if token:
        token.delete()
    return response.Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def profile(request):
    user = request.user
    if request.method == 'GET':
        profile_data = UserProfileSerializer(instance=user).data
        return response.Response(status=status.HTTP_200_OK, data=profile_data)