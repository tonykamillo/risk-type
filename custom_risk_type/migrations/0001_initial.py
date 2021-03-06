# Generated by Django 2.1.3 on 2018-12-04 19:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('field_type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('date', 'Date'), ('enum', 'Options')], max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldChoice',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='custom_risk_type.Field')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value', to='custom_risk_type.Field')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RiskType',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='insurance',
            name='risk_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='custom_risk_type.RiskType'),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='insurance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='values', to='custom_risk_type.Insurance'),
        ),
        migrations.AddField(
            model_name='field',
            name='risk_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='custom_risk_type.RiskType'),
        ),
    ]
