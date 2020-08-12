from django.db import models
from student.models import Student
from django_mysql.models import ListCharField, JSONField

class StudentAttendance(models.Model):
    attendanceId    =   models.AutoField(primary_key=True)
    student         =   models.ForeignKey(Student,on_delete=models.CASCADE)
    attendance      =   JSONField(default=list)

    class Meta:
        db_table="StudentAttendance_Table"