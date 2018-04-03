'''from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return home(request)
    else:
        return HttpResponseNotFound("Invalid Login")
	
@login_required()
def home(request):
    return render(request, '3RS.html', {})


@login_required()
def logoutView(request):
    logout(request)
    return render(request, 'logout.html', {})'''