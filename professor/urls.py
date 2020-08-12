from django.urls import path
from professor import views
# from professor.views import ProfessorView
urlpatterns = [
    path('api/students_attend/<int:sub_id>/<int:class_id>/',views.get_date_attenence),
    path('api/students_week_attend/<int:sub_id>/<int:class_id>/',views.get_week_attenence),
    path('api/students_sub/<int:sub_id>/',views.get_students_sub),
    path('api/students_prof/<int:prof_id>/',views.get_students_professor),
    path('api/students_class/<int:class_id>/',views.get_students_class),
    path('api/class/<int:prof_id>/',views.get_class),
    path('<int:pk>/',views.ProfessorView.as_view()),
    path('',views.ProfessorView.as_view())
]
