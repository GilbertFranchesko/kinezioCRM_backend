from rest_framework import serializers
from .models import Notification


class NotificationInitSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(max_length=255, allow_null=True)
    doctorName = serializers.CharField(max_length=255, allow_null=True)
    class Meta:
        model = Notification
        fields = "__all__"