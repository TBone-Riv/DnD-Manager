from django.urls import path

from .views import (
    CampaignDetailView,
    CampaignCreateView,
    CampaignUpdateView,
    CharacterDetailView,
    CharacterCreateView,
    CharacterUpdateView,
    SessionDetailView,
    SessionCreateView,
    SessionUpdateView
)

app_name = "game"
urlpatterns = [
    path('campaign/<int:pk>/', CampaignDetailView.as_view(),
         name="campaign"),
    path('yourcampaign/<int:pk>/', CampaignUpdateView.as_view(),
         name="my-campaign"),
    path('newcampaign', CampaignCreateView.as_view(),
         name="new-campaign"),
    path('character/<int:pk>/', CharacterDetailView.as_view(),
         name="character"),
    path('yourcharacter/<int:pk>/', CharacterUpdateView.as_view(),
         name="my-character"),
    path('newcharacter', CharacterCreateView.as_view(),
         name="new-character"),
    path('session/<int:pk>/', SessionDetailView.as_view(),
         name="session"),
    path('yoursession/<int:pk>/', SessionUpdateView.as_view(),
         name="my-session"),
    path('campaign/<int:pk>/newsession', SessionCreateView.as_view(),
         name="new-session"),
]