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

'''
{
  "name": "Car",
  "fields": [
    {"label": "Starts at", "name": "starts_at", "field_type": "date"},
    {"label": "Expires at","name": "expires_at", "field_type": "date"},
    {"label": "Field type","name": "model", "field_type": "text"}
  ]
}

{
    "risk_type": "98e1d08c-d2aa-4317-90f0-4f1d55eb7517",
    "values": [
        {"name": "2018-11-28", "field": "3625c315-6aa5-4cfc-a0f2-a2361750e679"},
        {"name": "2019-11-28", "field": "9c173a05-b95d-4c73-b6e6-bb91ecd079a0"},
        {"name": "Dodge Charger", "field": "53e5676f-4e94-402e-8eb0-176924177d14"}
    ]
}

{
    "risk_type":"98e1d08c-d2aa-4317-90f0-4f1d55eb7517",
    "values":[
        {"name":"2018-12-02","field":"8065a984-6767-479a-92f0-4b68ab61b9e9"},
        {"name":"2018-12-02","field":"2bff43a4-139f-41ba-8784-5173f6d02c70"},
        {"name":"ads","field":"d617cc36-96a4-4953-8e30-3442f9d3d4ce"}
    ]
}

{
  "name": "Fleet",
  "fields": [
    {"name": "starts_at", "label": "Starts at", "field_type": "date"},
    {"name": "expires_at", "label": "Expires at", "field_type": "date"},
    {"name": "coverage", "label": "Coverage", "field_type": "number"},
    {"name": "clause", "label": "Clause", "field_type": "text"},
    {"name": "price", "label": "Price", "field_type": "number"},
    {
      "name": "fleet_type",
      "label": "Fleet type",
      "field_type": "enum",
      "choices": [
        {"value": "Car"},
        {"value": "Truck"},
        {"value": "Ship"}
      ]
    }
  ]
}

# Feet Risk Type Policy
{
    "risk_type": "b37494b9-0558-467c-a86b-920db8f1e1eb",
    "values": [
        {"name": "2018-11-28", "field": "bce3bf2d-5bb4-4d5d-8806-87ad36a2540b"},
        {"name": "2019-11-28", "field": "b1e1dcad-5d41-4dc7-b52a-0ad3c6ab537b"},
        {"name": 1000000.00, "field": "b3ee56bf-5126-47f2-a01d-77aba28f71cc"},
        {"name": "Pay the coverage", "field": "9c41b3f6-cca8-4fa6-a98f-d706591f891f"},
        {"name": 1100000.00, "field": "edb67ec7-0cc1-4133-9d63-20358bb556d8"},
        {"name": "Truck", "field": "9c46e321-58d6-4564-951b-9d9a446855f0"}
    ]
}
  '''
