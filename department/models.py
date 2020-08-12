from django.db import models
# from professor.models import Professor

class Department(models.Model):
    
    departmentId    =   models.AutoField(primary_key=True)
    departmentName  =   models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.departmentName
    
    class Meta:
        db_table="Department_Table"


