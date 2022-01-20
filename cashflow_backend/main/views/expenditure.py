from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count
from ..models import Expenditure, Category, ExpenditureReceipt

from ..serializers.expenditure import ExpenditureSerializer, CategorySerializer, ExpenditureHeatmapSerializer

from ..utils import get_user
from ..helpers import category_exists

from decimal import Decimal

## importing OCR
from ..ocr_detect import extract_data

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

import datetime
from time import strptime

def month_chooser(month):
    months = {
        "January": 1,
        "JANUARY": 1,
        "February": 2,
        "FEBRUARY": 2,
        "March": 3,
        "MARCH":3,
        "April": 4,
        "APRIL": 4,
        "May":5,
        "MAY":5,
        "June":6,
        "JUNE":6,
        "July":7,
        "JULY":7,
        "August":8,
        "AUGUST":8,
        "September":9,
        "SEPTEMBER":9,
        "October":10,
        "OCTOBER":10,
        "November":11,
        "NOVEMBER":11,
        "December":12,
        "DECEMBER":12
    }

    return months[month]

@api_view(['POST'])
def add_expenditure(request):
    user = get_user(request)

    expenditure_title = request.data["expenditure_title"]
    try:
        expenditure_amount = round(Decimal(request.data["expenditure_amount"]), 2)
    except:
        print("except")
        expenditure_amount = round(Decimal("000.00"), 2)
    expenditure_remarks = request.data["expenditure_remarks"]
    expenditure_date = request.data["expenditure_date"]
    category_name = request.data["category_name"]

    if " " in expenditure_date:
        date_chunck = expenditure_date.split(" ")
    if "-" in expenditure_date:
        date_chunck = expenditure_date.split("-")
    if "/" in expenditure_date:
        date_chunck = expenditure_date.split("/")

    print("date_chunckb4")
    print(date_chunck)
    if len(date_chunck[1]) == 3:
        date_chunck[1] = str(strptime(date_chunck[1],'%b').tm_mon)
        if len(expenditure_date) == 1:
            date_chunck[1] = "0" + date_chunck[1]
    if len(date_chunck[1]) > 3:
        date_chunck[1] = str(month_chooser(date_chunck[1]))
        if len(expenditure_date) == 1:
            date_chunck[1] = "0" + date_chunck[1]
    print("date_chunckafter")
    print(date_chunck)
    
    if len(date_chunck[2]) == 2:
        date_chunck[2] = "20"+date_chunck[2]

    expenditure_date = date_chunck[0] + "-"+ date_chunck[1] +"-"+ date_chunck[2]

    print(f"beforConv{expenditure_date}")
    if len(date_chunck[0]) < 3:
        expenditure_date = datetime.datetime.strptime(expenditure_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        print(f"aftaConv{expenditure_date}")
    # try:
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
    # except:
    #     return Response({"MSSG":"FAILED_TO_ADD_TRANSACTION"}, status=status.HTTP_400_BAD_REQUEST)

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


import json

@csrf_exempt
def detect_expenditure(request):
    user = get_user(request)

    exp_pic = request.FILES["exp_pic"]
    print(request.FILES["exp_pic"])

    exp_pic_file = ExpenditureReceipt.objects.create(receipt_pic=exp_pic, by_user=user)

    # print(exp_pic_file)
    # print(exp_pic_file.receipt_pic.name)
    # print(exp_pic_file.receipt_pic.url)

    d = extract_data(exp_pic_file.receipt_pic.url)
    
    return JsonResponse({"MSSG":"Okay", "model_extr_data":d})

@api_view(["GET"])
def expenditure_heatmap(request):
    user = get_user(request)

    expenditures = Expenditure.objects.filter(by_user=user).values("expenditure_date").annotate(exp_count=Count("expenditure_date")).order_by("-exp_count")
    expenditure_serializer = ExpenditureHeatmapSerializer(expenditures, many=True)

    expenditure_heatmap = []

    for expenditure in expenditures:
        expenditure_heatmap.append({"date":expenditure["expenditure_date"], "count":expenditure["exp_count"]})

    return Response({"heatmap":expenditure_heatmap})