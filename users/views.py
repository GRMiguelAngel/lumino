from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from subjects.models import Subject

# Create your views here.


@login_required
def enroll(request: HttpRequest) -> HttpResponse:
    subjects = Subject.objects.all()
    return render(request, 'users/subject_enrollment.html', dict(subjects=subjects))
