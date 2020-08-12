from django.test import TestCase
from rest_framework.test import APITestCase
from department.models import Department
from professor.models import Professor
from rest_framework import status
import json
class DepartmentTest(TestCase):
    def setup(self):
        departmentName='CSE'
        professerName='RKC'
        department=Department(departmentName=departmentName)
        department.save()
        department=Department.objects.get(departmentName=departmentName)
        self.department=department
        self.departmentId=department.departmentId
        professor=Professor(fname=professerName,lname=professerName,email='rkc@gmail.com',mobile='123456789',city='nanded',state='maha',department=self.department)
        professor.save()
        professor=Professor.objects.get(fname=professerName)
        self.professor=professor
        self.professorId=professor.professorId

    def test_insert(self):
        Professor.objects.all().delete()
        old_count=Professor.objects.all().count()
        self.setup()
        new_count=Professor.objects.all().count()
        self.assertNotEqual(old_count,new_count)

class TestGet(APITestCase):
    def setup(self):
        departmentName='CSE'
        professerName='RKC'
        department=Department(departmentName=departmentName)
        department.save()
        department=Department.objects.get(departmentName=departmentName)
        self.department=department
        self.departmentId=department.departmentId
        professor=Professor(fname=professerName,lname=professerName,email='rkc@gmail.com',mobile='123456789',city='nanded',state='maha',department=self.department)
        professor.save()
        professor=Professor.objects.get(fname=professerName)
        self.professor=professor
        self.professorId=professor.professorId


    def test_get(self):
        Professor.objects.all().delete()
        self.setup()
        response=self.client.get('/professor/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id(self):
        Professor.objects.all().delete()
        self.setup()
        response=self.client.get('/professor/%s/' % self.professorId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Professor.objects.all().delete()
        self.setup()
        id=int(self.professorId)+1
        response=self.client.get('/professor/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)


class TestPOST(APITestCase):
    def setup(self):
        departmentName='CSE'
        professerName='RKC'
        department=Department(departmentName=departmentName)
        department.save()
        department=Department.objects.get(departmentName=departmentName)
        self.department=department
        self.departmentId=department.departmentId
        professor=Professor(fname=professerName,lname=professerName,email='rkc@gmail.com',mobile='123456789',city='nanded',state='maha',department=self.department)
        professor.save()
        self.professorId=professor.professorId
        professor=Professor.objects.get(fname=professerName)
        self.professor=professor
        self.professorId=professor.professorId


    def test_post(self):
        Professor.objects.all().delete()
        self.setup()
        data={"fname":"rkc","lname":"rkc","email":"rkc@gmail.com","mobile":"123456789","city":"nanded","state":"maha","department":self.departmentId}
        response=self.client.post('/professor/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_post_exists(self):
        Professor.objects.all().delete()
        self.setup()
        data={"fname":"rkc","lname":"rkc","email":"rkc@gmail.com","mobile":"123456789","city":"nanded","state":"maha","department":int(self.departmentId)+1}
        response=self.client.post('/professor/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

 

class TestPUT(APITestCase):
    def setup(self):
        departmentName='CSE'
        professerName='RKC'
        department=Department(departmentName=departmentName)
        department.save()
        department=Department.objects.get(departmentName=departmentName)
        self.department=department
        self.departmentId=department.departmentId
        professor=Professor(fname=professerName,lname=professerName,email='rkc@gmail.com',mobile='123456789',city='nanded',state='maha',department=self.department)
        professor.save()
        professor=Professor.objects.get(fname=professerName)
        self.professor=professor
        self.professorId=professor.professorId

    def test_put(self):
        Professor.objects.all().delete()
        self.setup()
        department=Department(departmentName='EXTC')
        department.save()
        departmentId=Department.objects.get(departmentName='EXTC').departmentId
        data={"fname":"rkc","lname":"rkc","email":"rkc@gmail.com","mobile":"123456789","city":"nanded","state":"maha","department":departmentId}
        response=self.client.put('/professor/%s/' % self.professorId,data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_put_coflict(self):
        Professor.objects.all().delete()
        self.setup()
        data={"fname":"rkc","lname":"rkc","email":"rkc@gmail.com","mobile":"123456789","city":"nanded","state":"maha","department":int(self.departmentId)+1}
        response=self.client.put('/professor/%s/' % self.professorId,data,fomat='json')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

    def test_put_not_found(self):
        Professor.objects.all().delete()
        self.setup()
        id=int(self.professorId)+1
        departmentName="EXTC"
        department=Department(departmentName=departmentName)
        department.save()
        departmentId=Department.objects.get(departmentName='EXTC').departmentId
        data={"fname":"rkc","lname":"rkc","email":"rkc@gmail.com","mobile":"123456789","city":"nanded","state":"maha","department":departmentId}
        response=self.client.put('/professor/%s/' % id,data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)    

class TestDelete(APITestCase):
    def setup(self):
        departmentName='CSE'
        professerName='RKC'
        department=Department(departmentName=departmentName)
        department.save()
        department=Department.objects.get(departmentName=departmentName)
        self.department=department
        self.departmentId=department.departmentId
        professor=Professor(fname=professerName,lname=professerName,email='rkc@gmail.com',mobile='123456789',city='nanded',state='maha',department=self.department)
        professor.save()
        professor=Professor.objects.get(fname=professerName)
        self.professor=professor
        self.professorId=professor.professorId

    def test_delete(self):
        Professor.objects.all().delete()
        self.setup()
        response=self.client.delete('/professor/%s/' % self.professorId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)

    def test_delete_not_found(self):
        Professor.objects.all().delete()
        self.setup()
        id=int(self.professorId)+1
        response=self.client.delete('/professor/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)
    
    def test_all_delete(self):
        self.setup()
        response=self.client.delete('/professor/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)
