# Generated by Django 4.1.1 on 2023-05-18 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0014_remove_exercise_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
