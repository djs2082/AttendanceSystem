from rest_framework import serializers
from subject.models import Subject
from rest_framework.validators import UniqueValidator

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=('__all__')
        extra_kwargs={
            'subjectName': {
                'validators': [UniqueValidator(queryset = model.objects.all())],
            }
        }

