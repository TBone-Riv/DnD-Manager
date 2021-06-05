from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    TemplateView,
    UpdateView,
)

from .form import CustomUserCreationForm, CustomUserChangeForm


class HomeView(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy("profile:login")
    template_name = "placeholder.html"


class CustomLoginView(LoginView):

    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):

    template_name = "registration/logout.html"


class CreateCustomUserView(CreateView):

    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("profile:home")

    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context

    def get_redirect_url(self):
        """Return the user-originating redirect URL."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return redirect_to


class UpdateCustomUserView(LoginRequiredMixin, UpdateView):

    template_name = "registration/account.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("profile:account")

    def get_object(self, queryset=None):
        return self.request.user
