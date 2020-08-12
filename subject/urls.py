from django.contrib import admin
from django.urls import path
from subject.views import SubjectView


urlpatterns = [
    path('',SubjectView.as_view()),
    path('<int:pk>/',SubjectView.as_view())
]