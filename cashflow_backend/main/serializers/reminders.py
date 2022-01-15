from rest_framework import serializers, exceptions
from django.contrib.auth.models import User

from ..models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"