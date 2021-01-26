from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import generics
from .models import Notification
from .serializers import NotificationInitSerializer

class ShowAll(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationInitSerializer
    permission_classes = [AllowAny]

class ShowByToken(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationInitSerializer

    def get_queryset(self):
        user = self.request.user.id
        if self.request.user.type == "Пациент":
            check_patient = Notification.objects.filter(patient=user).order_by('-id')
            for i in range(len(check_patient)):
                check_patient[i].patientName = check_patient[i].getPatient()
                check_patient[i].doctorName = check_patient[i].getDoctor()
            return check_patient
        elif self.request.user.type == "Врач":
            check_doctor = Notification.objects.filter(doctor=user).order_by('-id')
            for i in range(len(check_doctor)):
                if check_doctor[i].patient == 0:
                    continue
                check_doctor[i].patientName = check_doctor[i].getPatient()
                check_doctor[i].doctorName = check_doctor[i].getDoctor()
            return check_doctor



