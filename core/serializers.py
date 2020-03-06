from rest_framework import serializers
from .models import (
    evaluator,
    TeamInfo,
    UserType
)

class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluator
        fields = '__all__'
        depth = 1