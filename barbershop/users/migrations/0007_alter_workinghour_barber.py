# Generated by Django 5.0.6 on 2024-11-08 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_working_hours_barber_workinghours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinghour',
            name='barber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to='users.barber'),
            preserve_default=False,
        ),
    ]
