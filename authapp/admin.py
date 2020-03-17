from django.contrib import admin

from authapp import models


class TeacherModelAdmin(admin.ModelAdmin):

    list_display = ['name', 'surname', 'patronymic', 'faculty', 'department']


admin.site.register(models.Teacher, TeacherModelAdmin)
