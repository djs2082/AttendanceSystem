from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Section

class SectionTest(TestCase):
    def setUp(self):
        self.sectionName="A"
        self.section=Section(sectionName=self.sectionName)

    def test_adding_to_database(self):
        old_count=Section.objects.count()
        self.section.save()
        new_count=Section.objects.count()
        self.assertNotEqual(old_count,new_count)

class TestGET(APITestCase):

    def test_get_not_found(self):
        Section.objects.all().delete()
        response=self.client.get('/section/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_get(self):
        sectionName='A'
        section=Section(sectionName=sectionName)
        section.save()
        response=self.client.get('/section/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_by_id(self):
        sectionName='B'
        section=Section(sectionName=sectionName)
        section.save()
        data=Section.objects.get(sectionName='B')
        response=self.client.get('/section/%s/' % data.sectionId)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        Section.objects.all().delete()
        sectionName='B'
        section=Section(sectionName=sectionName)
        section.save()
        data=Section.objects.get(sectionName='B')
        id=int(data.sectionId)+1
        response=self.client.get('/section/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class TestPOST(APITestCase):

    def test_post(self):
        Section.objects.all().delete()
        data={"sectionName":"C"}
        response=self.client.post('/section/',data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_post_exists(self):
        Section.objects.all().delete()
        sectionName="C"
        section=Section(sectionName=sectionName)
        section.save()
        data={"sectionName":"C"}
        response=self.client.post('/section/',data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class TestPUT(APITestCase):

    def test_put(self):
        Section.objects.all().delete()
        sectionName="D"
        section=Section(sectionName=sectionName)
        section.save()
        saved_data=Section.objects.get(sectionName='D')
        data={"sectionName":"Z"}
        response=self.client.put('/section/%s/' % saved_data.sectionId,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_put_coflict(self):
        Section.objects.all().delete()
        sectionName="E"
        section=Section(sectionName=sectionName)
        section.save()
        sectionName="Y"
        section=Section(sectionName=sectionName)
        section.save()
        saved_data=Section.objects.get(sectionName='Y')
        data={"sectionName":"E"}
        response=self.client.put('/section/%s/' % saved_data.sectionId,data,fomat='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_put_not_found(self):
        Section.objects.all().delete()
        sectionName='F'
        section=Section(sectionName=sectionName)
        section.save()
        data=Section.objects.get(sectionName='F')
        id=int(data.sectionId)
        data={"sectionName":"X"}
        response=self.client.put('/section/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)    

class TestDelete(APITestCase):

    def test_delete(self):
        Section.objects.all().delete()
        section=Section(sectionName='G')
        section.save()
        saved_data=Section.objects.get(sectionName='G')
        response=self.client.delete('/section/%s/' % saved_data.sectionId)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_delete(self):
        Section.objects.all().delete()
        section=Section(sectionName='H')
        section.save()
        saved_data=Section.objects.get(sectionName='H')
        id=int(saved_data.sectionId)+1
        response=self.client.delete('/section/%s/' % id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_all_delete(self):
        response=self.client.delete('/section/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
