from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import EditProfileForm
from .models import Profile

# Create your views here.


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    return render(request, 'users/user_profile.html', dict(profile=profile))


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    profile = Profile.objects.get(user=request.user)
    username = profile.user.username
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            form.save()
            return redirect('user-detail', username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', dict(form=form, username=username))


@login_required
def user_leave(request: HttpRequest) -> HttpResponse:
    request.user.delete()
    return redirect('home')
