from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Semester
# Create your tests here.
# database setup testing
class SemesterTest(TestCase):
    def setUp(self):
        self.semesterName   = "FIRST"
        self.semester       = Semester(semesterName=self.semesterName)

    def test_adding_to_database(self):
        old_count   = Semester.objects.count()
        self.semester.save()
        new_count   = Semester.objects.count()
        self.assertNotEqual(old_count, new_count)

# view testing 
class TestGET(APITestCase):

    def test_get_not_found(self):
        Semester.objects.all().delete()
        response = self.client.get('/semester/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get(self):
        semesterName    = 'FIRST'
        semester        = Semester(semesterName=semesterName)
        semester.save()
        response    = self.client.get('/semester/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id(self):
        semesterName    = 'SECOND'
        semester        = Semester(semesterName=semesterName)
        semester.save()
        data        = Semester.objects.get(semesterName='SECOND')
        response    = self.client.get('/semester/%s/' % data.semesterId)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Semester.objects.all().delete()
        semesterName    = 'SECOND'
        semester        = Semester(semesterName=semesterName)
        semester.save()
        data    = Semester.objects.get(semesterName='SECOND')
        id      = int(data.semesterId)+1
        response = self.client.get('/semester/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPOST(APITestCase):

    def test_post(self):
        Semester.objects.all().delete()
        data     = {"semesterName":"THIRD"}
        response = self.client.post('/semester/',data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_exists(self):
        Semester.objects.all().delete()
        semesterName    = "THIRD"
        semester        = Semester(semesterName=semesterName)
        semester.save()
        data    = {"semesterName":"THIRD"}
        response = self.client.post('/semester/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestPUT(APITestCase):

    def test_put(self):
        Semester.objects.all().delete()
        semesterName    = "FOURTH"
        semester        = Semester(semesterName=semesterName)
        semester.save()
        saved_data  = Semester.objects.get(semesterName='FOURTH')
        data        = {"semesterName":"FIFTH"}
        response    = self.client.put('/semester/%s/' % saved_data.semesterId, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_coflict(self):
        Semester.objects.all().delete()
        semesterName    = "FIFTH"
        semester        = Semester(semesterName=semesterName)
        semester.save()
        semesterName    = "SIXTH"
        semester    = Semester(semesterName=semesterName)
        semester.save()
        saved_data  = Semester.objects.get(semesterName='SIXTH')
        data        = {"semesterName":"FIFTH"}
        response    = self.client.put('/semester/%s/' % saved_data.semesterId, data, fomat='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_not_found(self):
        Semester.objects.all().delete()
        semesterName    = 'FOURTH'
        semester        = Semester(semesterName=semesterName)
        semester.save()
        data    = Semester.objects.get(semesterName='FOURTH')
        id      = int(data.semesterId)+1
        data    = {"semesterName":"SEVENTH"}
        response = self.client.put('/semester/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

class TestDelete(APITestCase):

    def test_delete(self):
        Semester.objects.all().delete()
        semester    = Semester(semesterName='FIRST')
        semester.save()
        saved_data  = Semester.objects.get(semesterName='FIRST')
        response=self.client.delete('/semester/%s/' % saved_data.semesterId)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_not_found(self):
        Semester.objects.all().delete()
        semester    = Semester(semesterName='EIGHTH')
        semester.save()
        saved_data  = Semester.objects.get(semesterName='EIGHTH')
        id  = int(saved_data.semesterId)+1
        response    = self.client.delete('/semester/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_all_delete(self):
    #     response    = self.client.delete('/semester/')
    #     self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)

    
