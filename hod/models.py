from django.db import models
from department.models import Department
from professor.models import Professor
# Create your models here.
class HOD(models.Model):
    hodId           =   models.AutoField(primary_key=True)
    departmentId    =   models.ForeignKey(Department,on_delete=models.CASCADE,unique=True)
    hod             =   models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL) 

    def __str__(self):
        return str(self.hodId)
    class Meta:
        db_table='HOD_Table'