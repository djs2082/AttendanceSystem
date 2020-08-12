from django.shortcuts import render
from .models import Student
from professor.models import Professor
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.serializers import ValidationError
from requirements import success, error
from django.db import IntegrityError
from rest_framework.response import Response
from .serializers import StudentSerializer, StudentSubjectSerializer, SubjectProfessorSerializer
from student_attendence.serializer import StudentAttendanceSerializer
from student_attendence.models import StudentAttendance

import datetime

class StudentView(APIView):
    def get(self, request, pk=None):
        try:
            if pk is None:
                queryset    = Student.objects.all()
                serializer  = StudentSerializer(queryset, many = True)
                if queryset.count() == 0:
                    raise TableEmptyError("No classess to display")
            else:
                queryset    = Student.objects.get(pk = pk)
                serializer  = StudentSerializer(queryset)
            response = success.APIResponse(200, serializer.data).respond()
            # return Response(response, status=200)

        except TableEmptyError as empty_error:
            response = error.APIErrorResponse(404, str(empty_error)).respond()
            # return Response(response, status=404)

        except Student.DoesNotExist as not_found_error:
            error_message = f"Student with given id {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            response = error.APIErrorResponse(400, str(e)).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

    def post(self, request):
        try:
            serializer = StudentSerializer(data = request.data)
            if serializer.is_valid(raise_exception = True):
                saved_object = serializer.save()
            success_message = f"Student {saved_object} added successfully"
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
            class_instance  = Student.objects.get(pk=pk)
            serializer          = StudentSerializer(instance=class_instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                saved_object = serializer.save()
            success_message = f"Student {saved_object} updated successfully"
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

        except Student.DoesNotExist as not_found_error:
            error_message = f"Student with given id {pk} does not exist"
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
            class_instance = Student.objects.get(pk=pk)
            class_instance.delete()
            success_message = f"Student with id {pk} deleted successfully"
            response = success.APIResponse(202, success_message).respond()
            # return Response(response, status=202)

        except IntegrityError:
            error_message = "Database integrity error occured"
            response      = error.APIErrorResponse(409, str(IntegrityError), error_message).respond()
            # return Response(response, status=409)

        except Student.DoesNotExist as not_found_error:
            error_message = f"Student with given {pk} does not exist"
            response = error.APIErrorResponse(404, str(not_found_error), error_message).respond()
            # return Response(response, status=404)

        except Exception as e:
            error_message   = "unexpected error occured"
            response        = error.APIErrorResponse(400, str(e), error_message).respond()
            # return Response(response, status=400)

        finally:
            return Response(response)

#getting student subjects with professors

class StudentSubjectView(APIView):
    def get(self, request, pk):
        queryset    = Student.objects.get(pk = pk).class_data
        serializer1 = StudentSubjectSerializer(queryset)
        data = {}
        for subject in serializer1.data['subject']:
            queryset    = Professor.objects.filter(subject__in=[subject])
            serializer2 = SubjectProfessorSerializer(queryset, many=True)
            professors  = []
            for i in range(len(serializer2.data)):
                professors.append(serializer2.data[i])
            data[subject] = professors
        response = success.APIResponse(200, data).respond()
        return Response(response)


class StudentAttendanceView(APIView):
    def get(self, request, pk):
        #getting student
        queryset_stud       = Student.objects.get(pk = pk)
        serializer_stud     = StudentSerializer(queryset_stud)

        #getting student subject
        serializer_sub      = StudentSubjectSerializer(queryset_stud.class_data)

        # getting student attendance
        queryset            = StudentAttendance.objects.get(student=serializer_stud.data['studentId'])
        serializer_attend   = StudentAttendanceSerializer(queryset)
        attendance_list     = serializer_attend.data['attendance']

        # get today's date
        date_today          = datetime.datetime.today().date()

        #initializing student attendance subjectwise to zero for counting
        subject_attendance  = {}
        for subject in serializer_sub.data['subject']:
            subject_attendance[subject] = 0
        
        data    =   {}
        day_count = 0

        #fetching attendance from student attendance model
        for attendance in attendance_list:
            date_stored = datetime.datetime.strptime(attendance['date'].replace("-",""),'%Y%m%d').date()

            if date_stored == date_today:
                data['today'] = attendance['status']

            elif date_stored < date_today:
                day_count += 1
                for subject in serializer_sub.data['subject']:
                    subject_attendance[subject] += attendance['status'][str(subject)]

        #calculating average attendance
        for subject in serializer_sub.data['subject']:
            subject_attendance[subject] = subject_attendance[subject]*100/day_count
        
        data['percentage'] = subject_attendance

        response = success.APIResponse(200, data).respond()
        return Response(response)


class TableEmptyError(Exception):
    pass
