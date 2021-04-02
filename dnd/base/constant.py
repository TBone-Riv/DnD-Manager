from django.utils.translation import gettext_lazy as _
from extended_choices import Choices


STATUS_CAMPAIGN = Choices(
    ['OPEN', 1, _('open')],
    ['CLOSE', 2, _('close')],
    ['ARCHIVED', 3, _('archived')],
)

STATUS_SESSION = Choices(
    ['WAITING', 1, _('in waiting')],
    ['VALIDATED', 2, _('validated')],
    ['REFUSED', 3, _('refused')],
    ['ARCHIVED', 4, _('archived')],
)
