# Generated by Django 3.1.6 on 2021-05-18 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0023_auto_20210518_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowedstudents',
            name='attendance',
            field=models.BooleanField(default=False),
        ),
    ]