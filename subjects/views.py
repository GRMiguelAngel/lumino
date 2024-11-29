from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Subject

# Create your views here.


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    if request.user.profile
        subjects = Subject.objects.filter(students=request.user)
    return render(request, 'subjects/subject_list.html', dict(subjects=subjects))
