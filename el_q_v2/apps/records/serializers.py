from rest_framework import serializers
from .models import Record

class RecordAddSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(max_length=255, allow_null=True)
    doctorName = serializers.CharField(max_length=255, allow_null=True)
    class Meta:
        model = Record
        fields = "__all__"
