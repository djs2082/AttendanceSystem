from django.shortcuts import render
from .serializer import StudentAttendanceSerializer
from rest_framework.views import APIView
from requirements import success, error
from requirements.attendence import AttendencePrototype
from rest_framework.response import Response
from .models import StudentAttendance
from student.models import Student
from studentclass.models import StudentClass
from django.core.exceptions import EmptyResultSet
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from rest_framework.decorators import api_view
from professor.serializers import SubjectSerializer
from student.serializers import StudentSerializer
import json



class StudentAttendanceView(APIView):

    def post(self, request):
        try:
            serialized  =   StudentAttendanceSerializer(data=request.data)
            if serialized.is_valid(raise_exception=True):
                saved   =   serialized.save()
            msg         =   f"Attendence {saved} successfully"
            response    =   success.APIResponse(200, msg).respond()
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


    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    =   StudentAttendance.objects.all()
                serialized  =   StudentAttendanceSerializer(queryset, many=True)
            else:
                queryset    =   StudentAttendance.objects.get(pk=pk)
                serialized  =   StudentAttendanceSerializer(queryset)
                
            response    =   success.APIResponse(200, serialized.data).respond()
            return Response(response)

        except EmptyResultSet as empty_error:
            response    =   error.APIErrorResponse(404,str(empty_error)).respond()
            return Response(response)

        except StudentAttendance.DoesNotExist as not_found_error:
            msg         =   "Attendance of given id does not exists"
            response    =   error.APIErrorResponse(404, str(not_found_error), msg).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    def put(self, request, pk):
        try:
            att         =   StudentAttendance.objects.get(pk=pk)
            print(att)
            print(len(att.attendance))
            if len(att.attendance) is 0 or att.attendance == []:
                stat        =   {request.data['sid']: request.data['status']}
                proto       =   AttendencePrototype(request.data['date'], stat).get()
                print(proto)
                att.attendance.append(proto)
            else:
                for a in att.attendance:
                    print(a)
                    if a['date'].strip() == request.data['date'].strip():
                        print('date same')
                        proto   =   AttendencePrototype(a['date'], a['status'])
                        proto.update(request.data['sid'], request.data['status'])
                        print(proto.get())
                    else:
                        stat        =   {request.data['sid']: request.data['status']}
                        proto       =   AttendencePrototype(request.data['date'], stat).get()
                        att.attendance.append(proto)
            saved       =   att.save()
            msg         =   "Attendance updated successfully"
            response    =   success.APIResponse(200, msg).respond()
            return Response(response)
        
        except StudentAttendance.DoesNotExist as not_found_error:
            msg         =   "Attendance of given id does not exists"
            response    =   error.APIErrorResponse(404, str(not_found_error), msg).respond()
            return Response(response)

        except Exception as unkown_exception:
            response    =   error.APIErrorResponse(400,str(unkown_exception)).respond()
            return Response(response)

    
    def delete(self, request, pk=None):
        try:
            if pk is None:
                StudentAttendance.objects.all().delete()
                success_message =   "All Sections are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
                return Response(response)
            else:
                data            =   StudentAttendance.objects.get(pk = pk)
                data.delete()     
                success_message =   f"Attendance with id {pk} is deleted"
                response        =   success.APIResponse(202,success_message).respond()
                return Response(response)
        
        except StudentAttendance.DoesNotExist as not_found_error:
            error_message   =  f"Attendance with given id {pk} does not exist"
            response        =   error.APIErrorResponse(404,str(not_found_error),error_message).respond()
            return Response(response)
        
        except IntegrityError as integrity_error:
            error_message   =   "Integrity Error Occurred"
            response        =   error.APIErrorResponse(409,str(integrity_error),error_message).respond()
            return Response(response)                                      
        
        except Exception as unknown_exception:
            response        =   error.APIErrorResponse(400,str(unknown_exception)).respond()
            return Response(response)

