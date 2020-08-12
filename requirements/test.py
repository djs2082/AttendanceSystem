from django.test import TestCase
from requirements import authentication
from rest_framework.test import APITestCase
from professor.models import Professor
from student.models import Student
import json
class TestAuth(APITestCase):
    def test_create_token(self):
        auth=authentication.Authentication()
        response=auth.create_token('student',1,'djs@gmail.com')
        self.assertEqual(response['Status'],200)
    def test_token_decode(self):
        response=self.client.get("/req/auth/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoic3R1ZGVudCIsInVzZXJfaWQiOjEsImVtYWlsIjoiZGpzQGdtYWlsLmNvbSJ9.9k1GnZiONr0j-isBD1f0yY3L3njt7QkiCyE9caMst9o")
        self.assertEqual(json.loads(response.content)['Status'],202)

    def test_invalid_token_decode(self):
        response=self.client.get("/req/auth/0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoic3R1ZGVudCIsInVzZXJfaWQiOjEsImVtYWlsIjoiZGpzQGdtYWlsLmNvbSJ9.9k1GnZiONr0j-isBD1f0yY3L3njt7QkiCyE9caMst9o")
        self.assertEqual(json.loads(response.content)['Status'],400)

    def test_authenticate_student(self):
        auth=authentication.Authentication()
        student=Student(registrationNo='2017bcs042',fname='d',lname='j',email='djs@gmail.com',mobile='1234567890',city='nanded',state='maha')
        student.save()
        studentId=Student.objects.get(email='djs@gmail.com').studentId
        response=auth.create_token('student',studentId,'djs@gmail.com')
        token_decode=self.client.get('/req/auth/'+response['Token'])
        self.assertEqual(json.loads(token_decode.content)['Status'],202)

    def test_authenticate_professor(self):
        auth=authentication.Authentication()
        professor=Professor(fname='rkc',lname='rkc',email='rkc@gmail.com',mobile='1234566789',city='nanded',state=
        'maha')
        professor.save()
        professorId=Professor.objects.get(email='rkc@gmail.com').professorId
        response=auth.create_token('professor',professorId,'rkc@gmail.com')
        token_decode=self.client.get('/req/auth/'+response['Token'])
        self.assertEqual(json.loads(token_decode.content)['Status'],202)


    def test_authenticate_fail(self):
        auth=authentication.Authentication()
        student=Student(registrationNo='2017bcs042',fname='d',lname='j',email='djs@gmail.com',mobile='1234567890',city='nanded',state='maha')
        student.save()
        studentId=Student.objects.get(email='djs@gmail.com').studentId
        response=auth.create_token('student',studentId,'djsfake@gmail.com')
        token_decode=self.client.get('/req/auth/ee'+response['Token'])
        self.assertEqual(json.loads(token_decode.content)['Status'],400)


