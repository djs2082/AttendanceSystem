from rest_framework import serializers
from .models import Student
from studentclass.models import StudentClass
from professor.models import Professor
from subject.models import Subject
from student_attendence.models import StudentAttendance
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('__all__')

        validators = [
            UniqueTogetherValidator(
                queryset=Student.objects.all(),
                fields=['registrationNo', 'email', 'mobile']
            )
        ]

        extra_kwargs = {
            'registrationNo' : {
                'validators' : [UniqueValidator(queryset = model.objects.all())]
            },

            'mobile' : {
                'validators' : [UniqueValidator(queryset = model.objects.all())]
            },

            'email' : {
                'validators' : [UniqueValidator(queryset = model.objects.all())]
            }
        }

class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ('subject',)

class SubjectProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('__all__')

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ('__all__')
