from django.db import models
from django.db import models

class Subject(models.Model):

    subjectId=models.AutoField(primary_key=True)
    subjectName=models.CharField(max_length=100,unique=True) 

    def __str__(self):
        return self.subjectName   

    class Meta:
        db_table='Subject_Table'