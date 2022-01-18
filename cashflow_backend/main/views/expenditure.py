from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from ..models import Expenditure, Category, ExpenditureReceipt

from ..serializers.expenditure import ExpenditureSerializer, CategorySerializer

from ..utils import get_user
from ..helpers import category_exists

from decimal import Decimal

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


@api_view(['POST'])
def add_expenditure(request):
    user = get_user(request)

    expenditure_title = request.data["expenditure_title"]
    expenditure_amount = round(Decimal(request.data["expenditure_amount"]), 2)
    expenditure_remarks = request.data["expenditure_remarks"]
    expenditure_date = request.data["expenditure_date"]
    category_name = request.data["category_name"]

    try:
        is_exist, category = category_exists(user, category_name)
        if(is_exist):
            category.category_used_count += 1
            category.save()

            Expenditure.objects.create(expenditure_title=expenditure_title, expenditure_amount=expenditure_amount, expenditure_remarks=expenditure_remarks, expenditure_date=expenditure_date, belongs_to_category=category, by_user=user)
            return Response({"MSSG":"TRANSACTION_ADDED"}, status=status.HTTP_200_OK)
        else:
            category = Category.objects.create(category_name=category_name, category_used_count=1, by_user=user)
            Expenditure.objects.create(expenditure_title=expenditure_title, expenditure_amount=expenditure_amount, expenditure_remarks=expenditure_remarks, expenditure_date=expenditure_date, belongs_to_category=category, by_user=user)
            return Response({"MSSG":"TRANSACTION_ADDED"}, status=status.HTTP_200_OK)
    except:
        return Response({"MSSG":"FAILED_TO_ADD_TRANSACTION"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_expenditure(request, expenditure_id):
    user = get_user(request)

    expenditure = Expenditure.objects.get(id=expenditure_id)

    expenditure.expenditure_title = request.data["expenditure_title"]
    expenditure.expenditure_amount = round(Decimal(request.data["expenditure_amount"]), 2)
    expenditure.expenditure_remarks = request.data["expenditure_remarks"]
    expenditure.expenditure_date = request.data["expenditure_date"]

    expenditure.save()

    return Response({"MSSG":"EXPENDITURE_UPDATED"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def detect_expenditure(request):
    user = get_user(request)

   
    print(request.FILES["exp_pic"])

    exp_pic_file = ExpenditureReceipt.objects.create(receipt_pic=exp_pic, by_user=user)

    # print(exp_pic_file)
    # print(exp_pic_file.receipt_pic.name)
    # print(exp_pic_file.receipt_pic.url)
    
    return Response({"MSSG":"Okay"}, status=status.HTTP_200_OK)