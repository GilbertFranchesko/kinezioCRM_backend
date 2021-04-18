from rest_framework import status, generics
from .models import MedRecord
from medications.models import Medication
from .serializers import MedRecordSerializer, MedRecordIDSerializer, MedRecordInitSerializer, MedRecordShowBy, MedicationSerializer, MedicationDeleteSerializer
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
            # For get patientName and doctorName.
            dict_create_model = model_to_dict(create_model)
            dict_create_model['patientName'] = create_model.getPatient()
            dict_create_model['doctorName'] = create_model.getDoctor()
            return Response(dict_create_model, status=status.HTTP_201_CREATED)
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


class AddMedication(APIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            med_record_object = MedRecord.objects.get(id = serializer.data['medrecord_id'])
            medications_object = med_record_object.medications

            for i in range(len(medications_object)):
                json_data = json.loads(medications_object[i])

                if json_data['medication_id'] == serializer.data['medication_id']:
                    return Response("Препарат в данной медицинской карте уже прописан!", status=status.HTTP_400_BAD_REQUEST)

            # NOTE: Delete medrecord id.
            not_medrecord_data = serializer.data
            not_medrecord_data.pop("medrecord_id")
            not_medrecord_data['name_medication'] = Medication.objects.get(id=serializer.data['medication_id']).name

            med_record_object.medications.append(json.dumps(not_medrecord_data))

            med_record_object_dict = model_to_dict(med_record_object)
            med_record_object_dict['patientName'] = med_record_object.getPatient()
            med_record_object_dict['doctorName'] = med_record_object.getDoctor()
            med_record_object_dict['created'] = str(med_record_object.created)


            med_record_object.save()

            return Response(med_record_object_dict)
        else:
            return Response(serializer.errors)
        return Response("ok")


class DeleteMedication(APIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationDeleteSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            medrecord_object = MedRecord.objects.get(id = serializer.data['medrecord_id'])
            medications_in_medrecord = medrecord_object.medications

            for i in range(len(medications_in_medrecord)):
                json_data = json.loads(medications_in_medrecord[i])

                if json_data['medication_id'] == serializer.data['medication_id']:
                    update_medication = medications_in_medrecord.pop(i)
                    medrecord_object.medications = medications_in_medrecord

                medrecord_object.save()

                medrecord_object_dict = model_to_dict(medrecord_object)
                medrecord_object_dict['patientName'] = medrecord_object.getPatient()
                medrecord_object_dict['doctorName'] = medrecord_object.getDoctor()
                # BUG: model_to_dict delete field created.
                medrecord_object_dict['created'] = str(med_record_object.created)

                return Response(medrecord_object_dict)
            else:
                return Response("no")
        else:
            return Response(serializer.errors)
