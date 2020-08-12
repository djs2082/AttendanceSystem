from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Subject
# Create your tests here.
class SubjectTest(TestCase):
    def setUp(self):
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)

    def test_adding_to_database(self):
        old_count=Subject.objects.count()
        self.subject.save()
        new_count=Subject.objects.count()
        self.assertNotEqual(old_count,new_count)

class TestGET(APITestCase):

    def test_get_not_found(self):
        Subject.objects.all().delete()
        response=self.client.get('/subject/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    def test_get(self):
        subjectName='JAVA'
        subject=Subject(subjectName=subjectName)
        subject.save()
        response=self.client.get('/subject/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_by_id(self):
        subjectName='PHP'
        subject=Subject(subjectName=subjectName)
        subject.save()
        data=Subject.objects.get(subjectName='PHP')
        response=self.client.get('/subject/%s/' % data.subjectId)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Subject.objects.all().delete()
        subjectName='PHP'
        subject=Subject(subjectName=subjectName)
        subject.save()
        data=Subject.objects.get(subjectName='PHP')
        id=int(data.subjectId)+1
        response=self.client.get('/subject/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class TestPOST(APITestCase):

    def test_post(self):
        Subject.objects.all().delete()
        data={"subjectName":"Electronics"}
        response=self.client.post('/subject/',data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_post_exists(self):
        Subject.objects.all().delete()
        subjectName="Electronics"
        subject=Subject(subjectName=subjectName)
        subject.save()
        data={"subjectName":"Electronics"}
        response=self.client.post('/subject/',data)
        self.assertEqual(response.status_code,status.HTTP_409_CONFLICT)

class TestPUT(APITestCase):

    def test_put(self):
        Subject.objects.all().delete()
        subjectName="Compilers"
        subject=Subject(subjectName=subjectName)
        subject.save()
        saved_data=Subject.objects.get(subjectName='Compilers')
        data={"subjectName":"Networking"}
        response=self.client.put('/subject/%s/' % saved_data.subjectId,data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_put_coflict(self):
        Subject.objects.all().delete()
        subjectName="ED"
        subject=Subject(subjectName=subjectName)
        subject.save()
        subjectName="Physics"
        subject=Subject(subjectName=subjectName)
        subject.save()
        saved_data=Subject.objects.get(subjectName='Physics')
        data={"subjectName":"ED"}
        response=self.client.put('/subject/%s/' % saved_data.subjectId,data,fomat='json')
        self.assertEqual(response.status_code,status.HTTP_409_CONFLICT)

    def test_put_not_found(self):
        Subject.objects.all().delete()
        subjectName='Chemistry'
        subject=Subject(subjectName=subjectName)
        subject.save()
        data=Subject.objects.get(subjectName='Chemistry')
        id=int(data.subjectId)+1
        data={"subjectName":"Maths"}
        response=self.client.put('/subject/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)    

class TestDelete(APITestCase):

    def test_delete(self):
        Subject.objects.all().delete()
        subject=Subject(subjectName='Jquery')
        subject.save()
        saved_data=Subject.objects.get(subjectName='Jquery')
        response=self.client.delete('/subject/%s/' % saved_data.subjectId)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)

    def test_delete_not_found(self):
        Subject.objects.all().delete()
        subject=Subject(subjectName='OSC')
        subject.save()
        saved_data=Subject.objects.get(subjectName='OSC')
        id=int(saved_data.subjectId)+1
        response=self.client.delete('/subject/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_all_delete(self):
        response=self.client.delete('/subject/')
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
