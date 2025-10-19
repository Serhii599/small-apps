from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView

from .forms import CustomUserCreationForm


class UsersListView(LoginRequiredMixin, ListView):
    pass

class UserRegisterView(SuccessMessageMixin, FormView):
    template_name = "authentication/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('apps.authentication:login')
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()


class UserLoginView(BaseLoginView):
    pass

class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass
