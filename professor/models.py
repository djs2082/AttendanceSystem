from django.db import models
from subject.models import Subject
from department.models import Department

class Professor(models.Model):
    professorId=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    mobile=models.CharField(max_length=10)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=30)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    subject=models.ManyToManyField(Subject,blank=True)
    def __str__(self):
        return self.email

    class Meta:
        db_table="Professor_Table"
