from django.contrib import admin
from django.urls import path
from .views import DepartmentView


urlpatterns = [
    path('',DepartmentView.as_view()),
    path('<int:pk>/',DepartmentView.as_view())
]