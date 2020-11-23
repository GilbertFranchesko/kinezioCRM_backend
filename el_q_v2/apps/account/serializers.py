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

        user = authenticate(usernamd=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User with this email and password not founded.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'User has been deactivated.'
            )

        return {
            'token': user.token,
        }


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)
        password = data.get('password', None)
        username = data.get('username', None)

        try:
            check_tmp = User.objects.get(email=email)
        except:
            pass
        else:
            raise serializers.ValidationError("Пользователь уже существует!")

        tmp_account = User()
        tmp_account.first_name = first_name
        tmp_account.last_name = last_name
        tmp_account.email = email
        tmp_account.password = password
        tmp_account.username = username
        tmp_account.save()

        print(tmp_account)

        if tmp_account is None:
            raise serializers.ValidationError("Произошла ошибка!")

        return {
            'email': tmp_account,
        }
