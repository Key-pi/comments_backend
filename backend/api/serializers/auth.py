# serializers.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.password_validation import validate_password

User = get_user_model()  # noqa


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'language', 'avatar']


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class AuthResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserSerializer()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)
    language = serializers.ChoiceField(choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    avatar = serializers.ImageField(required=False, allow_null=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirmation', 'language', 'avatar']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match.'})
        return super().validate(data)

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class RefreshSerializer(TokenRefreshSerializer):
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.context['request'].user).data
        return data
