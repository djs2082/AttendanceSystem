from django.contrib import admin
from django.urls import path
from .views import SectionView


urlpatterns = [
    path('',SectionView.as_view()),
    path('<int:pk>/',SectionView.as_view())
]