from django.contrib import admin
from django.urls import path
from year.views import yearView
from rest_framework import routers

router=routers.DefaultRouter()

urlpatterns = [
    path('',yearView.as_view()),
    path('<int:pk>/',yearView.as_view())
]