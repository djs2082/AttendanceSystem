from django.db import models
from studentclass.models import StudentClass
from department.models import Department


class Student(models.Model):
    studentId       = models.AutoField(primary_key=True)
    registrationNo = models.CharField(max_length=10,unique=True)
    fname   = models.CharField(max_length=30)
    lname   = models.CharField(max_length=30)
    email   = models.EmailField(max_length=50)
    mobile  = models.CharField(max_length=10)
    city    = models.CharField(max_length=20)
    state   = models.CharField(max_length=30)
    department  = models.ForeignKey(Department,null=True,on_delete=models.SET_NULL)       
    class_data  = models.ForeignKey(StudentClass,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.registrationNo

    class Meta:
        db_table="Student_Table"