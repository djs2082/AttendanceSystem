# Generated by Django 3.0.6 on 2020-07-28 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studentclass', '0001_initial'),
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentId', models.AutoField(primary_key=True, serialize=False)),
                ('registrationNo', models.CharField(max_length=10, unique=True)),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=30)),
                ('class_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentclass.StudentClass')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.Department')),
            ],
            options={
                'db_table': 'Student_Table',
            },
        ),
    ]
