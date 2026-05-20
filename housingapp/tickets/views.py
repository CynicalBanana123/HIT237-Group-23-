from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket


@login_required
def ticket_create(request):
	form = TicketForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		ticket = form.save(commit=False)
		ticket.created_by = request.user
		ticket.save()
		return redirect('tickets:list')
	return render(request, 'tickets/create.html', {'form': form})


@login_required
def ticket_list(request):
	tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
	return render(request, 'tickets/list.html', {'tickets': tickets})
