from django.shortcuts import redirect

# Create your views here.


def index(request):
    if request.user:
        return redirect('subjects:subject-list')
    else:
        return redirect('login')