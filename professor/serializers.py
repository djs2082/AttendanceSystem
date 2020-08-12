from rest_framework import serializers
from professor.models import Professor
from subject.models import Subject
from subject.serializers import SubjectSerializer
from studentclass.models import StudentClass
from student.models import Student
from hod.models import HOD


class ProfessorSerializer(serializers.ModelSerializer):
    hod = serializers.SerializerMethodField('get_hod')
    def get_hod(self,professor):
        if HOD.objects.filter(hod=professor.professorId).exists():
            return HOD.objects.get(hod=professor.professorId).departmentId.departmentId
        else:
            return None
    class Meta:
        model   = Professor
        fields  = ('__all__')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StudentClass
        fields = ('classId','subject')
