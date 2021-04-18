from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import Training
from .serializers import TrainingSerializer, ManyIdSerializer

class ShowById(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingSerializer
    lookup_field = 'id'
    queryset = Training.objects.all()

class CreateTraining(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TrainingSerializer

class DeleteTraining(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = TrainingSerializer
    lookup_field = 'id'
    queryset = Training.objects.all()

    
class ShowByManyId(APIView):
    permission_classes = [AllowAny]
    serializer_class = ManyIdSerializer

    def post(self, request):
        many_id = request.data
        trainings = []
        for select_id in many_id:
            try:
                training_object = Training.objects.get(id = select_id)
                trainings.append(model_to_dict(training_object))

            except Training.DoesNotExist:
                return Response("В списке тренировка не найдена!", status = status.HTTP_400_BAD_REQUEST)

        return Response(trainings)
