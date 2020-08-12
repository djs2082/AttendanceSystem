from django.test import TestCase
from rest_framework.test import APITestCase
from department.models import Department
from rest_framework import status
import json
class DepartmentTest(TestCase):
    def test_insert(self):
        departmentName='CSE'
        old_count=Department.objects.all().count()
        department=Department(departmentName=departmentName)
        department.save()
        new_count=Department.objects.all().count()
        self.assertNotEqual(old_count,new_count)

class TestGet(APITestCase):
    def test_get_not_found(self):
        Department.objects.all().delete()
        response=self.client.get('/department/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)


    def test_get(self):
        departmentName='CSE'
        department=Department(departmentName=departmentName)
        department.save()
        response=self.client.get('/department/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id(self):
        deprtmentName='CSE'
        department=Department(departmentName=deprtmentName)
        department.save()
        data=Department.objects.get(departmentName=deprtmentName)
        response=self.client.get('/department/%s/' % data.departmentId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Department.objects.all().delete()
        departmentName='CSE'
        department=Department(departmentName=departmentName)
        department.save()
        data=Department.objects.get(departmentName=departmentName)
        id=int(data.departmentId)+1
        response=self.client.get('/department/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)


class TestPOST(APITestCase):

    def test_post(self):
        Department.objects.all().delete()
        data={"departmentName":"CSE"}
        response=self.client.post('/department/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_post_exists(self):
        Department.objects.all().delete()
        departmentName="CSE"
        department=Department(departmentName=departmentName)
        department.save()
        data={"departmentName":"CSE"}
        response=self.client.post('/department/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

class TestPUT(APITestCase):

    def test_put(self):
        Department.objects.all().delete()
        departmentName="CSE"
        department=Department(departmentName=departmentName)
        department.save()
        saved_data=Department.objects.get(departmentName='CSE')
        data={"departmentName":"EXTC"}
        response=self.client.put('/department/%s/' % saved_data.departmentId,data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_put_coflict(self):
        Department.objects.all().delete()
        departmentName="CSE"
        department=Department(departmentName=departmentName)
        department.save()
        departmentName="EXTC"
        department=Department(departmentName=departmentName)
        department.save()
        saved_data=Department.objects.get(departmentName='EXTC')
        data={"departmentName":"CSE"}
        response=self.client.put('/department/%s/' % saved_data.departmentId,data,fomat='json')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

    def test_put_not_found(self):
        Department.objects.all().delete()
        departmentName='CSE'
        department=Department(departmentName=departmentName)
        department.save()
        data=Department.objects.get(departmentName='CSE')
        id=int(data.departmentId)+1
        data={"departmentName":"EXTC"}
        response=self.client.put('/department/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)    

class TestDelete(APITestCase):

    def test_delete(self):
        Department.objects.all().delete()
        department=Department(departmentName='CSE')
        department.save()
        saved_data=Department.objects.get(departmentName='CSE')
        response=self.client.delete('/department/%s/' % saved_data.departmentId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)

    def test_delete_not_found(self):
        Department.objects.all().delete()
        department=Department(departmentName='CSE')
        department.save()
        saved_data=Department.objects.get(departmentName='CSE')
        id=int(saved_data.departmentId)+1
        response=self.client.delete('/department/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)
    
    def test_all_delete(self):
        response=self.client.delete('/department/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)