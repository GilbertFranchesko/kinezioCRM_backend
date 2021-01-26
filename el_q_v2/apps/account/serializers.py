from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Email is required field for log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Password is required field for log in.'
            )

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким E-mail и паролем не найден!'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'User has been deactivated.'
            )

        return {
            'token': user.token
        }


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, write_only=False)
    last_name = serializers.CharField(max_length=255, write_only=False)
    email = serializers.EmailField(write_only=False)
    password = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, write_only=False)

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)
        password = data.get('password', None)
        username = data.get('username', None)

        try:
            check_tmp = User.objects.get(email=email)
            User.objects.get(username=username)
        except:
            pass
        else:
            raise serializers.ValidationError("Пользователь уже существует!")



        tmp_account = User.objects.create_user(first_name = first_name,
                                       last_name = last_name,
                                       email = email,
                                       password=password,
                                       username = username)

        if tmp_account is None:
            raise serializers.ValidationError("Произошла ошибка!")

        return {
            'id': tmp_account.id,
            'first_name': tmp_account.first_name,
            'last_name': tmp_account.last_name,
            'email': tmp_account.email,
            'username': tmp_account.username,
        }


class PhotoSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('photo')

class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    AllName = serializers.CharField(max_length=255, allow_null=True)

class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    AllName = serializers.CharField(max_length=255, allow_null=True)

