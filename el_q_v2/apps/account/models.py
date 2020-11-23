import jwt
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.conf import settings

from django.db import models
from django.core import validators

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    first_name = models.CharField("Имя", max_length=255, default="00000000")
    last_name = models.CharField("Фамилия", max_length=255, default="00000000")

    # USERNAME_FIELD - указывает какое поле мы будем юзать для входа.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.username

    # @property - делает это возможным. `token` - называеться динамическим свойством.
    @property
    def token(self):
        return self._generate_jwt_token()

    """ 
    Следущии две функции нужны для самого Django. 
    (Для обработки електроной очереди и т.д.) 
    """
    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username

    """
    Генерируем веб-токен JSON, в котором хранится идентификатор
    данного пользователя и срок его действия 60 дней.
    """
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days = 60)
        print(dt.strftime("%s"))
        token = jwt.encode({
            "id": self.pk,
            "exp": int(dt.strftime("%s"))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode("utf-8")