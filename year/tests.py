from django.test import TestCase
from rest_framework.test import APITestCase
from year.models import Year
from rest_framework import status
import json
class YearTest(TestCase):
    def test_insert(self):
        yearName='First Year'
        old_count=Year.objects.all().count()
        year=Year(yearName=yearName)
        year.save()
        new_count=Year.objects.all().count()
        self.assertNotEqual(old_count,new_count)

class TestGet(APITestCase):
    def test_get_not_found(self):
        Year.objects.all().delete()
        response=self.client.get('/year/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)


    def test_get(self):
        yearName='First Year'
        year=Year(yearName=yearName)
        year.save()
        response=self.client.get('/year/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id(self):
        yearName='First Year'
        year=Year(yearName=yearName)
        year.save()
        data=Year.objects.get(yearName=yearName)
        response=self.client.get('/year/%s/' % data.yearId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Year.objects.all().delete()
        yearName='First Year'
        year=Year(yearName=yearName)
        year.save()
        data=Year.objects.get(yearName=yearName)
        id=int(data.yearId)+1
        response=self.client.get('/year/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)


class TestPOST(APITestCase):

    def test_post(self):
        Year.objects.all().delete()
        data={"yearName":"First Year"}
        response=self.client.post('/year/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_post_exists(self):
        Year.objects.all().delete()
        yearName="First Year"
        year=Year(yearName=yearName)
        year.save()
        data={"yearName":"First Year"}
        response=self.client.post('/year/',data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

class TestPUT(APITestCase):

    def test_put(self):
        Year.objects.all().delete()
        yearName="First Year"
        year=Year(yearName=yearName)
        year.save()
        saved_data=Year.objects.get(yearName='First Year')
        data={"subjectName":"Second Year"}
        response=self.client.put('/year/%s/' % saved_data.yearId,data)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_201_CREATED)

    def test_put_coflict(self):
        Year.objects.all().delete()
        yearName="First Year"
        year=Year(yearName=yearName)
        year.save()
        yearName="Second Year"
        year=Year(yearName=yearName)
        year.save()
        saved_data=Year.objects.get(yearName='Second Year')
        data={"yearName":"First Year"}
        response=self.client.put('/year/%s/' % saved_data.yearId,data,fomat='json')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_409_CONFLICT)

    def test_put_not_found(self):
        Year.objects.all().delete()
        yearName='First Year'
        year=Year(yearName=yearName)
        year.save()
        data=Year.objects.get(yearName='First Year')
        id=int(data.yearId)+1
        data={"yearName":"Second Year"}
        response=self.client.put('/year/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)    

class TestDelete(APITestCase):

    def test_delete(self):
        Year.objects.all().delete()
        year=Year(yearName='First Year')
        year.save()
        saved_data=Year.objects.get(yearName='First Year')
        response=self.client.delete('/year/%s/' % saved_data.yearId)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)

    def test_delete_not_found(self):
        Year.objects.all().delete()
        year=Year(yearName='First Year')
        year.save()
        saved_data=Year.objects.get(yearName='First Year')
        id=int(saved_data.yearId)+1
        response=self.client.delete('/year/%s/' % id)
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_404_NOT_FOUND)
    
    def test_all_delete(self):
        response=self.client.delete('/year/')
        self.assertEqual(json.loads(response.content)['Status'],status.HTTP_202_ACCEPTED)