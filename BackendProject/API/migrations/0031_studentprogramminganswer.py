# Generated by Django 3.1.6 on 2021-07-10 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0030_violation_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProgrammingAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programming_language', models.CharField(choices=[('csharp', 'csharp'), ('python3', 'python3'), ('java', 'java'), ('php', 'php'), ('cpp14', 'cpp14'), ('go', 'go')], default='python3', max_length=100)),
                ('answer', models.TextField()),
                ('output', models.TextField(null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.programmingquestion')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.programmingtest')),
            ],
        ),
    ]
