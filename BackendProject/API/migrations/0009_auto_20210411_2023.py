# Generated by Django 3.1.6 on 2021-04-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_auto_20210411_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='question',
            field=models.ManyToManyField(null=True, to='API.Question'),
        ),
    ]
