import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Basic"

    """
    Метод authenticate возвращяет либо: None или (user, token).
    None - в случае если в заголовке нет данных, в заголовке имеються пробелы.
    """

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_creadentials(request, token)

    """    
    Попытайтесь подтвердить данные учетные данные. Если аутентификация
    успешно, верните пользователя и токен. Если нет, то выдает ошибку.
    """
    def _authenticate_creadentials(self, reqeust, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            error_message = "Invalid authentication. Could not decode token."
            raise exceptions.AuthenticationFailed(error_message)

        try:
            user = User.objects.get(pk = payload['id'])
        except User.DoesNotExist:
            error_message = "No user matching this token was found."
            raise exceptions.AuthenticationFailed(error_message)

        if not user.is_active:
            error_message = "This user has been deactivated."
            raise exceptions.AuthenticationFailed(error_message)


        return (user, token)