from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.generic import CreateView, FormView
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegistrationForm
	
class LoginView(FormView):
	form_class = LoginForm
	template_name = 'login.html'
	success_url = '/'
	
	def form_valid(self, form):
		request = self.request
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None
	
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		return super(LoginView, self).form_invalid(form)

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = RegistrationForm()
		context = {'form' : form}
		return render(request, 'register.html', context)

'''
class RegisterationView(CreateView):
	form_class = RegisterationForm
	template_name = 'register.html'
	success_url = '/login/'
	
	def form_valid(self, form):
		request = self.request
		next_ = request.GET.get('next')
		redirect_path = next_ or None
		
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		return super(LoginView, self).form_invalid(form)
'''