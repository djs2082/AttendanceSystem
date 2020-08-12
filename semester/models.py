from django.db import models

class Semester( models.Model ):
    semesterId   = models.AutoField( primary_key=True )
    semesterName = models.CharField( max_length=30 )
    
    def __str__(self):
        return self.semesterName

    class Meta:
        db_table = "Semester_Table"
