from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from ..utils import get_user, get_tokens_for_user

@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    firstname = request.data['firstname']

    try:
        User.objects.get(username=username)
        return Response({"MSSG":"USERNAME_EXISTS"}, status=status.HTTP_409_CONFLICT)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname)

        tokens = get_tokens_for_user(user)

        return Response({"MSSG":"REGISTERED_SUCCESSFULLY", "tokens":tokens}, status=status.HTTP_201_CREATED)