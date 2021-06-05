from datetime import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from os.path import splitext


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
    if (datetime.today().year - value.year) > 200:
        raise ValidationError(
            _('Enter a valid date.'),
            code='to_old')
    if (datetime.today().year - value.year) < 14:
        raise ValidationError(
            _('Enter a valid date.'),
            code='to_young')


def extension_validator(value):
    if splitext(value.name)[1] != '.pdf':
        raise ValidationError(
            _('Wrong file extension'),
            code='bad_extension')
