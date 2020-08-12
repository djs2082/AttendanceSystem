from django.urls import path
from .views import StudentClassView

urlpatterns = [
    path('',StudentClassView.as_view()),
    path('<int:pk>/',StudentClassView.as_view())
]
