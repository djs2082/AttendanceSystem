from django.db import models


class Section(models.Model):
    
    sectionId=models.AutoField(primary_key=True)
    sectionName=models.CharField(max_length=1)

    def __str__(self):
        return self.sectionName
    
    class Meta:
        db_table="Section_Table"
