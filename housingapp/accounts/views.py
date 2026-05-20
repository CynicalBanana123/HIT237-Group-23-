from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required
from .forms import MixedLoginForm
from tickets.models import Ticket


def login_view(request):
	form = MixedLoginForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.get_user()
		auth_login(request, user)
		role = getattr(user, 'profile', None) and user.profile.role
		# Redirect all users to the dashboard home now provided by `accounts.home`.
		try:
			return redirect(reverse('accounts:home'))
		except NoReverseMatch:
			return redirect('/')
	return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
	auth_logout(request)
	return redirect('accounts:login')


def login(request):
	"""Alias for `login_view` so templates or imports can use `views.login`."""
	return login_view(request)


@login_required
def home(request):
	"""Dashboard home merged into `accounts` app; renders role-specific content."""
	role = getattr(request.user, 'profile', None) and request.user.profile.role
	if role == 'owner':
		tickets = Ticket.objects.all().order_by('-created_at')
		return render(request, 'dashboard/owner_home.html', {'role': role, 'user': request.user, 'tickets': tickets})
	else:
		return render(request, 'dashboard/tenant_home.html', {'role': role, 'user': request.user})


def index(request):
	"""Root view: send authenticated users to the dashboard home, others to login."""
	if request.user.is_authenticated:
		return redirect('accounts:home')
	return redirect('accounts:login')
