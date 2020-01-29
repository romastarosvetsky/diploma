from django.db import models
from django.utils.translation import gettext as _


class Teacher(models.Model):

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    name = models.CharField(max_length=64, null=False, blank=False, verbose_name=_('Name'))
    surname = models.CharField(max_length=64, null=False, blank=False, verbose_name=_('Surname'))
    patronymic = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Patronymic'))
    faculty = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Faculty'))
    department = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Department'))
