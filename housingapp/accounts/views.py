"""Account views: login, logout, dashboard and account management.

Where appropriate, views defer business rules to the `Profile` model and
to dedicated service modules. Owner-only views use `OwnerRequiredMixin`.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView
from django.http import HttpResponseForbidden

from django.contrib.auth.forms import UserCreationForm
from .forms import MixedLoginForm
from tickets.models import Ticket
from .models import Profile


class OwnerRequiredMixin:
	"""Mixin that restricts access to users with the 'owner' role.

	Views using this mixin should be subclassed after Django's class-based
	mixins (for example `LoginRequiredMixin`) to ensure `request.user` is set.
	"""
	def dispatch(self, request, *args, **kwargs):
		role = getattr(request.user, 'profile', None) and request.user.profile.role
		if role != 'owner':
			return HttpResponseForbidden("Owners only.")
		return super().dispatch(request, *args, **kwargs)


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
		tickets = Ticket.objects.with_creator().newest_first()
		return render(request, 'dashboard/owner_home.html', {'role': role, 'user': request.user, 'tickets': tickets})
	else:
		# show the tenant's own recent tickets on their dashboard
		tickets = Ticket.objects.for_user(request.user).newest_first()
		return render(request, 'dashboard/tenant_home.html', {'role': role, 'user': request.user, 'tickets': tickets})


def index(request):
	"""Root view: send authenticated users to the dashboard home, others to login."""
	if request.user.is_authenticated:
		return redirect('accounts:home')
	return redirect('accounts:login')



class CreateListingView(LoginRequiredMixin, OwnerRequiredMixin, View):
	"""Simple placeholder CBV for creating a property listing; owners only."""

	def get(self, request, *args, **kwargs):
		return render(request, 'create_listing.html')

	def post(self, request, *args, **kwargs):
		# placeholder: in a real app you'd save a Listing model
		return redirect('accounts:home')


class SignupView(CreateView):
	"""Signup view using Django's `UserCreationForm`. Optionally accepts a `role` field in the form.

	If a `role` value is posted, it will be applied to the user's `Profile`.
	"""
	form_class = UserCreationForm
	template_name = 'accounts/signup.html'

	def form_valid(self, form):
		# save user (don't call super().form_valid which expects a model)
		user = form.save()

		# set role if provided; deliberately avoid swallowing unexpected errors
		role = self.request.POST.get('role')
		profile, created = Profile.objects.get_or_create(user=user)

		if role in dict(Profile.ROLE_CHOICES):
			profile.role = role
			profile.save()

		auth_login(self.request, user)
		return redirect(reverse('accounts:home'))

