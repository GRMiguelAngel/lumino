from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from subjects.models import Subject
from .models import Profile

# Create your views here.

@login_required
def user_detail(request: HttpRequest, user) -> HttpResponse:
    profile = Profile.objects.get(user=user)
    return render(request, 'users/user_profile.html', dict(profile=profile))
