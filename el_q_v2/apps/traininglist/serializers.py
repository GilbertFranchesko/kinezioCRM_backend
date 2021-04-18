from rest_framework import serializers
from .models import Training

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"

class ManyIdSerializer(serializers.Serializer):
    list_id = serializers.CharField()
