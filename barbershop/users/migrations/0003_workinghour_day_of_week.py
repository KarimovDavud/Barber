# Generated by Django 5.0.6 on 2024-11-06 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_workinghour_barber'),
    ]

    operations = [
        migrations.AddField(
            model_name='workinghour',
            name='day_of_week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.dayofweek'),
            preserve_default=False,
        ),
    ]
