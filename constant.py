from datetime import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from extended_choices import Choices
from os.path import splitext

# profile/model
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

# validator
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


def extension_validator(value):
    ext = splitext(value.name)[1]
    if splitext(value.name)[1] != '.pdf':
        raise ValidationError(
            _('Wrong file extension'),
            code='bad_extension')
