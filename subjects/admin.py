from django.contrib import admin

from .models import Enrollment, Lesson, Subject

# Register your models here.


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    inlines = [EnrollmentInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
