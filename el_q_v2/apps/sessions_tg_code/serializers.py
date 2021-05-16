from rest_framework import serializers
from .models import Code
from account.models import User

class CodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user_object = User.objects.get(id=value)

            codes_objects = Code.objects.all()
            for i in range(len(codes_objects)):
                if codes_objects[i].user_id == value:
                    raise serializers.ValidationError("Код уже выслан!")

            return value
        except:
            raise serializers.ValidationError("Пользователь не найден!")
    
class CodeSerializerID(serializers.Serializer):
    code = serializers.IntegerField()

    def validate_code(self, value):
        try:
            Code.objects.get(code=value)
            return value
        except:
            raise serializers.ValidationError("Код не найден!")