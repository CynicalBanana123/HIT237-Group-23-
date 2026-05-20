from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from tickets.models import Ticket


@login_required
def home(request):
    role = getattr(request.user, 'profile', None) and request.user.profile.role
    if role == 'owner':
        # owner-specific dashboard: show all tickets
        tickets = Ticket.objects.all().order_by('-created_at')
        return render(request, 'dashboard/owner_home.html', {'role': role, 'user': request.user, 'tickets': tickets})
    else:
        # tenant-specific dashboard
        return render(request, 'dashboard/tenant_home.html', {'role': role, 'user': request.user})


def index(request):
    """Root view: send authenticated users to the dashboard home, others to login."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return redirect('accounts:login')
from django.shortcuts import render

# Create your views here.
