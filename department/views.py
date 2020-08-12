from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Department
from requirements import success, error
from .serializer import DepartmentSerializer,DepartmentInsertSerializer
from django.core.exceptions import EmptyResultSet
from rest_framework.validators import ValidationError
import json

class DepartmentView(APIView):

    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   Department.objects.all()
                serialized  =   DepartmentSerializer(queryset, many=True)
                if queryset.count() is 0:
                    raise EmptyResultSet("No Departments")
            else:
                queryset    =   Department.objects.get(pk=pk)
                serialized  =   DepartmentSerializer(queryset)

            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except Department.DoesNotExist as not_found_error:
            msg         =   "Department of given id does not exists"
            response    =   error.APIErrorResponse(404, str(not_found_error), msg).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    def post(self,request):
        try:
            data        =   request.data
            serialized  =   DepartmentInsertSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Department {saved} added Successfully"
            response        =   success.APIResponse(201,success_message).respond()
            return Response(response)

        except ValidationError as validation_error:
            err =   json.loads( json.dumps(validation_error.__dict__) )
            response        =   error.APIErrorResponse(409, err['detail']).respond()
            return Response(response)

        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)

        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def put(self,request,pk):
        try:
            data        =   request.data
            instance    =   Department.objects.get(pk = pk)
            serialized  =   DepartmentInsertSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Department {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err =   json.loads( json.dumps(validation_error.__dict__) )
            try:
                e               =   err['detail']['hod']
                error_message   =   "This HOD already have department"
                response        =   error.APIErrorResponse(409, str(validation_error), error_message).respond()
                return Response(response)
            except:
                error_message   =   f"Department {data['departmentName']} already exists"
                response        =   error.APIErrorResponse(409, str(validation_error), error_message).respond()
                return Response(response)
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)    
        
        except Department.DoesNotExist as not_found_error:
            error_message   =  f"Department with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    def delete(self,request,pk=None):
        try:
            if pk is None:
                Department.objects.all().delete()
                success_message =   "All Departments are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                Department.objects.get(pk = pk).delete()
                success_message =   f"Department with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except Department.DoesNotExist as not_found_error:
            error_message   =  f"Department with given id {pk} is Not available"
            response        =   error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)

