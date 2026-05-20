from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse, NoReverseMatch
from .forms import MixedLoginForm


def login_view(request):
	form = MixedLoginForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.get_user()
		auth_login(request, user)
		role = getattr(user, 'profile', None) and user.profile.role
		# Redirect all users to the dashboard home (dashboard view will render role-specific content)
		try:
			return redirect(reverse('dashboard:home'))
		except NoReverseMatch:
			return redirect('/')
	return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
	auth_logout(request)
	return redirect('accounts:login')


def login(request):
	"""Alias for `login_view` so templates or imports can use `views.login`."""
	return login_view(request)
