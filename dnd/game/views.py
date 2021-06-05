from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)
from dnd.base.constant import (
    STATUS_CAMPAIGN,
)

from .models import Campaign, Character, Session, SessionsCharacterStatus


# CAMPAIGN VIEW ===============================================================
# Campaign detail. "campaign"
class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/view.html"


# List of campaign for a user name. "list-campaign"
class CampaignListView(LoginRequiredMixin, ListView):

    model = Campaign
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            creator=get_object_or_404(
                get_user_model(),
                username=self.kwargs.get("user_name")
            )
        )


# Campaign creation. "new-campaign"
class CampaignCreateView(LoginRequiredMixin, CreateView):

    model = Campaign
    fields = [
        "title",
        "details",
        "link_world",
        "default_link_vtable",
        "default_link_vocal",
        "master", "max_player", "status",
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/create.html"

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        form.initial['master'] = self.request.user
        form.initial['status'] = STATUS_CAMPAIGN.OPEN
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Campaign Update. Access only if user = creator else redirect to detail.
# "my-campaign"
class CampaignUpdateView(LoginRequiredMixin, UpdateView):

    model = Campaign
    fields = [
        "title",
        "details",
        "link_world",
        "default_link_vtable",
        "default_link_vocal",
        "master", "max_player", "status",
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/update.html"

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().creator:
            return redirect("game:campaign", pk=self.kwargs.get("pk"))
        return super().get(request, *args, **kwargs)
# END CAMPAIGN VIEW ===========================================================


# CHARACTER VIEW ==============================================================
# Character detail. "character"
class CharacterDetailView(LoginRequiredMixin, DetailView):

    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/view.html"


# List of character for a user name. "list-character"
class CharacterListView(LoginRequiredMixin, ListView):

    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "character/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            creator=get_object_or_404(
                get_user_model(),
                username=self.kwargs.get("user_name")
            )
        )


# List of character for a campaign. "list-campaign-character"
class CharacterCampaignListView(LoginRequiredMixin, ListView):

    model = Character
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/add_player.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            in_campaign=get_object_or_404(
                Campaign,
                id=self.kwargs.get("pk")
            )
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            characters=Character.objects.filter(
                in_campaign=None,  # Not already in a campaign
            ).exclude(  # Not already in this campaign
                creator__in=[
                    character.creator for character in self.get_queryset()
                ]
            )
        )

    def post(self, request, *args, **kwargs):
        character = Character.objects.get(
            id=self.request.POST.get('new_character'))
        character.in_campaign = Campaign.objects.get(id=self.kwargs.get("pk"))
        character.save()
        return super().get(request, *args, **kwargs)


# Character creation. "new-character"
class CharacterCreateView(LoginRequiredMixin, CreateView):

    model = Character
    fields = [
        "name",
        "character_class",
        "character_race",
        "character_level",
        "details"
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "character/create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


# Character Update. Access only if user = creator else redirect to detail.
# "my-character"
class CharacterUpdateView(LoginRequiredMixin, UpdateView):

    model = Character
    fields = [
        "name",
        "character_class",
        "character_race",
        "character_level",
        "details"
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "character/update.html"

    def get(self, request, *args, **kwargs):
        view = super().get(request, *args, **kwargs)
        if self.request.user != self.object.creator:
            return redirect("game:character", pk=self.kwargs.get("pk"))
        return view
# END CHARACTER VIEW ==========================================================


# SESSION VIEW ================================================================
# Session detail. "session"
class SessionDetailView(LoginRequiredMixin, DetailView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "session/view.html"


# List of session for a user name. "list-session"
class SessionListView(LoginRequiredMixin, ListView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "session/list.html"

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(),
            username=self.kwargs.get("user_name")
        )
        return super().get_queryset().filter(
            for_campaign__in=[
                campaign for campaign in
                Campaign.objects.filter(master=user)
                             ] + [
                character.in_campaign for character in
                Character.objects.filter(creator=user)
            ]
        )


# List of session for a campaign. "list-campaign-session"
class SessionCampaignListView(LoginRequiredMixin, ListView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "campaign/add_session.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            for_campaign=Campaign.objects.get(id=self.kwargs.get("pk"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["creator"] = Campaign.objects.get(
            id=self.kwargs.get("pk")
        ).creator

        return context


# List of session for a character. "list-character-session"
class SessionCharacterListView(LoginRequiredMixin, ListView):

    model = Session
    login_url = reverse_lazy("profile:login")
    template_name = "session/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(
            for_campaign=Character.objects.get(
                id=self.kwargs.get("pk")
            ).in_campaign
        )


# Session creation. "new-session"
class SessionCreateView(LoginRequiredMixin, CreateView):

    model = Session
    fields = [
        "title",
        "date",
        "link_vtable",
        "link_vocal"
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "Session/create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.creator = self.request.user

        form.instance.for_campaign = Campaign.objects.get(
            id=self.kwargs.get("pk"),
            creator=self.request.user
        )

        return super().form_valid(form)


# Session Update. Access only if user = creator else redirect to detail.
# "my-session"
class SessionUpdateView(LoginRequiredMixin, UpdateView):

    model = Session
    fields = [
        "title",
        "date",
        "link_vtable",
        "link_vocal"
    ]
    login_url = reverse_lazy("profile:login")
    template_name = "Session/update.html"

    def get(self, request, *args, **kwargs):
        view = super().get(request, *args, **kwargs)
        if self.request.user != self.object.creator:
            return redirect("game:session", pk=self.kwargs.get("pk"))
        return view


class SessionStatusUpdateView(LoginRequiredMixin, UpdateView):

    model = SessionsCharacterStatus
    fields = ["status"]
    login_url = reverse_lazy("profile:login")
    template_name = "Session/vote.html"
    success_url = "/"

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(
            session=self.kwargs.get("pk"),
            character__in=Character.objects.filter(creator=self.request.user)
        )

        return queryset.get()
