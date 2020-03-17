import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from authapp import models as auth_models


class TimeCreationMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name=_('Created at'), null=True, blank=False, auto_now_add=True)


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
    LAB = 'lab'
    PRACTICE_LESSONS = 'practice_lessons'
    COURSE_WORKS = 'course_works'
    CONSULTATION = 'consultation'
    CREDIT = 'credit'
    EXAM = 'exam'
    MAGISTRACY = 'magistracy'
    REVIEW = 'review'
    DIPLOMA = 'diploma'
    GOV_EXAM = 'gov_exam'
    GEC_DIPLOMA = 'gec_diploma'
    PRACTICE = 'practice'

    LESSON_CHOICES = (
        (LECTURE, _('Lecture')),
        (LAB, _('Laboratory class')),
        (PRACTICE_LESSONS, _('Practice lessons')),
        (COURSE_WORKS, _('Course works')),
        (CONSULTATION, _('Consultation')),
        (CREDIT, _('Credit')),
        (EXAM, _('Exam')),
        (MAGISTRACY, _('Magistracy')),
        (REVIEW, _('Review')),
        (DIPLOMA, _('Diploma heading')),
        (GOV_EXAM, _('Gov exam')),
        (GEC_DIPLOMA, _('GEC diploma')),
        (PRACTICE, _('Practice')),
        (OTHER, _('Other')),
    )

    ADDITIONAL_LOAD_METHODS_CHOICES = (
        ('add_value', _('Add value')),
        ('substr_value', _('Subtract value'))
    )

    section = models.CharField(max_length=64, verbose_name=_('Job section'), null=False, blank=False,
                               choices=JOB_CHOICES)
    lesson_type = models.CharField(max_length=64, verbose_name=_('Lesson type'), null=False, blank=False,
                                   choices=LESSON_CHOICES)
    common_id = models.CharField(max_length=32, verbose_name=_('Number'), null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'))
    dimension = models.CharField(max_length=256, verbose_name=_('Relate to'), null=False, blank=False)
    factor = models.FloatField(verbose_name=_('Factor'), null=False, blank=False)
    additional_load_method = models.CharField(max_length=256, null=True, blank=True,
                                              choices=ADDITIONAL_LOAD_METHODS_CHOICES)
    additional_method_value = models.FloatField(null=True, blank=True)
    validator_methods = ArrayField(max_length=5, base_field=models.CharField(max_length=256), default=list, blank=True)
    validator_values = ArrayField(max_length=5, base_field=models.FloatField(), default=list, blank=True)

    def __str__(self):
        return f"{self.common_id} {self.description}"

    @staticmethod
    def add_value(source, additional):
        return source + additional

    @staticmethod
    def substr_value(source, additional):
        return source - additional

    @staticmethod
    def is_eql(source, value):
        return source == value

    @staticmethod
    def is_less_or_eql(source, value):
        return source <= value

    @staticmethod
    def is_less(source, value):
        return source < value

    @staticmethod
    def is_greater_or_eql(source, value):
        return source >= value

    @staticmethod
    def is_greater(source, value):
        return source > value


class Discipline(models.Model):

    FIRST_SEMESTER_YEAR = 2019

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _('Disciplines')

    name = models.CharField(max_length=128, null=False, blank=False, verbose_name=_('Discipline name'))
    semester = models.IntegerField(null=False, blank=False, verbose_name=_('Semester'))

    @property
    def semester_start_date(self):
        year = self.FIRST_SEMESTER_YEAR + self.semester // 2
        month = '01' if self.semester % 2 == 0 else '09'
        return datetime.datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d').date()

    @property
    def semester_end_date(self):
        year = self.FIRST_SEMESTER_YEAR + self.semester // 2
        month = '05' if self.semester % 2 == 0 else '12'
        return datetime.datetime.strptime(f'{year}-{month}-31', '%Y-%m-%d').date()

    def __str__(self):
        return f"{self.name}, {self.semester_start_date} - {self.semester_end_date}"


class Load(models.Model):

    class Meta:
        verbose_name = _('Load')
        verbose_name_plural = _('Loads')

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    teacher = models.ForeignKey(auth_models.Teacher, on_delete=models.DO_NOTHING, verbose_name=_('Teacher'))
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING, verbose_name=_('Discipline'))
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, verbose_name=_('Job'))
    input_value = models.FloatField(null=False, blank=False, verbose_name=_('Input value'))
    result_value = models.FloatField(null=True, blank=True, verbose_name=_('Result value'))
