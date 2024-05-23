from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from authentication.forms import RegisterForm


class Login(LoginView, SuccessMessageMixin):
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, f"Welcome {self.request.user.get_short_name()}!")
        return response

    def get_success_url(self):
        return reverse_lazy("index")

    def get_template_names(self):
        if self.request.htmx:
            return ["registration/forms/login.html"]
        return super().get_template_names()


class Logout(LogoutView, SuccessMessageMixin):
    next_page = reverse_lazy("index")
    success_message = "You have successfully logged out."


class Register(FormView):
    form_class = RegisterForm
    redirect_authenticated_user = True
    template_name = "registration/register.html"

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        messages.warning(
            self.request,
            "Registered successfully!\n "
            "We've notified a moderator to activate your account!",
        )
        return response

    def get_success_url(self) -> str:
        return reverse_lazy("index")

    def get_template_names(self) -> list:
        if self.request.htmx:
            return ["registration/forms/register.html"]
        return super().get_template_names()
