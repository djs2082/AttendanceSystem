from rest_framework import serializers
from year.models import Year
from rest_framework.validators import UniqueValidator

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model=Year
        fields=('__all__')
        extra_kwargs={
            'yearName': {
                'validators': [UniqueValidator(queryset = model.objects.all())],
            }
        }

