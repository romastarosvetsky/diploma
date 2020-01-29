from rest_framework import serializers

from authapp import models as auth_models
from central import models as central_models


class JobSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    additional_load_method = serializers.CharField(required=False)
    additional_method_value = serializers.IntegerField(required=False)
    validator_methods = serializers.ListField(required=False, child=serializers.CharField())
    validator_values = serializers.ListField(required=False, child=serializers.IntegerField())
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = central_models.Job
        fields = ['id', 'section', 'lesson_type', 'common_id', 'description', 'dimension', 'factor',
                  'additional_load_method', 'additional_method_value', 'validator_methods', 'validator_values']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.Teacher
        fields = '__all__'

    def create(self, validated_data):
        key_fields = ['name', 'surname']
        assertion_data = dict([(key, validated_data.pop(key)) for key in key_fields])
        instance, _ = auth_models.Teacher.objects.update_or_create(**assertion_data, defaults=validated_data)
        return instance


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = central_models.Discipline
        fields = '__all__'

    def create(self, validated_data):
        instance, _ = central_models.Discipline.objects.update_or_create(name=validated_data['name'],
                                                                         semesters=validated_data['semesters'],
                                                                         defaults=validated_data)
        return instance


class LoadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    result_value = serializers.FloatField(required=False)

    class Meta:
        model = central_models.Load
        fields = ['id', 'input_value', 'result_value']


class DisciplineLoadSerializer(serializers.Serializer):
    """
    res = {
        'teacher': {
            'name'
            'surname'
            'patronymic'
            'faculty'
            'department'
        },
        'discipline': {
            'name'
            'semesters'
        },
        'jobs': [
            {
                'id'
                'input_value'
                'result_value'
            }, ...
        ]
    }"""

    teacher = TeacherSerializer()
    discipline = DisciplineSerializer()
    jobs = LoadSerializer(many=True)

    def create(self, validated_data):
        teacher_data = validated_data.pop('teacher')
        teacher_serializer = TeacherSerializer(data=teacher_data)
        teacher_serializer.is_valid(raise_exception=True)
        teacher = teacher_serializer.save()
        discipline_data = validated_data.pop('discipline')
        discipline_serializer = DisciplineSerializer(data=discipline_data)
        discipline_serializer.is_valid(raise_exception=True)
        discipline = discipline_serializer.save()
        objects = []
        for job in validated_data.pop('jobs'):
            instance = central_models.Load.objects.create(discipline_id=discipline.id,
                                                          teacher_id=teacher.id,
                                                          job_id=job['id'],
                                                          input_value=job['input_value'],
                                                          result_value=job['result_value'])
            objects.append(instance)
        return objects
