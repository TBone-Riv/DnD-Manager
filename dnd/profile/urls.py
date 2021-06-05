from django.urls import path

from .views import (
    CreateCustomUserView,
    CustomLoginView,
    CustomLogoutView,
    UpdateCustomUserView,
    HomeView,
)

app_name = "profile"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('account', UpdateCustomUserView.as_view(), name="account"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', CustomLogoutView.as_view(), name="logout"),
    path('register', CreateCustomUserView.as_view(), name="register"),
]
