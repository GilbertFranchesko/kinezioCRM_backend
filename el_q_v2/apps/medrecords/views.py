from rest_framework import status
import json
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

class Show(APIView):
    def post(self, request):
        return Response('ok')