from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from central import models
from central.reports.report_manager import ReportManager
from central.reports.report_writer import CSVCommonReportResponseWriter


class ValidLoadFilter(SimpleListFilter):
    title = _('Valid ones')
    parameter_name = 'qwerty'

    def queryset(self, request, queryset):
        if self.value() == 'valid':
            valid_loads = ReportManager.get_valid_loads()
            return valid_loads
        return queryset

    def lookups(self, request, model_admin):
        return (
            ('valid', _('Actual loads')),
        )


class JobModelAdmin(ModelAdmin):
    search_fields = ['id', 'common_id', 'section', 'description', 'dimension', 'factor', ]
    list_display = ['id', 'common_id', 'section', 'description', 'dimension', 'factor', ]
    list_display_links = ['id', 'common_id', 'section', 'description', 'dimension', 'factor', ]
    ordering = ['common_id', ]
    list_filter = ['section', ]


class DisciplineModelAdmin(ModelAdmin):
    list_display = ['id', 'name', 'semester', ]
    search_fields = ['id', 'name', 'semester', ]
    ordering = ['-semester']


class LoadModelAdmin(ModelAdmin):

    change_list_template = 'central/load_change_list.html'
    list_display = ['teacher', 'discipline', 'job', 'input_value', 'created_at']
    search_fields = ['teacher', 'discipline', 'job', 'input_value']
    fields = ['teacher', 'discipline', 'job', 'input_value', 'result_value', 'created_at']
    readonly_fields = ['created_at']
    list_filter = [ValidLoadFilter, ]

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            year = request.POST.get('year', None)
            if year is not None and year != '':
                year = int(year)
                base_year = models.Discipline.FIRST_SEMESTER_YEAR
                if base_year - year >= 2:
                    return Response({'detail': 'Data for provided year can not be received.'},
                                    status=status.HTTP_404_NOT_FOUND)
                last_semester = (year - base_year + 1) * 2
                semesters = (last_semester - 1 if last_semester != 0 else 0, last_semester)
                writer = CSVCommonReportResponseWriter()
                return ReportManager(writer).get_semesters_load_report(semesters)
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(models.Discipline, DisciplineModelAdmin)
admin.site.register(models.Job, JobModelAdmin)
admin.site.register(models.Load, LoadModelAdmin)
