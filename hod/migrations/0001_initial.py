# Generated by Django 3.0.5 on 2020-07-28 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('professor', '0001_initial'),
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('hodId', models.AutoField(primary_key=True, serialize=False)),
                ('departmentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.Department')),
                ('hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='professor.Professor')),
            ],
            options={
                'db_table': 'HOD_Table',
            },
        ),
    ]