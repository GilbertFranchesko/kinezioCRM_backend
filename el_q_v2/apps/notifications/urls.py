from django.urls import re_path, path
from .views import ShowAll ,ShowByToken

urlpatterns = [
    re_path(r'showAll/?$', ShowAll.as_view(), name="show_all_notification"),
    re_path(r'showByToken/?$', ShowByToken.as_view(), name="show_by_token_notification")
]