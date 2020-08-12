from rest_framework import serializers
from hod.models import HOD

class HodSerializer(serializers.ModelSerializer):
    class Meta:
        model=HOD
        fields=('__all__')
