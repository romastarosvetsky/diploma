from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api import serializers as api_serializers
from central import models as central_models


class CreateLoadView(CreateAPIView):

    queryset = central_models.Load.objects.all()
    serializer_class = api_serializers.DisciplineLoadSerializer

    def get_additional_load_method(self, name):
        # Implementation for additional methods has to be done
        def noop(val, add):
            return val
        return noop

    def do_create(self, data, result_data):
        for ind, job in enumerate(data['jobs']):
            data['jobs'][ind].update({'result_value': result_data[job['id']]})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jobs = serializer.data['jobs']
        response_data = {}
        for job in jobs:
            job_instance = get_object_or_404(central_models.Job, pk=job['id'])
            value = job['input_value'] * job_instance.factor
            method = self.get_additional_load_method(job_instance.additional_load_method)
            value = method(value, job_instance.additional_method_value)
            response_data[job['id']] = value
        self.do_create(serializer.data, response_data)
        return Response(response_data, status=status.HTTP_200_OK)


class JobViewSet(viewsets.ModelViewSet):

    queryset = central_models.Job.objects.all()
    serializer_class = api_serializers.JobSerializer
