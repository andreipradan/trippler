from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from django_htmx.http import retarget

from expenses.forms import DebtFormSet, ExpenseForm
from expenses.models import Expense


def clear_messages(request):  # noqa: ARG001
    return HttpResponse("")


class ExpenseListView(LoginRequiredMixin, CreateView):
    form_class = ExpenseForm
    model = Expense
    success_url = reverse_lazy("expenses")
    template_name = "expenses/expense_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["formset"] = DebtFormSet(self.request.POST or None)
        context["object_list"] = super().get_queryset()
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs["initial"]["payer"] = self.request.user
        kwargs["initial"]["currency"] = self.request.user.currency
        return form_class(**kwargs)

    def form_invalid(self, form):
        context = super().get_context_data(form=form)
        return self.response_class(
            request=self.request,
            template=["expenses/partials/add_expense_form.html"],
            context=context,
            using=self.template_engine,
            content_type=self.content_type,
        )

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Expense saved successfully!")
        context = self.get_context_data(form=form)
        if context["object_list"].count() <= 1:
            return retarget(
                self.response_class(
                    request=self.request,
                    template=["expenses/partials/expense_list_body.html"],
                    context=context,
                    using=self.template_engine,
                    content_type=self.content_type,
                ),
                "#expense-body",
            )
        return retarget(
            self.response_class(
                request=self.request,
                template=["expenses/partials/expense_accordion.html"],
                context=context,
                using=self.template_engine,
                content_type=self.content_type,
            ),
            "#expense-list",
        )


class ExpenseDetailView(DeleteView):
    model = Expense
    success_url = reverse_lazy("expenses")
    template_name = "expenses/partials/expense_list_body.html"

    def delete(self, request, *args, **kwargs):  # noqa: ARG002
        self.object = self.get_object()
        self.object.delete()
        object_list = Expense.objects.all()
        context = super().get_context_data(object_list=object_list)
        response = self.render_to_response(context=context)
        if not object_list.exists():
            return retarget(response, "#expense-body")
        return response
