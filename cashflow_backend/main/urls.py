from django.urls import path
from .views import main, expenditure

## rest imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ## auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/logout/', authentication.logout, name='logout'),

    path("main/", main.main, name="main"),
    path("allexpenditures/", expenditure.all_expenditures, name="allexpenditures"),
    path("get-n-expenditures/<int:exp_count>/", expenditure.get_n_expenditures, name="get_n_expenditures"),
]
