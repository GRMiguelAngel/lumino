from subjects.models import Subject

def all_subjects(request):
    try:
        return {'subjects':Subject.objects.all()}
    except Subject.DoesNotExist:
        return {}