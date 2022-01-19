from django.urls import path
from .views import main, expenditure, reminders, categories, goals, authentication

## rest imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ## auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', authentication.register, name='register'),
    # path('auth/logout/', authentication.logout, name='logout'),

    # expenditures
    path("main/", main.main, name="main"),
    path("allexpenditures/", expenditure.all_expenditures, name="allexpenditures"),
    path("get-n-expenditures/<int:exp_count>/", expenditure.get_n_expenditures, name="get_n_expenditures"),
    path("add-expenditure/", expenditure.add_expenditure, name="add_expenditure"),
    path("update-expenditure/<int:expenditure_id>", expenditure.update_expenditure, name="update_expenditure"),
    path("detect-expenditure/", expenditure.detect_expenditure, name="detect_expenditure"),
    path("expenditure-heatmap/", expenditure.expenditure_heatmap, name="expenditure_heatmap"),

    # categories
    path("get-categories/", categories.get_categories, name="get_categories"),
    path("get-most-used-categories/", categories.get_most_used_categories, name="get_most_used_categories"),
    path("get-category-count/", categories.get_category_count, name="get_category_count"),
    path("get-category-by-month/", categories.get_category_by_month, name="get_category_by_month"),
    
    # reminders
    path("get-reminders/", reminders.get_reminders, name="get_reminders"),
    path("add-reminder/", reminders.add_reminder, name="add_reminder"),
    path("complete-reminder/<int:reminder_id>/", reminders.complete_reminder, name="complete_reminder"),
    
    # goals
    path("get-goals/", goals.get_goals, name="get_goals"),
    path("add-goal/", goals.add_goal, name="add_goal"),
    path("update-goal/<int:goal_id>/", goals.update_goal, name="update_goal"),
]
