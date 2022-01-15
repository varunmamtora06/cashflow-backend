from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Category

from ..serializers.categories import CategorySerializer

from ..utils import get_user

@api_view(['GET'])
def get_categories(request):
    user = get_user(request)

    categories = Category.objects.filter(by_user=user)
    category_serializer = CategorySerializer(categories, many=True)

    return Response({"categories":category_serializer.data}, status=status.HTTP_200_OK)