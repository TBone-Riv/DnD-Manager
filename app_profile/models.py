from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import \
    RegexValidator,\
    MinValueValidator, \
    MaxValueValidator, \
    URLValidator
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from extended_choices import Choices

from app_feed.models import PostAttachment


STATUS_CAMPAIGN = Choices(
    ['OPEN', 1, _('open')],
    ['CLOSE', 2, _('close')],
    ['ARCHIVED', 3, _('archived')],
)

STATUS_SESSION = Choices(
    ['WAITING', 1, _('in waiting')],
    ['VALIDATED', 2, _('validated')],
    ['REFUSED', 2, _('refused')],
    ['ARCHIVED', 4, _('archived')],
)


name_validator = RegexValidator(
    _lazy_re_compile(r'^[-a-zA-Z]*$'),
    message=_('Enter a valid word consisting of letters and - only.'),
    code='invalid',
)

discord_validator = RegexValidator(
    _lazy_re_compile(r'.*#[0-9]{4}'),
    message=_('Enter a valid discord username.'),
    code='invalid',
)

title_validator = RegexValidator(
    _lazy_re_compile(r'^[-0-9a-zA-Z]*$'),
    message=_('Enter a valid title consisting of letters, number, - and space '
              'only.'),
    code='invalid',
)


def date_validator(value):
    if (value.year - datetime.today().year) > 200:
        raise ValidationError(
            _('Enter a valid date.'),
            code='to_old')
    if (value.year - datetime.today().year) < 14:
        raise ValidationError(
            _('Enter a valid date.'),
            code='to_young')


class CustomUser(AbstractUser):

    REQUIRED_FIELDS = ['email', 'username']

    lastname = models.CharField(
        _('lastname'),
        max_length=150,
        unique=False,
        help_text=_('150 characters or fewer. Letters only.'),
        validators=[name_validator],
        error_messages={
            'invalid': _("A lastname may only contain letters"),
        }
    )
    firstname = models.CharField(
        _('firstname'),
        max_length=150,
        unique=False,
        help_text=_('150 characters or fewer. Letters only.'),
        validators=[name_validator],
        error_messages={
            'invalid': _("A firstname may only contain letters"),
        }
    )
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


class Campaign(models.Model, PostAttachment):

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
    creation_date = models.DateField(
        _('creation date'),
        unique=False,
        auto_now_add=True,
    )

    creator = models.ForeignKey(
        'CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='creator',
    )
    master = models.ForeignKey(
        'CustomUser',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='master',
    )


class Session(models.Model, PostAttachment):

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
    creation_date = models.DateField(
        _('creation date'),
        unique=False,
        auto_now_add=True,
    )

    campaign = models.ForeignKey(
        'Campaign',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='campaign',
    )


class Character(models.Model, PostAttachment):

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
        validators=[URLValidator],
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
    creation_date = models.DateField(
        _('creation date'),
        unique=False,
        auto_now_add=True,
    )

    creator = models.ForeignKey(
        'CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='creator',
    )
    campaign = models.ForeignKey(
        'Campaign',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='campaign',
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
