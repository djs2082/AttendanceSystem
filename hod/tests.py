from django.test import TestCase
from rest_framework.test import APITestCase
from department.models import Department
from professor.models import Professor
from hod.models import HOD
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

    def test_insert(self):
        HOD.objects.all().delete()
        self.setup()
        old_count=HOD.objects.all().count()
        hod=HOD(departmentId=self.department,hod=self.professor)
        hod.save()
        new_count=HOD.objects.all().count()
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
        self.hod=HOD(departmentId=self.department,hod=self.professor)
        self.hod.save()
        self.hodId=HOD.objects.get(departmentId=self.departmentId).hodId


    def test_get(self):
        HOD.objects.all().delete()
        self.setup()
        response=self.client.get('/hod/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id(self):
        HOD.objects.all().delete()
        self.setup()
        response=self.client.get('/hod/%s/' % self.hodId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        HOD.objects.all().delete()
        self.setup()
        id=int(self.hodId)+1
        response=self.client.get('/hod/%s/' % id)
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


    def test_post(self):
        HOD.objects.all().delete()
        self.setup()
        data={"departmentId":self.departmentId,"hod":self.professorId}
        response=self.client.post('/hod/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_post_exists(self):
        HOD.objects.all().delete()
        self.setup()
        hod=HOD(departmentId=self.department,hod=self.professor)
        hod.save()
        data={"departmentId":self.departmentId,"hod":self.professorId}
        response=self.client.post('/hod/',data)
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
        self.hod=HOD(departmentId=self.department,hod=self.professor)
        self.hod.save()
        self.hodId=HOD.objects.get(departmentId=self.departmentId).hodId

    def test_put(self):
        HOD.objects.all().delete()
        self.setup()
        department=Department(departmentName='EXTC')
        department.save()
        departmentId=Department.objects.get(departmentName='EXTC').departmentId
        data={"departmentId":departmentId}
        response=self.client.put('/hod/%s/' % self.hodId,data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_put_coflict(self):
        HOD.objects.all().delete()
        self.setup()
        departmentName="EXTC"
        department=Department(departmentName=departmentName)
        department.save()
        hod=HOD(departmentId=department,hod=self.professor)
        hod.save()
        departmentId=Department.objects.get(departmentName='EXTC').departmentId
        data={"departmentId":departmentId}
        response=self.client.put('/hod/%s/' % self.hodId,data,fomat='json')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

    def test_put_not_found(self):
        HOD.objects.all().delete()
        self.setup()
        id=int(self.hodId)+1
        departmentName="EXTC"
        department=Department(departmentName=departmentName)
        department.save()
        departmentId=Department.objects.get(departmentName='EXTC').departmentId
        data={"departmentId":departmentId}
        response=self.client.put('/hod/%s/' % id,data)
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
        self.hod=HOD(departmentId=self.department,hod=self.professor)
        self.hod.save()
        self.hodId=HOD.objects.get(departmentId=self.departmentId).hodId

    def test_delete(self):
        HOD.objects.all().delete()
        self.setup()
        response=self.client.delete('/hod/%s/' % self.hodId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)

    def test_delete_not_found(self):
        HOD.objects.all().delete()
        self.setup()
        id=int(self.hodId)+1
        response=self.client.delete('/hod/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)
    
    def test_all_delete(self):
        self.setup()
        response=self.client.delete('/hod/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)