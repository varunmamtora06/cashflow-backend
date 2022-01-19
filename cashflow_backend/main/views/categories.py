from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count
from django.db.models import Sum
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

@api_view(['GET'])
def get_category_by_month(request):
    user = get_user(request)

    expenditures = Expenditure.objects.filter(by_user=user)

    categs = []

    for expenditure in expenditures:
        if not expenditure.belongs_to_category.category_name in categs:
            categs.append(expenditure.belongs_to_category.category_name)

    print(categs)

    categs_exp_amt = Expenditure.objects.filter(by_user=user).values("belongs_to_category__category_name", "expenditure_date__month").annotate(tot_amt=Sum("expenditure_amount")).order_by("expenditure_date__month")
    print(categs_exp_amt)

    chrt = {}
    for categ_exp in categs_exp_amt:
        chrt[categ_exp["belongs_to_category__category_name"]] = [0,0,0,0,0,0,0,0,0,0,0,0]
    # for category in categs:
    for i in range(12):
        for categ_exp in categs_exp_amt:
            if i == categ_exp["expenditure_date__month"] - 1:
                # chrt[categ_exp["belongs_to_category__category_name"]].append(categ_exp["tot_amt"])
                chrt[categ_exp["belongs_to_category__category_name"]][i] = categ_exp["tot_amt"]
            # else:
            #     chrt[categ_exp["belongs_to_category__category_name"]].append(0)

    return Response({"month_chart":chrt})