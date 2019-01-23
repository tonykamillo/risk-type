import json
from django.urls import reverse
from django.test import TestCase
from . import get_risk_type_data, get_insurance_data
from ..models import RiskType, Insurance


class RiskTypeTestCase(TestCase):

    def make_risk_type_post(self):
        return self.client.post(
            reverse('risk-type'),
            json.dumps(get_risk_type_data()),
            content_type='application/json'
        )

    def test_create_risk_type(self):

        response = self.make_risk_type_post()
        data = response.json()
        print(response)
        print(data)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertEqual(RiskType.objects.filter(pk=data.get('uuid')).count(), 1)

    def test_get_risk_type_list(self):

        self.make_risk_type_post()

        response = self.client.get(reverse('risk-type'))
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), RiskType.objects.count())

    def test_get_single_risk_type(self):
        risk_type = self.make_risk_type_post().json()
        response = self.client.get(reverse('insurance', kwargs={'pk': risk_type.get('uuid')}))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)

    def test_create_insurance(self):

        risk_type_data = self.make_risk_type_post().json()

        payload = json.dumps(get_insurance_data(risk_type_data))

        response = self.client.post(
            reverse('insurance', kwargs={'pk': risk_type_data.get('uuid')}),
            payload,
            content_type='application/json'
        )

        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertEqual(Insurance.objects.filter(pk=data.get('uuid')).count(), 1)

    def test_risk_type_not_allowed_method(self):

        self.make_risk_type_post()

        put_response = self.client.put(reverse('risk-type'), {}, content_type='application/json')
        self.assertEqual(put_response.status_code, 405)

        put_response = self.client.put(
            reverse('insurance', kwargs={'pk': RiskType.objects.last().uuid}),
            {}, content_type='application/json')

        self.assertEqual(put_response.status_code, 405)
