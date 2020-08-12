from django.db import models

# Create your models here.
class Year(models.Model):
    yearId=models.AutoField(primary_key=True)
    yearName=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.yearName
    class Meta:
        db_table='Year_Table'