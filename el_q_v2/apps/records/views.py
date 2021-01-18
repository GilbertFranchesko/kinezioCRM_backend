from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RecordAddSerializer

from .models import Record

class ShowAll(generics.ListCreateAPIView):
    serializer_class = RecordAddSerializer
    queryset = Record.objects.all()
    permission_classes = [AllowAny]

class ShowByToken(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecordAddSerializer

    def get_queryset(self):
        user = self.request.user.id
        if self.request.user.type == "Пациент":
            check_patient = get_object_or_404(Record, patient=user)
            check_patient.patientName = check_patient.getPatient()
            check_patient.doctorName = check_patient.getDoctor()
            return [check_patient, ]
        elif self.request.user.type == "Врач":
            check_doctor = Record.objects.filter(doctor=user)
            for i in range(len(check_doctor)):
                print("\n\n",check_doctor[i].patientFirstName,"\n\n")
                if not check_doctor[i].patient == 0:
                    check_doctor[i].patientName = check_doctor[i].getPatient()
                else:
                    check_doctor[i].patientName = check_doctor[i].patientFirstName + " " + check_doctor[
                        i].patientLastName + " (гость)"
                    check_doctor[i].doctorName = check_doctor[i].getDoctor()
                    print(check_doctor[i])
            return check_doctor

