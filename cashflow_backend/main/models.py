from django.db import models
from django.contrib.auth.models import User
# Category:
# - category_name
# - category_used_count
# - user

# Expenditure:
# - expenditure_title
# - amt
# - remrks
# - date
# - belongs_to_category
# - user

# ExpenditureReceipt:
# - img
# - expenditure_title
# - user

# Reminder:
# - reminder_title
# - reminder_desc
# - amount
# - due_date
# - pic_of_bill(optional)
# - user

# Goal:
# - goal_title 
# - goal_desc 
# - goal_amount
# - saved_amount
# - goal_complete_date
# - goal_set_on
# - by_user

class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_used_count = models.IntegerField()
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category_name} by {self.user.username}"

class Expenditure(models.Model):
    expenditure_title = models.CharField(max_length=200)
    expenditure_amount = models.DecimalField(max_digits=7, decimal_places=2)
    expenditure_remarks = models.TextField(blank=True, null=True)
    expenditure_date = models.DateField()
    belongs_to_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.expenditure_title} for {self.by_user.username}"

def get_receipt_filename(instance, filename):
    username = instance.by_user.username

    return f"ExpenditureReceipts/{username}/{filename}"

class ExpenditureReceipt(models.Model):
    expenditure_title = models.CharField(max_length=200, null=True, blank=True)
    receipt_pic = models.FileField(upload_to=get_receipt_filename)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"receipt for {self.expenditure_title}"

def get_bill_filename(instance, filename):
    username = instance.by_user.username

    return f"ReminderBills/{username}/{filename}"

class Reminder(models.Model):
    reminder_title = models.CharField(max_length=200)
    reminder_desc = models.TextField(blank=True, null=True)
    reminder_amount = models.DecimalField(max_digits=7, decimal_places=2)
    reminder_due_date = models.DateField()
    pic_of_bill = models.FileField(upload_to=get_bill_filename, blank=True)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reminder {self.reminder_title} for {self.by_user.username}"

class Goal(models.Model):
    goal_title = models.CharField(max_length=200)
    goal_desc = models.TextField(blank=True, null=True)
    goal_amount = models.DecimalField(max_digits=7, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=7, decimal_places=2)
    goal_complete_date = models.DateField()
    goal_set_on = models.DateField()
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Goal {self.goal_title} for {self.by_user.username}"