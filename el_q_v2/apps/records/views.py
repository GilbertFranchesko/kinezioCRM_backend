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

    def create(self, request, *args, **kwargs):
        patientFirstName = request.data.get('patientFirstName')
        patientLastName = request.data.get('patientLastName')
        patientNumberPhone = request.data.get('patientNumberPhone')
        dateEvent = request.data.get('dateEvent')
        timeEvent = request.data.get('timeEvent')
        doctor = request.data.get('doctor')
        patient = request.data.get('patient')
        if patientFirstName == None or patientLastName == None or patientNumberPhone == None:
            print('NotGuest Record ADD')
            new_object = Record(
                dateEvent = dateEvent,
                timeEvent = timeEvent,
                doctor = doctor,
                patient = patient
            )
            new_object.save()
            return Response("ok")
        else:
            print('NotGuest Record ADD')
            new_object = Record(
                patientFirstName = patientFirstName,
                patientLastName = patientLastName,
                patientNumberPhone = patientNumberPhone,
                dateEvent = dateEvent,
                timeEvent = timeEvent,
                doctor = doctor,
                patient = patient
            )
            new_object.save()
            return Response("ok")


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
            check_doctor = Record.objects.filter(doctor=user).order_by('-id')
            for i in range(len(check_doctor)):
                if not check_doctor[i].patient == 0:
                    check_doctor[i].patientName = check_doctor[i].getPatient()
                    check_doctor[i].doctorName = check_doctor[i].getDoctor()
                else:
                    check_doctor[i].patientName = check_doctor[i].patientFirstName + " " + check_doctor[
                        i].patientLastName + " (гость)"
                    check_doctor[i].doctorName = check_doctor[i].getDoctor()
                    print(check_doctor[i])
            return check_doctor


class DeleteByID(generics.DestroyAPIView):
    serializer_class = RecordAddSerializer
    permission_classes = [AllowAny]
    queryset = Record.objects.all()
    lookup_field = 'id'

