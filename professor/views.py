from django.shortcuts import render
from rest_framework.views import APIView
from professor.models import Professor
from professor.serializers import ProfessorSerializer,SubjectSerializer
from requirements import success,error
from rest_framework.response import Response
from django.core.exceptions import EmptyResultSet
from rest_framework.serializers import ValidationError
from django.db import IntegrityError
from studentclass.models import StudentClass
from student.models import Student
from student.serializers import StudentSerializer
from studentclass.models import StudentClass
from rest_framework.decorators import api_view
from student_attendence.models import StudentAttendance
import json



class ProfessorView(APIView):
    def get(self,request,pk=None):
        try:
            if pk is None:
                queryset=Professor.objects.all()
                serialized=ProfessorSerializer(queryset,many=True)
                response = success.APIResponse(200, serialized.data).respond()
            else:
                queryset=Professor.objects.get(pk=pk)
                serialized=ProfessorSerializer(queryset)
                response = success.APIResponse(200, serialized.data).respond()
        except EmptyResultSet as empty_result:
            response = error.APIErrorResponse(404,str(empty_result)).respond()
        except Professor.DoesNotExist as not_found_error:
            error_message = "Professor with id {} is not found".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
        except EmptyResultSet as empty_error:
            response = error.APIErrorResponse(404,str(empty_error)).respond()
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
        finally:
            return Response(response)
    
    def post(self,request):
        try:
            data=request.data
            serialized=ProfessorSerializer(data=data)
            if(serialized.is_valid(raise_exception=True)):
                saved=serialized.save()
            response = success.APIResponse(201, "added {}".format(saved)).respond()
        except ValidationError as validation_error:
            err = validation_error.__dict__
            response        = error.APIErrorResponse(409, err['detail']).respond()
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()   
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
        finally:
            return Response(response)

    def put(self,request,pk):
        try:
            data=request.data
            instance=Professor.objects.get(pk=pk)
            serialized=ProfessorSerializer(data=data,instance=instance,partial=True)
            if(serialized.is_valid(raise_exception=True)):
                saved=serialized.save()
            response = success.APIResponse(201, "updated {}".format(saved)).respond()
        except ValidationError as validation_error:
            response = error.APIErrorResponse(409,str(validation_error)).respond()
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()   
        except Professor.DoesNotExist as not_found_error:
            error_message = "Professor with id {} is Not available".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()  
        except Exception as unkown_exception:
            response = error.APIErrorResponse(400,str(unkown_exception)).respond()
        finally:
            return Response(response,status=400) 

    def delete(self,request,pk=None):
        try:
            if pk is None:
                Professor.objects.all().delete()
                success_message="All Professors are deleted Successfully"
                response=success.APIResponse(202,success_message).respond()
            else:
                data = Professor.objects.get(pk = pk)
                data.delete()     
                success_message ="Professor with id {} is deleted".format(pk)
                response = success.APIResponse(202,success_message).respond()
        except Professor.DoesNotExist as not_found_error:
            error_message = "Professor with given id {} is Not available".format(pk)
            response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
        except IntegrityError as integrity_error:
            error_message = "Integrity Error Occurred"
            response = error.APIErrorResponse(409,str(integrity_error),error_message).respond()                                      
        except Exception as unknown_exception:
            response = error.APIErrorResponse(400,str(unknown_exception)).respond()
        finally:
            return Response(response)
        


@api_view(['GET',])
def get_students_sub(request,sub_id):
    try:
        queryset=StudentClass.objects.all()
        stud={}
        serialized=SubjectSerializer(queryset,many=True)
        for studentclass in serialized.data:
            data=dict(studentclass.items())
            print(data)
            for subject in data['subject']:
                if subject is sub_id:
                    queryset=Student.objects.filter(class_data=data['classId'])
                    serialized=StudentSerializer(queryset,many=True)
                    stud[data['classId']]=serialized.data
        response = success.APIResponse(200, stud).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response = error.APIErrorResponse(400, err).respond()
    finally:
        return(Response(response))


@api_view(['GET',])
def get_students_class(request,class_id):
    try:
        queryset=Student.objects.filter(class_data=class_id)
        serialized=StudentSerializer(queryset,many=True)
        response = success.APIResponse(200, serialized.data).respond()
    except Student.DoesNotExist as not_found_error:
        error_message = "Student with given class {} is Not available".format(class_id)
        response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response = error.APIErrorResponse(400, err).respond()
    finally:
        return(Response(response))



