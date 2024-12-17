from django.shortcuts import redirect, render

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')

    return redirect('home')


def home(request):
    return render(request, 'home.html')
