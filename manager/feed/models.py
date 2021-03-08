from django.db import models
from django.utils.translation import gettext_lazy as _
from constant import title_validator


class Like(models.Model):

    user = models.ForeignKey(
        'profile.CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='liked_by',
    )
    post = models.ForeignKey(
        'Post',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='liked_post',
    )

    class Meta:
        unique_together = ('user', 'post',)


class Post(models.Model):

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

    parent = models.ForeignKey(
        'Post',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='post_parent',
    )
    attachment = models.ForeignKey(
        'Post',
        unique=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='attached_post',
    )
    creator = models.ForeignKey(
        'profile.CustomUser',
        unique=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='creator',
    )


class PostText(models.Model):

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

    post = models.OneToOneField(
        'Post',
        unique=True,
        on_delete=models.CASCADE,
        related_name='text_of'
    )

