from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserChangeForm(UserCreationForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email',
                  'first_name', 'last_name', 'birth_date']