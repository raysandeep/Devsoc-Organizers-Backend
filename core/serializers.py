from rest_framework import serializers
from .models import (
    evaluator,
    TeamInfo,
    UserType
)

class EvaluatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = evaluator
        fields = ['team']
        depth = 1