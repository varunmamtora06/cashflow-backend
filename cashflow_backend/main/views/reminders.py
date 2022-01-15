from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Reminder

from ..serializers.reminders import ReminderSerializer

from ..utils import get_user

from decimal import Decimal

@api_view(['GET'])
def get_reminders(request):
    user = get_user(request)

    reminders = Reminder.objects.filter(by_user=user)
    reminders_serializers = ReminderSerializer(reminders, many=True)

    return Response({"reminders":reminders_serializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_reminder(request):
    user = get_user(request)

    reminder_title = request.data["reminder_title"]
    reminder_desc = request.data["reminder_desc"]
    reminder_amount = round(Decimal(request.data["reminder_amount"]))
    reminder_due_date = request.data["reminder_due_date"]
    pic_of_bill = request.FILES["pic_of_bill"]

    try:
        Reminder.objects.create(reminder_title=reminder_title, reminder_desc=reminder_desc, reminder_amount=reminder_amount, reminder_due_date=reminder_due_date, pic_of_bill=pic_of_bill, by_user=user)
        return Response({"MSSG": "REMINDER_SET"}, status=status.HTTP_200_OK)
    except:
        return Response({"MSSG": "FAILED_TO_SET"}, status=status.HTTP_400_BAD_REQUEST)

