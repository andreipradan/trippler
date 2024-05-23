from django.db import models

from trippler.models import DECIMAL_DEFAULT_KWARGS, TimeStampedModel


class Currency(TimeStampedModel):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.code


class Debt(models.Model):
    amount = models.DecimalField(**DECIMAL_DEFAULT_KWARGS)
    currency = models.CharField(max_length=3)
    expense = models.ForeignKey(
        "expenses.Expense",
        on_delete=models.CASCADE,
        related_name="debts",
    )
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        related_name="debts",
    )


class Expense(TimeStampedModel):
    payer = models.ForeignKey("authentication.User", on_delete=models.DO_NOTHING)
    amount = models.DecimalField(**DECIMAL_DEFAULT_KWARGS)
    currency = models.ForeignKey("expenses.Currency", on_delete=models.DO_NOTHING)
    date = models.DateField()
    description = models.CharField(max_length=256, default="")

    class Meta:
        ordering = ("-date", "description")


class Group(TimeStampedModel):
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.DO_NOTHING,
        related_name="created_expense_groups",
    )
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(
        "authentication.User",
        blank=True,
        related_name="expense_groups",
    )
