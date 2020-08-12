from django.shortcuts import render
from rest_framework.views import APIView
from year.models import Year
from year.serializers import YearSerializer
from requirements import success,error
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import IntegrityError


# Create your views here.
class yearView(APIView):

    def get(self, request, pk = None):
        try:
            if pk is None:
                queryset = Year.objects.all()
                serialized = YearSerializer(queryset, many = True)
                if queryset.count() is 0:
                    raise TableEmptyError("No Years in Table to Display")
            else:
                queryset = Year.objects.get(pk = pk)
                serialized = YearSerializer(queryset)
            response = success.APIResponse(200, serialized.data).respond()
            return Response(response)
        except Year.DoesNotExist as not_found_error:
            error_message = "Yearect with given Id is not found"
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response)
        except TableEmptyError as empty_error:
            response = error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response,)
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    def post(self,request):
        try:
            data = request.data
            serialized = YearSerializer(data = data)  
            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message = "Year {} added Successfully".format(saved)
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
            instance = Year.objects.get(pk = pk)
            serialized = YearSerializer(instance = instance,data = data,partial = True)
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            success_message="Year {} updated successfully".format(saved)
            response=success.APIResponse(201,success_message).respond()
            return Response(response,status=201)
        except ValidationError as validation_error:
            error_message = "Year {} already exists".format(data.get('yearName'))
            response = error.APIErrorResponse(409,str(validation_error),error_message).respond()
            return Response(response,status=409) 
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response,status=409)    
        except Year.DoesNotExist as not_found_error:
            error_message = "Year with id {} is Not available".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response,status=400)    

    def delete(self,request,pk=None):
        try:
            if pk is None:
                Year.objects.all().delete()
                success_message="All Years are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response,status=202)
            else:
                data = Year.objects.get(pk = pk)
                data.delete()     
                success_message ="Year with id {} is deleted".format(pk)
                response = success.APIResponse(202,success_message).respond()
                return Response(response,status=202)
        except Year.DoesNotExist as not_found_error:
            error_message = "Year with given id {} is Not available".format(pk)
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