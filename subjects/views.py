from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AddLessonForm, EnrollForm, UnenrollForm
from .models import Subject

# Create your views here.


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = Subject.objects.filter(students=request.user)
    return render(request, 'subjects/subject_list.html', dict(subjects=subjects))


@login_required
def enroll(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := EnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.student_subjects.add(subject)
            return redirect('subjects:subject-list')
    else:
        form = EnrollForm(request.user)
    return render(request, 'subjects/subject_enrollment.html', dict(form=form))


@login_required
def unenroll(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := UnenrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.student_subjects.remove(subject)
            return redirect('subjects:subject-list')
    else:
        form = UnenrollForm(request.user)
    return render(request, 'subjects/subject_enrollment.html', dict(form=form))


@login_required
def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    return render(request, 'subjects/subject_detail.html', dict(subject=subject))


@login_required
def add_lesson(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.save()
            return redirect(lesson.subject)
    else:
        form = EnrollForm(request.user)
    return render(request, '')
