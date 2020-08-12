from .models import StudentClass
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ValidationError


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model   = StudentClass
        fields  = ('__all__')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=StudentClass.objects.all(),
        #         fields=['section', 'year', 'subject', 'semester']
        #     )
        # ]
    
    # def validate(self, data):
    #     # print(data)
    #     c = StudentClass.objects.filter(section=data['section'], year=data['year'], semester=data['semester']).count()
    #     # print(c)
    #     if c != 0:
    #         raise ValidationError('class exists')
    #     return data