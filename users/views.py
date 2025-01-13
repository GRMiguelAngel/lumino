from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import EditProfileForm
from .models import Profile

# Create your views here.

forbidden_msg = 'No tienes permiso para realizar esta acción.'


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    return render(request, 'users/user_profile.html', dict(profile=profile))


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    profile = request.user.profile
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            form.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('user-detail', request.user)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', dict(form=form))


@login_required
def user_leave(request: HttpRequest) -> HttpResponse:
    if request.user.profile.is_teacher():
        return HttpResponseForbidden(forbidden_msg)
    request.user.delete()
    messages.success(request, 'Good bye! Hope to see you soon.')
    return redirect('index')
