from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count
from ..models import Category, Expenditure

from ..serializers.categories import CategorySerializer, CategoryCountPieSerializer

from ..utils import get_user

@api_view(['GET'])
def get_categories(request):
    user = get_user(request)

    categories = Category.objects.filter(by_user=user)
    category_serializer = CategorySerializer(categories, many=True)

    return Response({"categories":category_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_most_used_categories(request):
    user = get_user(request)

    categories = Category.objects.filter(by_user=user).order_by("-category_used_count")
    category_serializer = CategorySerializer(categories, many=True)

    return Response({"categories":category_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_category_count(request):
    user = get_user(request)

    category_count = Expenditure.objects.filter(by_user=user).values('belongs_to_category__category_name').annotate(exp_count=Count('belongs_to_category__category_name'))

    category_serializer = CategoryCountPieSerializer(category_count, many=True)

    category_labels = [ expenditure["belongs_to_category__category_name"] for expenditure in category_serializer.data ]
    category_count = [ expenditure["exp_count"] for expenditure in category_serializer.data ]



    category_count_pie = {
        "labels": category_labels,
        "count": category_count
    }

    return Response({"category_count_pie":category_count_pie}, status=status.HTTP_200_OK)