from rest_framework import serializers, exceptions
from django.contrib.auth.models import User

from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"