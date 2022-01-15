from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Goal

from ..serializers.goals import GoalSerializer

from ..utils import get_user

from decimal import Decimal

@api_view(['GET'])
def get_goals(request):
    user = get_user(request)

    goals = Goal.objects.filter(by_user=user)
    goal_serializer = GoalSerializer(goals, many=True)

    return Response({"goals":goal_serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_goal(request):
    user = get_user(request)

    goal_title = request.data["goal_title"]
    goal_desc = request.data["goal_desc"]
    goal_amount = round(Decimal(request.data["goal_amount"]), 2)
    saved_amount = round(Decimal(request.data["saved_amount"]), 2)
    goal_complete_date = request.data["goal_complete_date"]
    goal_set_on = request.data["goal_set_on"]

    try:
        Goal.objects.create(goal_title=goal_title, goal_desc=goal_desc, goal_amount=goal_amount, saved_amount=saved_amount, goal_complete_date=goal_complete_date, goal_set_on=goal_set_on, by_user=user)
        return Response({"MSSG": "GOAL_SET"}, status=status.HTTP_200_OK)
    except:
        return Response({"MSSG": "FAILED_TO_SET"}, status=status.HTTP_400_BAD_REQUEST)
