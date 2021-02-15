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


title_validator = RegexValidator(
    _lazy_re_compile(r'^[-0-9a-zA-Z]*$'),
    message=_('Enter a valid title consisting of letters, number, - and space '
              'only.'),
    code='invalid',
)


class Like(models.Model):

    user = models.ForeignKey(
        'CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='creator',
    )
    post = models.ForeignKey(
        'PostAttachment',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='post',
    )

    class Meta:
        unique_together = ('user', 'post',)


class Post(models.Model):

    parent = models.ForeignKey(
        'PostAttachment',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='parent',
    )
    attachment = models.ForeignKey(
        'PostAttachment',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='Attachment',
    )


class PostText(models.Model, Post):

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
    content = models.TextField(
        _('content'),
        unique=False,
    )
    creation_date = models.DateField(
        _('creation date'),
        unique=False,
        auto_now_add=True,
    )
    update_date = models.DateField(
        _('update date'),
        unique=False,
        auto_now=True,
    )

    creator = models.ForeignKey(
        'CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='creator',
    )

