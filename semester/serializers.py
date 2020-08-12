from .models import Semester
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Semester
        fields  = ('__all__')
        extra_kwargs = {
            'semesterName' :{
                'validators' : [ UniqueValidator(queryset = model.objects.all()) ]
            }
        }