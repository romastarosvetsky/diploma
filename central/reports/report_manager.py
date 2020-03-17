from django.db.models import Max, OuterRef, Subquery, Q, Sum, F

from central.models import Load, Job


class ReportManager:

    def __init__(self, writer):
        self.writer = writer

    @staticmethod
    def get_valid_loads():
        distinct_values = Load.objects.values('teacher__id', 'discipline__id', 'job__id').annotate(
            max_date=Max('created_at')).filter(
            teacher__id=OuterRef('teacher__id'), discipline__id=OuterRef('discipline__id'),
            job__id=OuterRef('job__id'),
            max_date=OuterRef('created_at'))
        valid_loads = Load.objects.select_related('teacher', 'discipline').filter(
            teacher__id=Subquery(distinct_values.values('teacher__id')[:1]),
            discipline__id=Subquery(distinct_values.values('discipline__id')[:1]),
            job__id=Subquery(distinct_values.values('job__id')[:1]),
            created_at=Subquery(distinct_values.values('max_date')[:1]))
        return valid_loads

    def get_semesters_load_report(self, semesters):
        valid_loads = self.get_valid_loads().filter(discipline__semester__in=semesters)
        fields = (Job.LECTURE, Job.LAB, Job.CREDIT, Job.PRACTICE_LESSONS, Job.COURSE_WORKS, Job.CONSULTATION,
                  Job.CREDIT, Job.EXAM, Job.MAGISTRACY, Job.REVIEW, Job.OTHER)
        annotations = {}
        for i, semester in enumerate(semesters):
            annotations.update(
                {f'{field}_sum_{i}': Sum('result_value',
                                         filter=Q(job__lesson_type=f'{field}') & Q(discipline__semester=f'{semester}'))
                 for field in fields}
            )
        all_semesters_fields = [Job.DIPLOMA, Job.GOV_EXAM, Job.GEC_DIPLOMA, Job.PRACTICE]
        all_semesters_annotations = {f'{field}_sum': Sum('result_value', filter=Q(job__lesson_type=f'{field}'))
                                     for field in all_semesters_fields}
        teachers_loads = valid_loads.values('teacher_id') \
            .annotate(**annotations, **all_semesters_annotations).values(
            'teacher__name', 'teacher__surname', *annotations.keys(), *all_semesters_annotations.keys())
        self.writer.write_lines(teachers_loads)
        return self.writer.get_result()
