# Generated by Django 3.1.6 on 2021-04-15 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0012_auto_20210414_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='previous_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='API.question'),
        ),
    ]