@api_view(['GET',])
def get_students_professor(request,prof_id):
    try:
        queryset    =   Professor.objects.get(professorId=prof_id)
        stud    =   []
        serialized  =   SubjectSerializer(queryset)
        subjects    =   dict(serialized.data)['subject']
        queryset    =   StudentClass.objects.all()
        serialized  =   SubjectSerializer(queryset,many=True)
        for studentclass in serialized.data:
            class_student   =   {}
            class_subjects  =   dict(studentclass)['subject']
            class_student['class']    =   dict(studentclass)['classId']
            subs=[]
            for prof_subject in subjects:
                subject_student   =   {}
                if prof_subject in class_subjects:
                    subject_student['subject']    =   prof_subject
                    queryset=Student.objects.filter(class_data  =   class_student['class'])
                    serialized_student  =   StudentSerializer(queryset,many=True)
                    subject_student['data'] =    serialized_student.data

                    subs.append(subject_student)
            class_student['data']   =  subs
            if 'data' in class_student:
                stud.append(class_student)
        response    =   success.APIResponse(200, stud).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except Professor.DoesNotExist as not_found_error:
        error_message = "Professor with given id {} is Not available".format(prof_id)
        response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response    =   success.APIResponse(400, err).respond()
    finally:
        return(Response(response))

@api_view(['GET',])
def get_date_attenence(request,sub_id,class_id):
    try:
        date=request.data.get('date')
        studs={}
        students=Student.objects.filter(class_data=class_id)
        for student in students:
            attendence=StudentAttendance.objects.get(student=student.studentId)
            for attend in attendence.attendance:
                print(attend)
                if date == attend['date']:
                    if str(sub_id) in attend['status']:
                        print(attend['status'][str(sub_id)])
                        studs[student.fname]=attend['status'][str(sub_id)]
        response    =   success.APIResponse(200, studs).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except StudentAttendance.DoesNotExist as not_found_error:
        error_message = "Attendence of given id  is Not available"
        response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response    =   success.APIResponse(400, err).respond()
    finally:
        return(Response(response))

@api_view(['GET',])
def get_week_attenence(request,sub_id,class_id):
    try:
        studs=[]
        students=Student.objects.filter(class_data=class_id)
        for student in students:
            data={}
            attendence=StudentAttendance.objects.get(student=student.studentId)
            data['student']=student.fname
            subs_data={}
            for attend in attendence.attendance:
                subs_data['date']=attend['date']
                sub_list=attend['status']
                if str(sub_id) in sub_list:
                    subs_data['data']={str(sub_id):sub_list[str(sub_id)]}
                data['data']=subs_data
            studs.append(data)
        response    =   success.APIResponse(200, studs).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except StudentAttendance.DoesNotExist as not_found_error:
        error_message = "Attendence of given id is Not available"
        response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response    =   success.APIResponse(400, err).respond()
    finally:
        return(Response(response))



@api_view(['GET',])
def get_class(request,prof_id):
    try:
        subjects=[]
        classes=[]
        queryset=Professor.objects.get(pk=prof_id)
        serialized=SubjectSerializer(queryset)
        for subject in serialized.data['subject']:
            subjects.append(subject)
        studenclass=StudentClass.objects.all()
        serialized=SubjectSerializer(studenclass,many=True)
        for subject in serialized.data:
            data=dict(subject.items())
            class_temp={}
            subs=[]
            class_temp['classId']=data['classId']
            for prof_subject in subjects:
                if prof_subject in data['subject']:
                    subs.append(prof_subject)
            if len(subs) > 0:
                class_temp['subjects']=subs
                classes.append(class_temp)
        response = success.APIResponse(200, classes).respond()
    except EmptyResultSet as empty_error:
        response = error.APIErrorResponse(404,str(empty_error)).respond()
    except Professor.DoesNotExist as not_found_error:
        error_message = "Professor of id {} is Not available".format(prof_id)
        response = error.APIErrorResponse(404,str(not_found_error),error_message).respond()
    except ValidationError as validation_error:
        err = validation_error.__dict__
        response        = error.APIErrorResponse(409, err['detail']).respond()
    except Exception as err:
        response    =   success.APIResponse(400, err).respond()
    finally:
        return(Response(response))




