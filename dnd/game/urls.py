from django.urls import path

from .views import (
    # CAMPAIGN
    CampaignListView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDetailView,
    # CHARACTER
    CharacterListView,
    CharacterCampaignListView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDetailView,
    # SESSION
    SessionListView,
    SessionCampaignListView,
    SessionCharacterListView,
    SessionCreateView,
    SessionUpdateView,
    SessionDetailView,
    SessionStatusUpdateView
)

app_name = "game"
urlpatterns = [
    # CAMPAIGN
    path('<str:user_name>/campaign', CampaignListView.as_view(),
         name="list-campaign"),
    path('campaign/new', CampaignCreateView.as_view(),
         name="new-campaign"),
    path('campaign/<int:pk>/update', CampaignUpdateView.as_view(),
         name="my-campaign"),
    path('campaign/<int:pk>', CampaignDetailView.as_view(),
         name="campaign"),
    # CHARACTER
    path('<str:user_name>/character', CharacterListView.as_view(),
         name="list-character"),
    path('campaign/<int:pk>/character', CharacterCampaignListView.as_view(),
         name="list-campaign-character"),
    path('character/new', CharacterCreateView.as_view(),
         name="new-character"),
    path('character/<int:pk>/update', CharacterUpdateView.as_view(),
         name="my-character"),
    path('character/<int:pk>', CharacterDetailView.as_view(),
         name="character"),
    # SESSION
    path('<str:user_name>/session/', SessionListView.as_view(),
         name="list-session"),
    path('campaign/<int:pk>/session/', SessionCampaignListView.as_view(),
         name="list-campaign-session"),
    path('character/<int:pk>/session/', SessionCharacterListView.as_view(),
         name="list-character-session"),
    path('campaign/<int:pk>/session/new', SessionCreateView.as_view(),
         name="new-session"),
    path('session/<int:pk>/update', SessionUpdateView.as_view(),
         name="my-session"),
    path('session/<int:pk>/', SessionDetailView.as_view(),
         name="session"),
    path('session/<int:pk>/vote', SessionStatusUpdateView.as_view(),
         name="vote-session"),
]
