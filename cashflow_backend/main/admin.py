from django.contrib import admin
from .models import Category, Expenditure, ExpenditureReceipt, Reminder, Goal
# Register your models here.

admin.site.register(Category)
admin.site.register(Expenditure)
admin.site.register(ExpenditureReceipt)
admin.site.register(Reminder)
admin.site.register(Goal)