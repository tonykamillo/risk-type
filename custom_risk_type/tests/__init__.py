
'''
Some shortcuts to use in tests
'''


def get_risk_type_data():
    '''
    Get a sample parameter for creating a risk type
    '''
    return {
        'name': 'Fleet',
        'fields': [
            {'name': 'starts_at', 'label': 'Starts at', 'field_type': 'date'},
            {'name': 'expires_at', 'label': 'Expires at', 'field_type': 'date'},
            {'name': 'coverage', 'label': 'Coverage', 'field_type': 'number'},
            {'name': 'clause', 'label': 'Clause', 'field_type': 'text'},
            {'name': 'price', 'label': 'Price', 'field_type': 'number'},
            {
                'name': 'fleet_type',
                'label': 'Fleet type',
                'field_type': 'enum',
                'choices': [
                    {'value': 'Car'},
                    {'value': 'Truck'},
                    {'value': 'Ship'}
                ]
            }
        ]
    }


def get_values(field_choice='Truck'):
    '''
    Get a sample values for tests

    Paramenters
    -----------
    field_choice: str (optinal)
        Setting a field choices option.
    '''
    return [
        '2018-11-28',
        '2019-11-28',
        1000000.00,
        'Pay the coverage',
        1100000.00,
        field_choice
    ]


def get_insurance_data(risk_type, field_choice='Truck'):
    '''
    Get a sample parameters for creating a insurance based on risk type

    Parameters
    ----------
    risk_type: dict/RiskType
        A risk type object or representation
    field_choice: str (optional)
        Especifies a field choices option. It allows testing invalid choice option.
    '''

    fields = []
    if not isinstance(risk_type, dict):
        fields = list(risk_type.fields.values_list('uuid', flat=True))
        risk_type = vars(risk_type)

    else:
        fields = [field['uuid'] for field in risk_type['fields']]

    values = get_values(field_choice)

    return {
        'risk_type': risk_type['uuid'],
        'values': [
            {'name': values[i], 'field': fields[i]} for i in range(len(fields))
        ]
    }
