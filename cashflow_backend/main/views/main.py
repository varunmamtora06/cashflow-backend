from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import *
from ..helpers import category_exists

@api_view(['GET'])
def main(request):
    user = User.objects.get(id=1)
    cn = "ct1"
    print(category_exists(user,cn))
    return Response({"Mssg":"hello"})