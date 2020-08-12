from rest_framework import serializers
from .models import StudentAttendance
from rest_framework.validators import UniqueValidator

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model   =   StudentAttendance
        fields  =   ('attendanceId', 'student', 'attendance')

        extra_kwargs={
            'student': {
                'validators': [UniqueValidator(queryset = model.objects.all())],
            }
        }
