from rest_framework import serializers
from .models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    doctorName = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = Medication
        fields = "__all__"
