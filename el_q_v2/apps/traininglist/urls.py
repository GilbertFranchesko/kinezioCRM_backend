from django.urls import re_path, path
from .views import ShowById, CreateTraining, ShowByManyId, DeleteTraining


urlpatterns = [
    path("showById/<int:id>", ShowById.as_view(), name="show_by_id" ),
    path("showByManyId/", ShowByManyId.as_view(), name="show_by_many_id"),

    path("createTraining/", CreateTraining.as_view(), name="create_training"),
    path("deleteTraining/<int:id>", DeleteTraining.as_view(), name="delete_training")
]
