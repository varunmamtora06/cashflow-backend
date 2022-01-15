from rest_framework_simplejwt.backends import TokenBackend
from cashflow_backend.settings import SECRET_KEY
import jwt

## import models
from django.contrib.auth.models import User


def get_user(request):
    token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    # print(f"dec->{jwt.decode(token,SECRET_KEY,'HS256')}")
    ## can use 
    # valid_data = jwt.decode(token,SECRET_KEY,'HS256')
    # instead of below 

    valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
    
    user_id = valid_data['user_id']
    return User.objects.get(id=user_id)