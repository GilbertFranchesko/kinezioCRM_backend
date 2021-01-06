from rest_framework import status
import json
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, PhotoSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InfoByAuthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.get(id=request.user.id)
        tmp = queryset.__dict__
        tmp.pop('_state')
        tmp.pop('password')
        return Response(tmp)


class SetPhoto(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data, files = request.FILES)
        serializer.is_valid()
        return Response(serializer.data)

class Check(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        queryset = User.objects.get(id=request.user.id)
        print(queryset.getClientIP(request))
        return Response('ok')


