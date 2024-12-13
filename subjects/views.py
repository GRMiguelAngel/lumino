from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AddLessonForm, EnrollForm, UnenrollForm
from .models import Lesson, Subject

# Create your views here.


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    if request.user.profile.is_teacher():
        teacher_subjects = Subject.objects.filter(teacher=request.user)
        student_subjects = Subject.objects.filter(students=request.user)
        return render(
            request,
            'subjects/subject_list.html',
            dict(teacher_subjects=teacher_subjects, student_subjects=student_subjects),
        )
    else:
        student_subjects = Subject.objects.filter(students=request.user)
        return render(
            request, 'subjects/subject_list.html', dict(student_subjects=student_subjects)
        )


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
    lessons = Lesson.objects.filter(subject=subject)
    return render(request, 'subjects/subject_detail.html', dict(subject=subject, lessons=lessons))


@login_required
def add_lesson(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            form.save(subject)
            return redirect('subjects:subject-detail', subject.code)
    else:
        form = AddLessonForm()
    return render(request, 'lessons/add_lesson.html', dict(form=form))


@login_required
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(request, 'lessons/lesson_detail.html', dict(subject=subject, lesson=lesson))
