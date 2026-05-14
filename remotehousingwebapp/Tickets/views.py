from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import TicketForm
from .models import Ticket


# Create your views here.
def home(request):
    """Render the site home page (uses page_home.html template)."""
    return render(request, "page_home.html")


@login_required
def user_ticket(request):
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
    return render(request, 'tickets/user_ticket.html', {
        'form': form,
        'tickets': tickets
    })


@login_required
def ticket_list(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'user_tickets/page_tickets.html', {
        'tickets': tickets
    })


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully.')
            return redirect('tickets:ticket_list')
    else:
        form = TicketForm()

    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'user_tickets/page_tickets_create.html', {
        'form': form,
        'tickets': tickets
    })


@login_required
def ticket_detail(request, id):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, id=id)
    else:
        ticket = get_object_or_404(Ticket, id=id, created_by=request.user)

    return render(request, 'user_tickets/page_tickets_detail.html', {
        'ticket': ticket
    })
