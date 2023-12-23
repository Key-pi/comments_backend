from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.mixins.locale import LocaleMixin
from api.mixins.mapping import SerializerMapper, PermissionsMapper
from api.serializers.auth import UserSerializer, AuthSerializer, RegisterSerializer, AuthResponseSerializer, \
    RefreshSerializer
from settings.swagger import SwaggerTags

User = get_user_model()


@extend_schema_view(
    register=extend_schema(
        description='Register', tags=[SwaggerTags.AUTH],
        summary='Register in service'
    ),
    login=extend_schema(
        description='Login', tags=[SwaggerTags.AUTH],
        summary='Sign in'
    ),
    logout=extend_schema(
        description='Logout endpoint', tags=[SwaggerTags.AUTH],
        summary='Logout endpoint'
    ),
    refresh=extend_schema(
        description='Tokens refresh endpoint', tags=[SwaggerTags.AUTH],
        summary='Tokens refresh endpoint'
    ),

)  # for swagger
class AuthViewSet(LocaleMixin, SerializerMapper, PermissionsMapper, viewsets.GenericViewSet):
    serializers = {
        'register': RegisterSerializer,
        'login': AuthSerializer,
        'logout': Serializer,
        'refresh': RefreshSerializer,
        'default': UserSerializer,
    }
    permissions_per_actions = {
        'default': [permissions.AllowAny()],
        'refresh': [permissions.IsAuthenticated()],
    }

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response_serializer = AuthResponseSerializer({
                    'access_token': refresh.access_token,
                    'refresh_token': refresh,
                    'user': user
                })
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response({'error': _('Invalid credentials')}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_serializer = AuthResponseSerializer({'access_token': refresh.access_token,
                                                          'refresh_token': refresh,
                                                          'user': user})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            access_token = serializer.validated_data['access']
            refresh_token = serializer.validated_data['refresh']
            response_serializer = AuthResponseSerializer({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user
            })
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
