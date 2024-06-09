from django.urls import path
from . import views
app_name = 'student'

urlpatterns = [
    path('add_student/', views.add_student, name='add_student'),
    path('professors/', views.professors_list, name='professors_list'),
    path('professor_detail/<int:professor_id>/', views.professor_detail, name='professor_detail'),
    path('<int:project_id>/send_request/', views.send_request, name='send_request'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('sent-requests/',views.sent_requests_list,name='sent_requests_list'),
    path('student_profile/<int:student_id>/', views.student_profile, name='student_profile'),
]
