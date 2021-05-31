from django import forms
from .models import (
    Campaign,
    Character,
    Session
)


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ["parent", "attachment", "creator", "status"]


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = ["parent", "attachment", "creator", "status", "in_campaign"]


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ["parent", "attachment", "creator", ]
