from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from subject.models import Subject
from semester.models import Semester
from year.models import Year
from section.models import Section
from .models import StudentClass
# Create your tests here.
# database setup testing
class ClassTest(TestCase):
    def setUp(self):
        self.semesterName   = "FIRST"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'First Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="A"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()

    def test_adding_to_database(self):
        old_count   = StudentClass.objects.count()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)
        new_count   = StudentClass.objects.count()
        self.assertNotEqual(old_count, new_count)

# # view testing 
class TestGET(APITestCase):

    def test_get_not_found(self):
        StudentClass.objects.all().delete()
        response = self.client.get('/class/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get(self):
        self.semesterName   = "FIRST"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'First Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="A"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)
        response    = self.client.get('/class/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id(self):
        self.semesterName   = "THIRD"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Third Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="OSC"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="D"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)
        # data        = StudentClass.objects.get(section=self.section, year=self.year, semester=self.semester)
        response    = self.client.get('/class/%s/' % class_instance.classId)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)
        data        = StudentClass.objects.get(section=self.section, year=self.year, semester=self.semester)
        id      = int(data.classId)+1
        response = self.client.get('/class/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPOST(APITestCase):

    def test_post(self):
        StudentClass.objects.all().delete()
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        data     = {
            "section" : self.section.sectionId,
            "year" : self.year.yearId,
            "semester" : self.semester.semesterId,
            "subject" : [ self.subject.subjectId ]
            }
        response = self.client.post('/class/',data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_exists(self):
        StudentClass.objects.all().delete()
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        data     = {
            "section" : self.section.sectionId,
            "year" : self.year.yearId,
            "semester" : self.semester.semesterId,
            "subject" : [ self.subject.subjectId ]
            }
        response = self.client.post('/class/',data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestPUT(APITestCase):

    def test_put(self):
        StudentClass.objects.all().delete()
        #inserting new entry
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)

        # data for updation
        self.subjectName="USP"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="D"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        data     = {
            "section" : self.section.sectionId,
            "subject" : [ self.subject.subjectId ]
            }
        response    = self.client.put('/class/%s/' % class_instance.classId, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_coflict(self):
        StudentClass.objects.all().delete()
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance1 = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance1.save()
        class_instance1.subject.add(self.subject)

        data     = {
            "section" : self.section.sectionId,
            "year" : self.year.yearId,
            "semester" : self.semester.semesterId,
            "subject" : [ self.subject.subjectId ]
            }

        
        self.semesterName   = "FIRST"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Third Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="DAA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="A"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance2 = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance2.save()
        class_instance2.subject.add(self.subject)

        response    = self.client.put('/class/%s/' % class_instance2.classId, data, fomat='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_not_found(self):
        Semester.objects.all().delete()
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance1 = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance1.save()
        class_instance1.subject.add(self.subject)
        id      = int(class_instance1.classId)+1
        response = self.client.put('/class/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

class TestDelete(APITestCase):

    def test_delete(self):
        Semester.objects.all().delete()
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance.save()
        class_instance.subject.add(self.subject)
        response=self.client.delete('/class/%s/' % class_instance.classId)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_not_found(self):
        self.semesterName   = "SECOND"
        self.semester       = Semester(semesterName=self.semesterName)
        self.semester.save()
        self.yearName       = 'Second Year'
        self.year           = Year(yearName=self.yearName)
        self.year.save()
        self.subjectName="JAVA"
        self.subject=Subject(subjectName=self.subjectName)
        self.subject.save()
        self.sectionName="C"
        self.section=Section(sectionName=self.sectionName)
        self.section.save()
        class_instance1 = StudentClass(section=self.section, year=self.year, semester=self.semester)
        class_instance1.save()
        class_instance1.subject.add(self.subject)
        id      = int(class_instance1.classId)+1
        response    = self.client.delete('/semester/%s/' % id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_all_delete(self):
    #     response    = self.client.delete('/semester/')
    #     self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)

    
