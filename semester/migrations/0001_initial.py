# Generated by Django 3.0.5 on 2020-07-28 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('semesterId', models.AutoField(primary_key=True, serialize=False)),
                ('semesterName', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Semester_Table',
            },
        ),
    ]
