from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AddLessonForm,
    EditLessonForm,
    EditMarksForm,
    EditMarksFormSetHelper,
    EnrollForm,
    UnenrollForm,
)
from .models import Enrollment, Lesson, Subject

# Create your views here.

forbidden_msg = 'No tienes permiso para realizar esta acción.'


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
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(request, 'lessons/lesson_detail.html', dict(subject=subject, lesson=lesson))


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
def edit_lesson(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            form.save()
            return redirect('subjects:lesson-detail', subject_code, lesson_pk)
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'lessons/edit_lesson.html', dict(form=form))


@login_required
def delete_lesson(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    if request.user.profile.is_teacher and request.user == lesson.subject.teacher:
        lesson.delete()
        return redirect('subjects:subject-detail', subject_code)
    else:
        return HttpResponseForbidden(forbidden_msg)


@login_required
def edit_marks(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)

    # breadcrumbs = Breadcrumbs()
    # breadcrumbs.add('My subjects', reverse('subjects:subject-list'))
    # breadcrumbs.add(subject.code, reverse('subjects:subject-detail', args=[subject.code]))
    # breadcrumbs.add('Marks', reverse('subjects:mark-list', args=[subject.code]))
    # breadcrumbs.add('Edit marks')

    MarkFormSet = modelformset_factory(Enrollment, EditMarksForm, extra=0)
    queryset = subject.enrollment.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarksFormSetHelper()
    return render(
        request,
        'marks/subject_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )
