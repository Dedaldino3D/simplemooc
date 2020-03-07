import re

import django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.db import models
from django.db import models, connection
from django.db.models.fields.related import ManyToManyRel
from django.utils.translation import ugettext_lazy as _

from django.conf import settings


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    VALIDATOR = [validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                           _('O nome de usuário só pode conter letras, '
                                             'digítos e os seguintes caracteres: /@/./+/-/_/'),
                                           'invalid')]

    username = models.CharField(verbose_name=_('nome de usuário'), max_length=30, unique=True,
                                validators=VALIDATOR)
    name = models.CharField(verbose_name=_('nome'), max_length=100, blank=True)
    email = models.EmailField(verbose_name=_('e-mail'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name=_('data de entrada'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')


class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('usuário'), related_name='resets',
                             on_delete=models.CASCADE)
    key = models.CharField(_('chave'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    confirmed = models.BooleanField(_('confirmado?'), default=False, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = _('nova senha')
        verbose_name_plural = _('novas senhas')
        ordering = ['-created_at']
