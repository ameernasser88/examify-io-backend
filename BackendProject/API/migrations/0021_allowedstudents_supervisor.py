# Generated by Django 3.1.6 on 2021-05-16 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0020_auto_20210515_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowedstudents',
            name='supervisor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='API.supervisor'),
        ),
    ]