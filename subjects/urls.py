from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll, name='enroll'),
    path('unenroll/', views.unenroll, name='unenroll'),
    path('<subject_code>/', views.subject_detail, name='subject-detail'),
]
