from rest_framework import serializers, exceptions
from django.contrib.auth.models import User

from ..models import Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"