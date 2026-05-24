"""Ticket views implemented as class-based views.

Views in this module are intentionally thin: they handle request/response
behaviour and delegate business rules to the services module.
"""

from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TicketForm
from .models import Ticket
from .services import (
	create_ticket,
	delete_ticket,
	user_can_view_ticket,
	user_can_modify_ticket,
	TicketPermissionError,
    update_ticket_status,
    TicketStatusError,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


class TicketListView(LoginRequiredMixin, ListView):
	model = Ticket
	template_name = 'tickets/ticket_list.html'
	context_object_name = 'tickets'
	paginate_by = 5

	def get_queryset(self):
		# Owners should see all tickets; tenants see only their own
		role = getattr(self.request.user, 'profile', None) and self.request.user.profile.role

		if role == 'owner':
			return Ticket.objects.with_creator().newest_first()

		return Ticket.objects.for_user(self.request.user).newest_first()


class TicketDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Ticket
	template_name = 'tickets/detail.html'
	context_object_name = 'ticket'

	def test_func(self):
		ticket = self.get_object()
		return user_can_view_ticket(self.request.user, ticket)


class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	form_class = TicketForm
	template_name = 'tickets/create.html'

	def form_valid(self, form):
		# delegate creation to service layer
		try:
			ticket = create_ticket(self.request.user, form)
		except Exception:
			form.add_error(None, 'Could not create ticket')
			return self.form_invalid(form)
		return redirect('accounts:home')


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Ticket
	form_class = TicketForm
	template_name = 'tickets/create.html'

	def test_func(self):
		ticket = self.get_object()
		return user_can_modify_ticket(self.request.user, ticket)

	def get_success_url(self):
		return reverse_lazy('tickets:detail', kwargs={'pk': self.object.pk})


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Ticket
	template_name = 'tickets/confirm_delete.html'
	success_url = reverse_lazy('accounts:home')

	def test_func(self):
		ticket = self.get_object()
		return user_can_modify_ticket(self.request.user, ticket)

	def form_valid(self, form):
		self.object = self.get_object()

		try:
			delete_ticket(self.request.user, self.object)
		except TicketPermissionError:
			raise Http404()

		return redirect(self.success_url)


@login_required
def close_ticket(request, pk):
	"""Owner-only view to close a ticket via the service layer.

	Expects POST and redirects back to the ticket detail.
	"""
	if request.method != 'POST':
		raise Http404()

	ticket = get_object_or_404(Ticket, pk=pk)

	try:
		update_ticket_status(request.user, ticket, Ticket.STATUS_CLOSED)
	except (TicketPermissionError, TicketStatusError):
		raise Http404()

	return redirect('tickets:detail', pk=pk)
