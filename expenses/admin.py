from django.contrib import admin

from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    model = Expense
    fields = ("payer", "amount", "currency", "description", "date")
