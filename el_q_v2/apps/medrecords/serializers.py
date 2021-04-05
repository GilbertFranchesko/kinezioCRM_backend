from rest_framework import serializers
from django.db.models.fields import TextField
from .models import MedRecord
from account.models import User

class MedRecordSerializer(serializers.Serializer):
    patient = serializers.IntegerField()
    doctor = serializers.IntegerField()
    diagnosis = serializers.CharField(max_length=255, allow_null=True)
    training_list = serializers.CharField(max_length=1000, allow_null=True)
    created = serializers.DateTimeField(write_only=False, allow_null=True)
    update = serializers.DateTimeField(write_only=False, allow_null=True)
    active_id = serializers.IntegerField(allow_null=True)

    def validate(self, data):
        patient = data.get('patient')
        doctor = data.get('doctor')
        diagnosis = data.get('diagnosis')
        training_list = data.get('training_list')

        if patient == doctor:
            raise serializers.ValidationError(
                "Пациент не доктор!"
            )

        try:
            check_patient = User.objects.get(id=patient)
            if check_patient.type != "Пациент": raise serializers.ValidationError("Это не пациент!")
        except:
            raise serializers.ValidationError(
                    "Пациент не найден!"
                )
        try:
            check_doctor = User.objects.get(id=doctor)
            if check_doctor.type != "Врач": raise serializers.ValidationError("Это не врач!")
        except:
            raise serializers.ValidationError(
                "Доктор не найден!"
            )

        try:
            status = MedRecord.objects.get(patient=patient)
        except:
            new_med_record = MedRecord(
                patient=patient,
                doctor=doctor,
                diagnosis=diagnosis,
                training_list=training_list,
                active_id=doctor
                )
            new_med_record.save()

        return {
            "ok"
        }


class MedRecordIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedRecord
        fields = "__all__"


class MedRecordInitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    patient = serializers.IntegerField()
    doctor = serializers.IntegerField()
    patientName = serializers.CharField(max_length=255)
    doctorName = serializers.CharField(max_length=255)
    diagnosis = serializers.CharField(max_length=255)
    created = serializers.CharField(max_length=255)

class MedRecordShowBy(serializers.ModelSerializer):
    patientName = serializers.CharField(max_length=255)
    doctorName = serializers.CharField(max_length=255)
    created = serializers.CharField(max_length=255)
    update = serializers.CharField(max_length=255)
    id = serializers.IntegerField()
    class Meta:
        model = MedRecord
        fields = "__all__"



class MedRecordAddSerializer(serializers.Serializer):
    patient = serializers.CharField(max_length=255)
    doctor = serializers.IntegerField()

    def validate(self, data):
        patient = data.get('patient', None)
        doctor = data.get('doctor', None)

        if patient == doctor:
            raise serializers.ValidationError(
                "Пациент не доктор!"
            )

        try:
            check_patient = User.objects.get(id=patient)
            if check_patient.type != "Пациент": raise serializers.ValidationError("Это не пациент!")
        except:
            raise serializers.ValidationError(
                    "Пациент не найден!"
                )
        try:
            check_doctor = User.objects.get(id=doctor)
            if check_doctor.type != "Врач": raise serializers.ValidationError("Это не врач!")
        except:
            raise serializers.ValidationError(
                "Доктор не найден!"
            )

        try:
            status = MedRecord.objects.get(patient=patient)
        except:
            new_med_record = MedRecord(
                patient=patient,
                doctor=doctor,
                active_id=doctor
                )
            new_med_record.save()

        return {
            "ok"
        }




