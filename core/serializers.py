from rest_framework import serializers
from .models import (
    evaluator,
    TeamInfo,
    UserType,
    Messaging,
    Notifications,
    EvaluationParms
)


class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluator
        fields = ['team','id']
        depth = 1


class MessagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messaging
        fields = '__all__'



class NotificationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['device_id']



class EvaluationParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationParms
        fields = '__all__'
        depth=2