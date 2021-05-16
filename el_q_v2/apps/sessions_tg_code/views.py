from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Code
from .serializers import CodeSerializer, CodeSerializerID

import math, random


class CreateCode(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CodeSerializer

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            digits = "0123456789"
            gen_c = ""

            for i in range(6):
                gen_c += digits[math.floor(random.random() * 10)]

            new_object = Code(
                user_id = serializer.data['user_id'],
                code = gen_c,
                token = request.user.token
            )
            new_object.save()

            new_object_dict = model_to_dict(new_object)
            return Response(new_object_dict)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectCode(APIView):
    permission_classes = [AllowAny]
    serializer_class = CodeSerializerID

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            code_object = Code.objects.get(code = serializer.data['code'])
            return Response({"token": code_object.token})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)