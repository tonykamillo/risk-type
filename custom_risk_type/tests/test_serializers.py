from django.test import TestCase
from rest_framework import serializers
from . import get_risk_type_data, get_insurance_data
from ..models import RiskType, Insurance
from ..serializers import RiskTypeSerializer, InsuranceSerializer


class RiskTypeSerializerTest(TestCase):

    def test_create(self):
        data = get_risk_type_data()
        serializer = RiskTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        risk_type = serializer.create(serializer.validated_data)

        self.assertIsInstance(risk_type, RiskType)


class InsuranceSerializerTest(TestCase):

    def get_risk_type(self):
        risk_type_data = get_risk_type_data()
        risk_type_serializer = RiskTypeSerializer(data=risk_type_data)
        risk_type_serializer.is_valid()
        validated_data = risk_type_serializer.validated_data
        return risk_type_serializer.create(validated_data)

    def test_create(self):

        risk_type = self.get_risk_type()

        data = get_insurance_data(risk_type)
        serializer = InsuranceSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        insurance = serializer.create(serializer.validated_data)
        self.assertIsInstance(insurance, Insurance)

    def test_create_invalid_field_choice(self):

        risk_type = self.get_risk_type()

        invalid_choice = 'Bike'
        data = get_insurance_data(risk_type, invalid_choice)
        serializer = InsuranceSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        with self.assertRaisesMessage(serializers.ValidationError, 'Invalid choice option.'):
            serializer.create(serializer.validated_data)
