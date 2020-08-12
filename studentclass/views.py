from django.shortcuts import render
from .models import StudentClass
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError
from requirements import success, error
from django.db import IntegrityError
from rest_framework.response import Response
from .serializers import StudentClassSerializer

# Create your views here.
class StudentClassView(APIView):
    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    = StudentClass.objects.all()
                serializer  = StudentClassSerializer(queryset, many = True)
                if queryset.count() == 0:
                    raise TableEmptyError("No classess to display")
            else:
                queryset    = StudentClass.objects.get(pk = pk)
                serializer  = StudentClassSerializer(queryset)
            response = success.APIResponse(200, serializer.data).respond()
            # return Response(response, status=200)

        except TableEmptyError as empty_error:
            response = error.APIErrorResponse(404, str(empty_error)).respond()
            # return Response(response, status=404)

        except StudentClass.DoesNotExist as not_found_error:
            error_message = f"StudentClass with given id {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            response = error.APIErrorResponse(400, str(e)).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

    def post(self, request):
        try:
            serializer = StudentClassSerializer(data = request.data)
            if serializer.is_valid(raise_exception = True):
                saved_object = serializer.save()
            success_message = f"StudentClass {saved_object} added successfully"
            response = success.APIResponse(201, success_message).respond()
            # return Response(response, status=201)
        
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            # return Response(response, status=409)

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, str(IntegrityError), error_message).respond()
            # return Response(response, status=409)

        except Exception as e:
            error_message   = "unexpected error occured"
            response        = error.APIErrorResponse(400, str(e), error_message).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

    def put(self, request, pk):
        try:
            class_instance  = StudentClass.objects.get(pk=pk)
            serializer          = StudentClassSerializer(instance=class_instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                saved_object = serializer.save()
            success_message = f"StudentClass {saved_object} updated successfully"
            response = success.APIResponse(201, success_message).respond()
            # return Response(response, status=201)

        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
            # return Response(response, status=409)

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, str(IntegrityError), error_message).respond()
            # return Response(response, status=409)

        except StudentClass.DoesNotExist as not_found_error:
            error_message = f"StudentClass with given id {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            error_message   = "unexpected error occured"
            response        = error.APIErrorResponse(400, str(e), error_message).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

    def delete(self, request, pk):
        try:
            class_instance = StudentClass.objects.get(pk=pk)
            class_instance.delete()
            success_message = f"StudentClass with id {pk} deleted successfully"
            response = success.APIResponse(202, success_message).respond()
            # return Response(response, status=202)

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, str(IntegrityError), error_message).respond()
            # return Response(response, status=409)

        except StudentClass.DoesNotExist as not_found_error:
            error_message = f"StudentClass with given {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            error_message   = "unexpected error occured"
            response        = error.APIErrorResponse(400, str(e), error_message).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

class TableEmptyError(Exception):
    pass