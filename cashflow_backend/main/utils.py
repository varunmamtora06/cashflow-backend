from rest_framework_simplejwt.backends import TokenBackend
from cashflow_backend.settings import SECRET_KEY
import jwt

## import models
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken

def get_user(request):
    token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    # print(f"dec->{jwt.decode(token,SECRET_KEY,'HS256')}")
    ## can use 
    # valid_data = jwt.decode(token,SECRET_KEY,'HS256')
    # instead of below 

    valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
    
    user_id = valid_data['user_id']
    return User.objects.get(id=user_id)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }