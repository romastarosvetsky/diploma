from django.test import TestCase
from rest_framework import test as rf_test, status

from central import models as central_models
from authapp import models as auth_models


class BaseTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = rf_test.APIClient()


class TestCreateLoadView(BaseTest):

    def test_create_multiple_loads_success(self):
        data = {
            'teacher': {
                'name': 'Иван',
                'surname': 'Иванов'
            },
            'discipline': {
                'name': 'Математика',
                'semester': 1
            },
            'jobs': [
                {'id': 1, 'input_value': 25},
                {'id': 2, 'input_value': 25},
            ]
        }
        central_models.Job.objects.create(section='student', common_id='student', factor=3)
        central_models.Job.objects.create(section='student', common_id='student', factor=10)
        response_1 = self.client.post('/api/create_load/', data=data, format='json')
        response_2 = self.client.post('/api/create_load/', data=data, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(auth_models.Teacher.objects.count(), 1)
        self.assertEqual(central_models.Load.objects.count(), 4)
        self.assertEqual(central_models.Discipline.objects.count(), 1)
