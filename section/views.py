from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Section
from requirements import success, error
from .serializer import SectionSerializer
from django.core.exceptions import EmptyResultSet

class SectionView(APIView):

    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   Section.objects.all()
                serialized  =   SectionSerializer(queryset, many=True)
                if queryset.count() is 0:
                    raise EmptyResultSet("No Sections")
            else:
                queryset    =   Section.objects.get(pk=pk)
                serialized  =   SectionSerializer(queryset)

            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)   

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except Section.DoesNotExist as not_found_error:
            msg         =   "Section of given id does not exists"
            response    =   error.APIErrorResponse(404, str(not_found_error), msg).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)


    
    def post(self,request):
        try:
            data        =   request.data
            serialized  =   SectionSerializer(data = data)

            if(serialized.is_valid(raise_exception = True)):
                saved = serialized.save()
            success_message =   f"Section {saved} added Successfully"
            response        =   success.APIResponse(201,success_message).respond()
            return Response(response)

        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
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
            instance    =   Section.objects.get(pk = pk)
            serialized  =   SectionSerializer(instance, data, partial = True)
            
            if serialized.is_valid(raise_exception = True):
                saved = serialized.save()
            
            success_message =   f"Section {saved} updated successfully"
            response=success.APIResponse(201,success_message).respond()
            return Response(response)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            return Response(response) 
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)    
        
        except Section.DoesNotExist as not_found_error:
            error_message   =  f"Section with id {pk} is Not available"
            response        =  error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response,status=404)   
        except Exception as unkown_exception:
            response        =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self,request,pk=None):
        try:
            if pk is None:
                Section.objects.all().delete()
                success_message =   "All Sections are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   Section.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Section with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except Section.DoesNotExist as not_found_error:
            error_message   =  f"Section with given id {pk} is Not available"
            response        =   error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response,status=400)
