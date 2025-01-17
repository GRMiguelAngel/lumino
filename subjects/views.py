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
from .tasks import deliver_certificate
from .utils import non_teaching_teacher, student_enrolled

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
    if request.user.profile.is_teacher():
        return HttpResponseForbidden()
    if request.method == 'POST':
        if (form := EnrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.student_subjects.add(subject)
            messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')
    else:
        form = EnrollForm(request.user)
    return render(request, 'subjects/subject_enrollment.html', dict(form=form))


@login_required
def unenroll(request: HttpRequest) -> HttpResponse:
    if request.user.profile.is_teacher():
        return HttpResponseForbidden()
    if request.method == 'POST':
        if (form := UnenrollForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.student_subjects.remove(subject)
            messages.success(request, 'Successfully unenrolled from the chosen subjects.')

            return redirect('subjects:subject-list')
    else:
        form = UnenrollForm(request.user)
    return render(request, 'subjects/subject_enrollment.html', dict(form=form))


@login_required
@student_enrolled
@non_teaching_teacher
def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lessons = Lesson.objects.filter(subject=subject)
    if request.user.profile.is_student():
        enrollment = Enrollment.objects.get(student=request.user)
        return render(
            request,
            'subjects/subject_detail.html',
            dict(subject=subject, lessons=lessons, enrollment=enrollment),
        )

    return render(request, 'subjects/subject_detail.html', dict(subject=subject, lessons=lessons))


@login_required
@student_enrolled
@non_teaching_teacher
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(request, 'lessons/lesson_detail.html', dict(subject=subject, lesson=lesson))


@login_required
@non_teaching_teacher
def add_lesson(request: HttpRequest, subject_code: str) -> HttpResponse:
    if request.user.profile.is_student():
        return HttpResponseForbidden()
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(request.POST)).is_valid():
            form.save(subject)
            messages.success(request, 'Lesson was successfully added.')
            return redirect('subjects:subject-detail', subject.code)
    else:
        form = AddLessonForm()
    return render(request, 'lessons/add_lesson.html', dict(form=form))


@login_required
@non_teaching_teacher
def edit_lesson(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    if request.user.profile.is_student():
        return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            form.save()
            messages.success(request, 'Changes were successfully saved.')
            return render(
                request, 'lessons/lesson_detail.html', dict(subject=subject, lesson=lesson)
            )
    else:
        form = EditLessonForm(instance=lesson)
    return render(
        request, 'lessons/edit_lesson.html', dict(form=form, subject=subject, lesson=lesson)
    )


@login_required
@non_teaching_teacher
def delete_lesson(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    if request.user.profile.is_student():
        return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_pk)
    if request.user.profile.is_teacher() and request.user == lesson.subject.teacher:
        lesson.delete()
        messages.success(request, 'Lesson was successfully deleted.')
        return redirect('subjects:subject-detail', subject_code)
    else:
        return HttpResponseForbidden()


@login_required
@non_teaching_teacher
def marks_list(request: HttpRequest, subject_code: str) -> HttpResponse:
    if request.user.profile.is_student():
        return HttpResponseForbidden()
    subject = Subject.objects.get(code=subject_code)
    enrollments = subject.enrollment.all()
    return render(request, 'marks/marks_list.html', dict(enrollments=enrollments, subject=subject))


@login_required
@non_teaching_teacher
def edit_marks(request, subject_code: str):
    if request.user.profile.is_student():
        return HttpResponseForbidden()
    subject = Subject.objects.get(code=subject_code)

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
        'marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )


def request_certificate(request: HttpRequest) -> HttpResponse:
    deliver_certificate.delay()
    return render(request, 'subjects/certificate_confirmation.html')
