from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Expenditure

from ..serializers.expenditure import ExpenditureSerializer

from ..utils import get_user

@api_view(['GET'])
def all_expenditures(request):
    user = get_user(request)
    expenditures = Expenditure.objects.filter(by_user=user)
    expenditure_serializer = ExpenditureSerializer(expenditures, many=True)

    return Response({"expenditures":expenditure_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_n_expenditures(request, exp_count):
    user = get_user(request)
    expenditures = Expenditure.objects.filter(by_user=user).order_by("-expenditure_date")[:exp_count]
    expenditure_serializer = ExpenditureSerializer(expenditures, many=True)

    return Response({"expenditures":expenditure_serializer.data}, status=status.HTTP_200_OK)