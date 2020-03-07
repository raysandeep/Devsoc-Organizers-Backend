from rest_framework import serializers
from .models import (
    evaluator,
    TeamInfo,
    UserType,
    Messaging
)
from fcm_django.models import Device

class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluator
        fields = ['team']
        depth = 1


class MessagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messaging
        fields = '__all__'

class FCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id']