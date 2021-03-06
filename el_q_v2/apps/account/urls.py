from django.urls import path, re_path, include

from .views import LoginAPIView, RegisterAPIView, InfoByAuthAPIView, SetPhoto, Check, GetPatients, GetDoctors, InfoByIdAPIView, UpdatePhoto

urlpatterns = [
    re_path(r'^login/?$', LoginAPIView.as_view(), name="UserLogin"),
    re_path(r'^register/?$', RegisterAPIView.as_view(), name="UserRegister"),
    re_path(r'^getInfo/?$', InfoByAuthAPIView.as_view(), name="UserInfo"),
    re_path(r'^getInfoById/?$', InfoByIdAPIView.as_view(), name="UserInfoByID"),

    path("updatePhoto", UpdatePhoto.as_view(), name="update_photo"),



    re_path(r'^checkLogin/?$', Check.as_view(), name="Check"),
    re_path(r'^getPatients/?$', GetPatients.as_view(), name="GetPatients"),
    re_path(r'^getDoctors/?$', GetDoctors.as_view(), name="GetDoctors")

]
