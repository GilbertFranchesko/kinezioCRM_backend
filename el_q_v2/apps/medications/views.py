from django.shortcuts import render

from .models import Medication

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MedicationSerializer

class ShowAll(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()

class ShowByMedRecord(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationSerializer

    def get_queryset(self):
        medRecordID = self.request.GET['id']
        medications = Medication.objects.filter(medRecord = medRecordID)
        for medication in medications:
            medication.doctorName = medication.get_doctor_name()
        return medications

class DeleteById(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    lookup_field = "id"
