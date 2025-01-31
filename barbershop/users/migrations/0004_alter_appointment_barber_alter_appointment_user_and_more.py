# Generated by Django 5.0.6 on 2024-11-08 21:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_workinghour_day_of_week'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='barber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.barber'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workinghour',
            name='barber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.barber'),
        ),
        migrations.AlterField(
            model_name='workinghour',
            name='day_of_week',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.dayofweek'),
        ),
    ]
