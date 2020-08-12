from django.db import models
from subject.models import Subject
from semester.models import Semester
from year.models import Year
from section.models import Section

# Create your models here.
class StudentClass(models.Model):
    classId = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    year    = models.ForeignKey(Year, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    class Meta:
        db_table = "Class_Table"

    # def __str__(self):
    #     return str(self.year) + str(self.section) + str(self.semester)