from django.db import transaction
from rest_framework import serializers
from .models import RiskType, Field, FieldChoice, FieldValue, Insurance


class FieldChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldChoice
        fields = ('uuid', 'value', 'field')
        extra_kwargs = {'field': {'required': False}}


class FieldSerializer(serializers.ModelSerializer):

    choices = FieldChoiceSerializer(many=True, required=False)

    class Meta:
        model = Field
        fields = ('uuid', 'label', 'name', 'field_type', 'choices')


class FieldValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldValue
        fields = ('uuid', 'name', 'field')
        extra_kwargs = {'field': {'required': False}}


class RiskTypeSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = RiskType
        fields = ('uuid', 'name', 'fields')

    def create(self, validated_data):
        '''
        Creates a custom risk type
        '''
        # Extracting custom fields data from validated_data, avoiding parameter error in RiskType creation
        fields_data = []
        if 'fields' in validated_data:
            fields_data = validated_data.pop('fields')

        risk_type = {}
        with transaction.atomic():
            risk_type, created = RiskType.objects.get_or_create(name=validated_data['name'], defaults=validated_data)

            for field_data in fields_data:

                # Extracting custom choices data from field_data in case of enum type and also avoiding parameter error in Field creation
                choices_data = []
                if 'choices' in field_data:
                    choices_data = field_data.pop('choices')

                field, created = Field.objects.get_or_create(risk_type=risk_type, name=field_data['name'], defaults=field_data)

                # Creating options for enum type
                for choice_data in choices_data:
                    FieldChoice.objects.create(field=field, **choice_data)

        return risk_type


class InsuranceSerializer(serializers.ModelSerializer):
    values = FieldValueSerializer(many=True)

    class Meta:
        model = Insurance
        fields = ('uuid', 'risk_type', 'values')

    def create(self, validated_data):
        '''
        Creates a policy for a custom risk type
        '''

        # Stripping data values to avoiding creation error on Insurance
        values_data = validated_data.pop('values')

        insurance = {}

        with transaction.atomic():
            insurance = Insurance.objects.create(**validated_data)

            # Saving values and associating them to a custom field
            for value_data in values_data:
                field = value_data['field']

                # Checking if value is a valid option, otherwise raise an Exception
                if field.field_type == 'enum' \
                        and not field.choices.filter(value=value_data['name']).exists():
                    raise serializers.ValidationError('Invalid choice option.')

                FieldValue.objects.create(insurance=insurance, **value_data)

        return insurance
