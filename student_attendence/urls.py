from django.contrib import admin
from django.urls import path
from student_attendence import views


urlpatterns = [
    path('',views.StudentAttendanceView.as_view()),
    path('<int:pk>/',views.StudentAttendanceView.as_view())
]