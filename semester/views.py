from .models import Semester
from rest_framework.response import Response
from .serializers import SemesterSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError
from requirements import success, error
from django.db import IntegrityError
from django.core.exceptions import EmptyResultSet

class SemesterView(APIView):
    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    = Semester.objects.all()
                serializer  = SemesterSerializer(queryset, many = True)
                if queryset.count() == 0:
                    raise EmptyResultSet("No semesters to display")
            else:
                queryset    = Semester.objects.get(pk = pk)
                serializer  = SemesterSerializer(queryset)
            response = success.APIResponse(200, serializer.data).respond()
            # return Response(response, status=200)

        except EmptyResultSet as empty_error:
            response = error.APIErrorResponse(404, str(empty_error)).respond()
            # return Response(response, status=404)

        except Semester.DoesNotExist as not_found_error:
            error_message = f"Semester with given id {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            response = error.APIErrorResponse(400, str(e)).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

    def post(self, request):
        try:
            serializer = SemesterSerializer(data = request.data)
            if serializer.is_valid(raise_exception = True):
                saved_object = serializer.save()
            success_message = f"Semester {saved_object} added successfully"
            response = success.APIResponse(200, success_message).respond()
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
            semester_instatnce  = Semester.objects.get(pk=pk)
            serializer          = SemesterSerializer(instance=semester_instatnce, data=request.data)
            if serializer.is_valid(raise_exception=True):
                saved_object = serializer.save()
            success_message = f"Semester {saved_object} updated successfully"
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

        except Semester.DoesNotExist as not_found_error:
            error_message = f"Semester with given id {pk} does not exist"
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
            semester_instatnce = Semester.objects.get(pk=pk)
            semester_instatnce.delete()
            success_message = f"Semester with id {pk} deleted successfully"
            response = success.APIResponse(202, success_message).respond()
            # return Response(response, status=202)

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, str(IntegrityError), error_message).respond()
            # return Response(response, status=409)

        except Semester.DoesNotExist as not_found_error:
            error_message = f"Semester with given {pk} does not exist"
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
        # finally:
        #     return Response(response)
