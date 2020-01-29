from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from authapp import models as auth_models


class TimeCreationMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name=_('Created at'), null=False, blank=False, auto_now_add=True)


class Job(TimeCreationMixin):

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    STUDENT_JOB = 'student'
    IIFO_JOB = 'iifo'
    MAGISTRACY_JOB = 'magistracy'
    LEARNING_METODICAL_JOB = 'learning_metodical'
    ORGANIZE_METODICAL_JOB = 'organize_metodical'
    SCIENTIFIC_JOB = 'scientific'
    OTHER = 'other'

    JOB_CHOICES = (
        (STUDENT_JOB, _('Student job')),
        (IIFO_JOB, _('IIFO job')),
        (MAGISTRACY_JOB, _('Magistracy and graduates job')),
        (LEARNING_METODICAL_JOB, _('Learning metodical job')),
        (ORGANIZE_METODICAL_JOB, _('Organize metodical job')),
        (SCIENTIFIC_JOB, _('Scientific job')),
        (OTHER, _('Other job')),
    )

    LECTURE = 'lecture'
    PRACTICE = 'practice'
    SEMINAR = 'seminar'

    LESSON_CHOICES = (
        (LECTURE, _('Lecture')),
        (PRACTICE, _('Practice')),
        (SEMINAR, _('Seminar')),
    )

    section = models.CharField(max_length=64, verbose_name=_('Job section'), null=False, blank=False,
                               choices=JOB_CHOICES)
    lesson_type = models.CharField(max_length=64, verbose_name=_('Lesson type'), null=False, blank=False,
                                   choices=LESSON_CHOICES)
    common_id = models.CharField(max_length=32, verbose_name=_('Number'), null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'))
    dimension = models.CharField(max_length=256, verbose_name=_('Relate to'), null=False, blank=False)
    factor = models.FloatField(verbose_name=_('Factor'), null=False, blank=False)
    additional_load_method = models.CharField(max_length=256, null=True, blank=True)
    additional_method_value = models.FloatField(null=True, blank=True)
    validator_methods = ArrayField(max_length=5, base_field=models.CharField(max_length=256), default=list)
    validator_values = ArrayField(max_length=5, base_field=models.FloatField(), default=list)

    def __str__(self):
        return f"({self.id}), {_('Relate to')} {self.dimension}, {_('Factor')} {self.factor}"


class Discipline(models.Model):

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _('Disciplines')

    name = models.CharField(max_length=128, null=False, blank=False, verbose_name=_('Discipline name'))
    semesters = ArrayField(max_length=5, base_field=models.IntegerField(), null=False, blank=False, default=list)

    def __str__(self):
        return f"({self.id}), {_('Name')} {self.name}, {_('Semesters')} {self.semesters}"


class Load(models.Model):

    class Meta:
        verbose_name = _('Load')
        verbose_name_plural = _('Loads')

    teacher = models.ForeignKey(auth_models.Teacher, on_delete=models.DO_NOTHING)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    input_value = models.FloatField(null=False, blank=False, verbose_name=_('Input value'))
    result_value = models.FloatField(null=True, blank=True, verbose_name=_('Input value'))
