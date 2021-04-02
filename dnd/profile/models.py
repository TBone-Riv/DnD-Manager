from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from dnd.base.validator import (
    date_validator,
    discord_validator,
)


class CustomUser(AbstractUser):

    birth_date = models.DateField(
        _('birth date'),
        unique=False,
        help_text=_('Enter your date of birth dd/mm/yyyy'),
        validators=[date_validator],
        error_messages={
            'to_old': _("You should not lie about your age"),
            'to_young': _("Sorry you legally can not register on social media")
        }
    )
    discord = models.CharField(
        'discord',
        max_length=150,
        unique=False,
        blank=True,
        default="",
        help_text='username#0000',
        validators=[discord_validator],
        error_messages={
            'invalid': _("Invalid discord username. It must be formatted like "
                         "this : username#0000"),
        }
    )
    status_open_master = models.BooleanField(
        _('open to master'),
        unique=False,
        default=False,
    )
    status_open_player = models.BooleanField(
        _('open to play'),
        unique=False,
        default=False,
    )
