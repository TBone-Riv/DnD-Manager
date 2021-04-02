from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Campaign, Character, Session
from .form import CampaignForm, CharacterForm, SessionForm


class CampaignListView(LoginRequiredMixin, ListView):

    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class CampaignDetailView(LoginRequiredMixin, DetailView):

    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/view.html"


class CampaignCreateView(LoginRequiredMixin, CreateView):

    form_class = CampaignForm
    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class CampaignUpdateView(LoginRequiredMixin, UpdateView):

    form_class = CampaignForm
    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.creator:
            return redirect("profile:campaign", pk=self.kwargs.get("pk"))
        return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     return  super().get_queryset().get_object_or_404(creator=self.request.user)


class CharacterListView(LoginRequiredMixin, ListView):

    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class CharacterDetailView(LoginRequiredMixin, DetailView):

    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/view.html"


class CharacterCreateView(LoginRequiredMixin, CreateView):

    form_class = CharacterForm
    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instence.creator = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class CharacterUpdateView(LoginRequiredMixin, UpdateView):

    form_class = CharacterForm
    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/update.html"

    def get(self, request, *args, **kwargs):
        view = super().get(request, *args, **kwargs)
        if self.request.user != self.object.creator:
            return redirect(CharacterDetailView, pk=self.request.POST.get("pk"))
        return view


class SessionListView(LoginRequiredMixin, ListView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "session/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)


class SessionDetailView(LoginRequiredMixin, DetailView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "Session/view.html"


class SessionCreateView(LoginRequiredMixin, CreateView):

    form_class = SessionForm
    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "Session/create.html"

    def post(self, request, *args, **kwargs):
        self.campaign = Campaign.objects.get_object_or_404(
            id=self.kwargs.get("pk"),
            creator=self.request.user
        )
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.creator = self.request.user
        form.instance.for_campaign = self.campaign
        self.object = form.save()
        # SessionsPlayerStatus ?? dans save
        return super().form_valid(form)


class SessionUpdateView(LoginRequiredMixin, UpdateView):

    form_class = SessionForm
    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "Session/update.html"

    def get(self, request, *args, **kwargs):
        view = super().get(request, *args, **kwargs)
        if self.request.user != self.object.creator:
            return redirect(CharacterDetailView, pk=self.request.POST.get("pk"))
        return view
