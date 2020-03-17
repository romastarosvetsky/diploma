from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers as api_serializers
from central import models as central_models


class CreateLoadView(CreateAPIView):

    queryset = central_models.Load.objects.all()
    serializer_class = api_serializers.DisciplineLoadSerializer
    permission_classes = [IsAuthenticated, ]

    def get_additional_load_method(self, name):
        def noop(value, *args):
            return value
        if not isinstance(name, str):
            return noop
        return getattr(central_models.Job, name, noop)

    def get_validators(self, names):
        return [getattr(central_models.Job, name, lambda *args: True) if isinstance(name, str) else lambda *args: True for name in names]

    def validated(self, input_value, methods, values):
        validator_methods = self.get_validators(methods)
        return all([method(input_value, value) for method, value in zip(validator_methods, values)])

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
            if not self.validated(job['input_value'], job_instance.validator_methods, job_instance.validator_values):
                return Response(data={'detail': _('Input value invalid. Validation failure')},
                                status=status.HTTP_400_BAD_REQUEST)
            value = job['input_value'] * job_instance.factor
            method = self.get_additional_load_method(job_instance.additional_load_method)
            value = method(value, job_instance.additional_method_value)
            response_data[job['id']] = value
        self.do_create(serializer.data, response_data)
        return Response(response_data, status=status.HTTP_200_OK)


class JobViewSet(viewsets.ModelViewSet):

    queryset = central_models.Job.objects.all()
    serializer_class = api_serializers.JobSerializer
    permission_classes = [IsAuthenticated, ]


class LogInAPIView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (username and password) is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        return Response({'details': 'Credentials are invalid.'}, status=status.HTTP_400_BAD_REQUEST)
