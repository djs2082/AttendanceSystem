
from rest_framework import serializers
from .models import Department
from hod.models import HOD
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class DepartmentSerializer(serializers.ModelSerializer):
    hod = serializers.SerializerMethodField('get_hod')
    def get_hod(self,department):
        if HOD.objects.filter(departmentId=department.departmentId).exists():
            return HOD.objects.get(departmentId=department.departmentId).hod.professorId
        else:
            return 'null'
    class Meta:
        model       =   Department
        validators  = [
            UniqueTogetherValidator(
                queryset    =   model.objects.all(),
                fields      =   ('departmentName', 'hod')
            )
        ]
    
        fields  =   ('__all__')
        extra_kwargs={
            'departmentName': {
                'validators': [UniqueValidator(queryset = model.objects.all())],
            }
        }
class DepartmentInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model       =   Department
        fields  =   ('__all__')

