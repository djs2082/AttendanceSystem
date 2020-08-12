from django.urls import path
from hod.views import HodView

urlpatterns = [
    path('',HodView.as_view()),
    path('<int:pk>/',HodView.as_view())
]

