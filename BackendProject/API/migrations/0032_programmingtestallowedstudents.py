# Generated by Django 3.1.6 on 2021-07-10 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0031_studentprogramminganswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammingTestAllowedStudents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('submit_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.programmingtest')),
            ],
        ),
    ]
