from django.http import HttpResponseForbidden

from .models import Subject

forbidden_msg = 'No tienes permiso para realizar esta acción.'


def student_enrolled(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        subject = Subject.objects.get(code=kwargs['subject_code'])
        if user.profile.is_student():
            if not subject.enrollment.filter(student=user).exists():
                return HttpResponseForbidden(forbidden_msg)
        return func(*args, **kwargs)

    return wrapper

def non_teaching_teacher(func):
    def wrapper(*args, **kwargs):
        user = args[0].user
        if user.profile.is_teacher():
            subject = Subject.objects.get(code=kwargs['subject_code'])
            if user != subject.teacher:
                return HttpResponseForbidden(forbidden_msg)
        return func(*args, **kwargs)    
    return wrapper

