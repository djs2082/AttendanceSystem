from django.urls import path
from .views import StudentView, StudentSubjectView, StudentAttendanceView

urlpatterns = [
    path('',StudentView.as_view()),
    path('<int:pk>/',StudentView.as_view()),
    path('<int:pk>/subjects/',StudentSubjectView.as_view()),
    path('<int:pk>/attendance/',StudentAttendanceView.as_view())
]