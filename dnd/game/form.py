from django import forms
from .models import (
    Campaign,
    Character,
    Session
)


class CampaignForm(forms):
    class Meta:
        model = Campaign
        fields = []


class SessionForm(forms):
    class Meta:
        model = Session
        fields = []


class CharacterForm(forms):
    class Meta:
        model = Character
        fields = []
