from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit-profile'),
    path('leave/', views.user_leave, name='user-leave'),
]
