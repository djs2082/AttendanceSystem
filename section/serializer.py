from rest_framework import serializers
from .models import Section
from rest_framework.validators import UniqueValidator

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model   =   Section
        fields  =   ('__all__')
        extra_kwargs={
            'sectionName': {
                'validators': [UniqueValidator(queryset = model.objects.all())],
            }
        }