# Generated by Django 5.0 on 2023-12-30 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', models.BinaryField(null=True)),
                ('task', models.CharField(max_length=80, null=True)),
                ('updated_time', models.CharField(max_length=80, null=True)),
            ],
        ),
    ]