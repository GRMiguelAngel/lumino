from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll, name='enroll'),
    path('unenroll/', views.unenroll, name='unenroll'),
    path('<str:subject_code>/', views.subject_detail, name='subject-detail'),
    path('<str:subject_code>/lessons/<int:lesson_pk>', views.lesson_detail, name='lesson-detail'),
    path('<str:subject_code>/lessons/add/', views.add_lesson, name='add-lesson'),
]
