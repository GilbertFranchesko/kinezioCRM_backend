from django.urls import re_path, include

from .views import LoginAPIView, RegisterAPIView

urlpatterns = [
    re_path(r'^login/?$', LoginAPIView.as_view(), name="UserLogin"),
    re_path(r'^register/?$', RegisterAPIView.as_view(), name="UserRegister")
]