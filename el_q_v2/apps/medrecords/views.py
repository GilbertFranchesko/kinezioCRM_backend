from rest_framework import status, generics
from .models import MedRecord
from .serializers import MedRecordSerializer, MedRecordIDSerializer, MedRecordInitSerializer, MedRecordShowBy
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.views import APIView
import json

class ShowALL(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedRecordSerializer
    queryset = MedRecord.objects.all()

    def create(self, request):
        doctor = request.data.get('doctor')
        patient = request.data.get('patient')
        if doctor is None: doctor = request.user.id
        try:
            MedRecord.objects.get(patient=patient)
        except:
            create_model = MedRecord(
                doctor = doctor,
                patient = patient
            )
            create_model.save()
            return Response("ok", status=status.HTTP_201_CREATED)
        else: return Response({"error": "Мед. карта уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

class ShowByID(generics.ListAPIView):
    serializer_class = MedRecordShowBy
    permission_classes = [AllowAny]

    def get(self, request):
        id = request.GET.get('id')
        queryset = MedRecord.objects.get(id=id)
        queryset_model = model_to_dict(queryset)
        queryset_model['patientName'] = queryset.getPatient()
        queryset_model['doctorName'] = queryset.getDoctor()
        queryset_model['created'] = str(queryset.created)
        queryset_model['update'] = str(queryset.update)
        serializer = self.serializer_class(data=queryset_model)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class ShowByPatient(generics.RetrieveAPIView):
    queryset = MedRecord.objects.all()
    serializer_class = MedRecordIDSerializer
    permission_classes = [AllowAny]
    lookup_field = 'patient'

class ShowByDoctor(generics.RetrieveAPIView):
    queryset = MedRecord.objects.all()
    serializer_class = MedRecordIDSerializer
    permission_classes = [AllowAny]
    lookup_field = 'doctor'

class ShowByToken(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedRecordInitSerializer

    def get_queryset(self):
        user = self.request.user.id
        if self.request.user.type == "Пациент":
            patient_check = MedRecord.objects.get(patient=user)
            patient_check.doctorName = patient_check.getDoctor
            patient_check.patientName = patient_check.getPatient
            return [patient_check,]
        elif self.request.user.type == "Врач":
            doctor_check = MedRecord.objects.filter(doctor=user)
            for i in range(len(doctor_check)):
                doctor_check[i].doctorName = "%s [ID:%i]" % (doctor_check[i].getDoctor(), doctor_check[i].doctor)
                doctor_check[i].patientName = "%s [ID:%i]" % (doctor_check[i].getPatient(), doctor_check[i].patient)
            return doctor_check

class UpdateMedRecords(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedRecordIDSerializer
    queryset = MedRecord.objects.all()
    lookup_url_kwarg = "id"
