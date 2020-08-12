
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/',admin.site.urls),
    path('subject/', include('subject.urls')),
    path('section/', include('section.urls')),
    path('year/',include('year.urls')),
    path('semester/', include('semester.urls')),
    path('req/',include('requirements.urls')),
    path('professor/',include('professor.urls')),
    path('class/',include('studentclass.urls')),
    path('department/',include('department.urls')),
    path('hod/',include('hod.urls')),
    path('student/',include('student.urls')),
    path('student-attendence/', include('student_attendence.urls'))

]
