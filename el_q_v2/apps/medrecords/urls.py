from django.urls import re_path
from .views import Show
urlpatterns = [
    re_path(r'^show/?$', Show.as_view(), name="show")

]