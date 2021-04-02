from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    URLValidator
)

from dnd.base.constant import (
    STATUS_CAMPAIGN,
    STATUS_SESSION,
)
from dnd.base.validator import (
    extension_validator,
    title_validator
)
from dnd.feed.models import Post


class Campaign(Post):

    title = models.CharField(
        _('title'),
        max_length=150,
        unique=False,
        null=False,
        blank=False,
        help_text=_('150 characters or fewer. Letters, number, dash and space '
                    'only.'),
        validators=[title_validator],
        error_messages={
            'invalid': _("Invalid title. letters, numbers, dash and space "
                         "only"),
        }
    )
    max_player = models.PositiveSmallIntegerField(
        _('maximum number of player'),
        unique=False,
        help_text='Number maximum of player in this campaign, 1 to 250',
        validators=[MinValueValidator(1), MaxValueValidator(251)],
        error_messages={
            'max_value': _("250 is the maximum number of player allowed in a "
                           "campaign"),
            'min_value': _("You need to allow a least 1 player to join"),
        }
    )
    status = models.PositiveSmallIntegerField(
        _('status'),
        unique=False,
        choices=STATUS_CAMPAIGN,
        default=STATUS_CAMPAIGN.CLOSE
    )
    link_world = models.CharField(
        'world anvil',
        max_length=250,
        unique=False,
        blank=True,
        help_text='world anvil link',
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )
    default_link_vtable = models.CharField(
        _('virtual table link'),
        max_length=250,
        unique=False,
        blank=True,
        help_text=_('virtual table link'),
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )
    default_link_vocal = models.CharField(
        _('discord voice channel'),
        max_length=250,
        unique=False,
        blank=True,
        help_text=_('discord voice channel link'),
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )
    details = models.TextField(
        _('details'),
        unique=False,
        help_text=_('details'),
    )

    master = models.ForeignKey(
        get_user_model(),
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='master',
    )


class Session(Post):

    title = models.CharField(
        _('title'),
        max_length=150,
        unique=False,
        null=False,
        blank=True,
        help_text=_('150 characters or fewer. Letters, number, dash and space '
                    'only.'),
        validators=[title_validator],
        error_messages={
            'invalid': _("Invalid title. letters, numbers, dash and space "
                         "only"),
        }
    )
    date = models.DateField(
        _('play date'),
        unique=False,
    )
    status = models.PositiveSmallIntegerField(
        _('status'),
        unique=False,
        choices=STATUS_SESSION,
        default=STATUS_SESSION.WAITING
    )

    link_vtable = models.CharField(
        _('virtual table link'),
        max_length=250,
        unique=False,
        blank=True,
        help_text=_('virtual table link'),
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )
    link_vocal = models.CharField(
        _('discord voice channel'),
        max_length=250,
        unique=False,
        blank=True,
        help_text=_('discord voice channel link'),
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )

    for_campaign = models.ForeignKey(
        'Campaign',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='for_campaign',
    )


class Character(Post):

    name = models.CharField(
        _('name'),
        max_length=150,
        unique=False,
        null=False,
        blank=False,
        help_text=_('150 characters or fewer. Letters, number, dash and space '
                    'only.'),
        validators=[title_validator],
        error_messages={
            'invalid': _("Invalid name. letters, numbers, dash and space only"),
        }
    )
    character_class = models.CharField(
        _('class'),
        max_length=150,
        unique=False,
        null=False,
        blank=False,
        help_text=_('150 characters or fewer.'),
    )
    character_race = models.CharField(
        _('race'),
        max_length=150,
        unique=False,
        null=False,
        blank=False,
        help_text=_('150 characters or fewer.'),
    )

    character_level = models.PositiveSmallIntegerField(
        _('character level'),
        unique=False,
        help_text='Number maximum of player in this campaign, 1 to 40',
        validators=[MinValueValidator(1), MaxValueValidator(40)],
        error_messages={
            'max_value': _("40 (two class level 20) is currently the maximum "
                           "level"),
            'min_value': _("You can be level 0"),
        }
    )
    link_sheet = models.CharField(
        _('sheet link'),
        max_length=250,
        unique=False,
        blank=True,
        help_text=_('link to your character sheet'),
        validators=[URLValidator],
        error_messages={
            'invalid': _("Invalid link."),
        }
    )
    pdf_sheet = models.FileField(
        _('sheet pdf'),
        unique=False,
        blank=True,
        help_text=_('pdf of your character sheet'),
        validators=[extension_validator],
        error_messages={
            'invalid': _("Invalid file extension."),
        }
    )
    rule = models.TextField(
        _('rule'),
        unique=False,
        help_text=_('Rule aplided on your charter separat by a ; . Ex : '
                    'PHP+1; Stat array; ... '),
    )
    details = models.TextField(
        _('details'),
        unique=False,
        help_text=_('details'),
    )

    in_campaign = models.ForeignKey(
        'Campaign',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='in_campaign',
    )


class SessionsPlayerStatus(models.Model):

    status = models.PositiveSmallIntegerField(
        _('status'),
        unique=False,
        choices=STATUS_SESSION,
        default=STATUS_SESSION.WAITING
    )
    lock = models.BooleanField(
        _('is locked'),
        default=False
    )
    update_date = models.DateField(
        _('creation date'),
        unique=False,
        auto_now=True,
    )

    session = models.ForeignKey(
        'Session',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='session',
    )
    player = models.ForeignKey(
        'Character',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='player',
    )
