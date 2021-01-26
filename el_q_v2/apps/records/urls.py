from django.urls import path, re_path
from .views import ShowAll, ShowByToken, DeleteByID

urlpatterns = [
    re_path(r'showAll/?$', ShowAll.as_view(), name="show_all_records"),
    re_path(r'showByToken/?$', ShowByToken.as_view(), name="show_by_token_record"),
    path('deleteById/<int:id>', DeleteByID.as_view(), name="delete_by_id")

]