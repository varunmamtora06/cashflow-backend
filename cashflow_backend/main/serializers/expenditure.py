from rest_framework import serializers, exceptions
from django.contrib.auth.models import User

from ..models import Expenditure, Category

from .categories import CategorySerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ExpenditureSerializer(serializers.ModelSerializer):
    belongs_to_category = CategorySerializer(many=False)
    by_user = UserSerializer(many=False)
    class Meta:
        model = Expenditure
        fields = ["id", "expenditure_title", "expenditure_amount", "expenditure_remarks", "expenditure_date", "belongs_to_category", "by_user"]

class ExpenditureHeatmapSerializer(serializers.Serializer):
    expenditure_date = serializers.CharField()
    exp_count = serializers.IntegerField()