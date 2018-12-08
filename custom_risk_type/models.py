import uuid
from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RiskType(BaseModel):
    pass


class Field(BaseModel):

    FIELD_TYPE_CHOICES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('enum', 'Options'),
    )

    # basemodel_ptr = models.OneToOneField(BaseModel, on_delete=models.CASCADE, parent_link=True, related_name='field_child')

    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE_CHOICES)
    risk_type = models.ForeignKey(RiskType, related_name='fields', on_delete=models.CASCADE)


class FieldChoice(UUIDModel):
    value = models.CharField(max_length=100)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='choices')


class Insurance(UUIDModel):
    risk_type = models.ForeignKey(RiskType, related_name='policies', on_delete=models.CASCADE)


class FieldValue(BaseModel):
    insurance = models.ForeignKey(Insurance, related_name='values', null=True, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, related_name='value', on_delete=models.CASCADE)
