from django.urls import path
from .views import SemesterView

urlpatterns = [
    path('',SemesterView.as_view()),
    path('<int:pk>/',SemesterView.as_view())
]