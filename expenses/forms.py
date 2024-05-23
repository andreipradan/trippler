from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from authentication.models import User
from expenses.models import Debt, Expense


class DebtForm(forms.ModelForm):
    class Meta:
        fields = "user", "amount"
        model = Debt
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Amount"},
            ),
        }


class ExpenseForm(forms.ModelForm):
    split_with = forms.ModelMultipleChoiceField(
        label="Split with",
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "selectpicker form-control",
                "data-actions-box": "true",
                "data-live-search": "true",
                "data-style": "border border-secondary",
                "data-virtual-scroll": True,
                "multiple": "",
                "title": "Choose people to split with...",
            },
        ),
    )

    class Meta:
        fields = (
            "amount",
            "currency",
            "date",
            "description",
            "payer",
            "split_with",
        )
        model = Expense
        widgets = {
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Amount"},
            ),
            "currency": forms.Select(
                attrs={
                    "class": "selectpicker form-control",
                    "data-live-search": "true",
                    "data-style": "border border-secondary",
                    "placeholder": "Currency",
                },
            ),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                    "autofocus": "",
                },
            ),
            "payer": forms.Select(
                attrs={
                    "class": "selectpicker form-control",
                    "data-live-search": "true",
                    "data-style": "border border-secondary",
                    "data-virtual-scroll": True,
                },
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.errors:
            attrs = self[field].field.widget.attrs
            attrs.setdefault("class", "form-control")
            attrs["class"] += " is-invalid"
        self.fields["date"].initial = timezone.now()

    def clean_currency(self) -> str:
        currency = self.cleaned_data["currency"]
        currency.code = currency.code.upper()
        return currency


DebtFormSet = inlineformset_factory(
    can_delete=False,
    extra=1,
    form=DebtForm,
    min_num=2,
    model=Debt,
    parent_model=Expense,
)
