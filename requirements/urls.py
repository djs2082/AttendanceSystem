from django.urls import path
from requirements import authentication
urlpatterns = [
    path('auth/<str:token>',authentication.Authentication.as_view())
]
