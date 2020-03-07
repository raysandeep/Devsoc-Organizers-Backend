from rest_framework import serializers
from .models import (
    evaluator,
    TeamInfo,
    UserType,
    Messaging,
    Notifications
)


class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluator
        fields = ['team']
        depth = 1


class MessagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messaging
        fields = '__all__'



class NotificationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['device_id']