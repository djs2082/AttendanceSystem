from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Subject
from requirements import success, error 
from .serializers import SubjectSerializer



class SubjectView(APIView):

    def get(self, request, pk = None):
        try:
            if pk is None:
                queryset = Subject.objects.all()
                serialized = SubjectSerializer(queryset, many = True)
                if queryset.count() is 0:
                    raise TableEmptyError("No Subjects in Table to Display")
            else:
                queryset = Subject.objects.get(pk = pk)
                serialized = SubjectSerializer(queryset)
            response = success.APIResponse(200, serialized.data).respond()
            return Response(response,status=200)
        except Subject.DoesNotExist as not_found_error:
            error_message = "Subject with given Id is not found"
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)
        except TableEmptyError as empty_error:
            response = error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response,status=404)
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response,status=400)


    def post(self,request):
        try:
            data = request.data
            serialized = SubjectSerializer(data = data)  
            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message = "Subject {} added Successfully".format(saved)
            response = success.APIResponse(201,success_message).respond()
            return Response(response,201)
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response,409)
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response,409)   
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response,status=400)

    def put(self,request,pk):
        try:
            data = request.data
            instance = Subject.objects.get(pk = pk)
            serialized = SubjectSerializer(instance = instance,data = data,partial = True)
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            success_message="Subject {} updated successfully".format(saved)
            response=success.APIResponse(201,success_message).respond()
            return Response(response,status=201)
        except ValidationError as validation_error:
            error_message = "Subject {} already exists".format(data.get('subjectName'))
            response = error.APIErrorResponse(409,str(validation_error),error_message).respond()
            return Response(response,status=409) 
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response,status=409)    
        except Subject.DoesNotExist as not_found_error:
            error_message = "Subject with id {} is Not available".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response,status=400)    

    def delete(self,request,pk=None):
        try:
            if pk is None:
                Subject.objects.all().delete()
                success_message="All Subjects are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response,status=202)
            else:
                data = Subject.objects.get(pk = pk)
                data.delete()     
                success_message ="Subject with id {} is deleted".format(pk)
                response = success.APIResponse(202,success_message).respond()
                return Response(response,status=202)
        except Subject.DoesNotExist as not_found_error:
            error_message = "Subject with given id {} is Not available".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response,status=409)                                      
        except Exception as unknown_exception:
            response = error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)

class Error(Exception):
    pass
class TableEmptyError(Error):
    pass
