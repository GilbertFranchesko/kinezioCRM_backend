from rest_framework import status, generics
from .models import MedRecord
from medications.models import Medication
from traininglist.models import Training
from .serializers import MedRecordSerializer, MedRecordIDSerializer, MedRecordInitSerializer, MedRecordShowBy, MedicationSerializer, MedicationDeleteSerializer, AddTrainingSerializer, TrainingIdFromList
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
            medrecord_object = MedRecord.objects.get(id = serializer.data['medrecord_id'])
            medications_object = None

            if medrecord_object.medications != "":
                medications_object = json.loads(medrecord_object.medications)
                medications_object_list = medications_object['medications_list']
                for medication in medications_object_list:
                    if medication['medication_id'] == serializer.data['medication_id']:
                        return Response("Данный препарат уже прописан в данную мед. карту!", status = status.HTTP_400_BAD_REQUEST)
            

                # Обращяемся непосредственно к самому списку словарей медикаментов.
                medications_list = medications_object['medications_list']

                modifed_serializer_data  = serializer.data
                modifed_serializer_data.pop("medrecord_id")
                modifed_serializer_data['name_medication'] = Medication.objects.get(id=serializer.data['medication_id']).name
                medications_list.append(modifed_serializer_data)

                # Устанавливаем новое значение для списка medications_list в поле medications базы MedRecord.
                medications_object["medications_list"] = medications_list
                # Делаем замену ординарных на двойные кавычки.
                medications_object_str = str(medications_object).replace("'", '"')
                medrecord_object.medications = medications_object_str
                
                medrecord_object.save()

            else:
                # Формирование списка с именнем. Для валидности ряда формата JSON.
                default_structure = {"medications_list": []}
                modifed_serializer_data = serializer.data
                modifed_serializer_data['name_medication'] = Medication.objects.get(id=serializer.data['medication_id']).name
                default_structure["medications_list"].append(modifed_serializer_data)
                new_medications = json.dumps(default_structure)
                # new_medications - str. И вносим в базу.
                medrecord_object.medications = new_medications
                medrecord_object.save()
            
            # Готовим к выводу.
            medrecord_object_dict = model_to_dict(medrecord_object)
            medrecord_object_dict['patientName'] = medrecord_object.getPatient()
            medrecord_object_dict['doctorName'] = medrecord_object.getDoctor()
            medrecord_object_dict['created'] = str(medrecord_object.created)

            return Response(medrecord_object_dict)

        else:
            return Response(serializer.errors)


class DeleteMedication(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicationDeleteSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            medrecord_object = MedRecord.objects.get(id = serializer.data['medrecord_id'])
            medications_object = json.loads(medrecord_object.medications)

            # Инициализируем счётчик.
            i = 0
            for medication in medications_object['medications_list']:
                if medication['medication_id'] == serializer.data['medication_id']:
                    medications_object['medications_list'].pop(i)
                i+=1

            # Заносим измёненый список в базу.
            edit_list = json.dumps(medications_object['medications_list'])
            if edit_list == "[]": edit_list = ""
            medrecord_object.medications = edit_list
            medrecord_object.save()

            medrecord_object_dict = model_to_dict(medrecord_object)
            medrecord_object_dict['patientName'] = medrecord_object.getPatient()
            medrecord_object_dict['doctorName'] = medrecord_object.getDoctor()
            medrecord_object_dict['created'] = str(medrecord_object.created)
            
            return Response(medrecord_object_dict)

        
        else:
            return Response(serializer.errors)

class AddTraining(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddTrainingSerializer

    def post(self, request):

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            
            new_training_object = Training(
                patient = serializer.data['patient'],
                doctor = serializer.data['doctor'],
                medrecord = serializer.data['medrecord'],
                title = serializer.data['title'],
                description = serializer.data['description'],
                finish_date = serializer.data['finish_date']
            )

            new_training_object.save()

            medrecord_object = MedRecord.objects.get(id = serializer.data['medrecord'])
            medrecord_object.training_list.append(new_training_object.id)
            medrecord_object.save()

            #   Готовим к выводу.
            medrecord_object_dict = model_to_dict(medrecord_object)
            medrecord_object_dict['patientName'] = medrecord_object.getPatient()
            medrecord_object_dict['doctorName'] = medrecord_object.getDoctor()
            medrecord_object_dict['created'] = str(medrecord_object.created)

            return Response(medrecord_object_dict)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemomveTraining(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingIdFromList

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            
            #   Удаляём саму запись тренировки.
            training_object = Training.objects.get(id=serializer.data['training_id'])
            training_object.delete()
            
            #   Убираем индекс записи из мед. карты.
            medrecord_object = MedRecord.objects.get(id=serializer.data['medrecord_id'])
            medrecord_object.training_list.pop(medrecord_object.training_list.index(serializer.data['training_id']))
            print(medrecord_object.training_list)
            medrecord_object.save()
            
            #   Готовим к выводу.
            medrecord_object_dict = model_to_dict(medrecord_object)
            medrecord_object_dict['patientName'] = medrecord_object.getPatient()
            medrecord_object_dict['doctorName'] = medrecord_object.getDoctor()
            medrecord_object_dict['created'] = str(medrecord_object.created)

            return Response(medrecord_object_dict)
            

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)