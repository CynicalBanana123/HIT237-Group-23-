from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
	"""Render the site home page (uses page_home.html template)."""
	return render(request, "page_home.html")


@login_required
def user_ticket(request):
	from .forms import TicketForm
	from .models import Ticket

	if request.method == 'POST':
		form = TicketForm(request.POST)
		if form.is_valid():
			ticket = form.save(commit=False)
			ticket.created_by = request.user
			ticket.save()
			return redirect('tickets:user_ticket')
	else:
		form = TicketForm()

	tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
	return render(request, 'tickets/user_ticket.html', {'form': form, 'tickets': tickets})


def ticket_list(request):
	"""Public ticket list (or admin view)."""
	from .models import Ticket
	tickets = Ticket.objects.order_by('-created_at')[:50]
	return render(request, 'page_tickets.html', {'tickets': tickets})
