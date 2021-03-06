# Generated by Django 2.1.1 on 2018-09-30 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BadPassports',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('passport_series', models.CharField(max_length=4)),
                ('passport_number', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='IdentifiablePerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('passport_series', models.CharField(max_length=4)),
                ('passport_number', models.CharField(max_length=6)),
                ('first_name', models.CharField(max_length=65)),
                ('middle_name', models.CharField(max_length=65)),
                ('last_name', models.CharField(max_length=65)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='IdentificationAttempt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('response', models.BooleanField()),
                ('attempt_date', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.IdentifiablePerson')),
            ],
        ),
        migrations.CreateModel(
            name='SimpleWords',
            fields=[
                ('value', models.CharField(max_length=65, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
