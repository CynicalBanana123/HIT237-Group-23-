# ADR-004: Use Class-Based Views for Ticket Pages

## Class-Based Views Revision:

### Status:
Approved

### Context
The ticketing system includes repeated page behaviours such as creating tickets, viewing ticket details, updating tickets, and deleting tickets.

These behaviours can be written using function-based views, but this may lead to duplicated logic as the project grows.

Django Class-Based Views provide reusable generic views for common CRUD actions.

### Alternative Solutions Considered

1. Use Function-Based Views
  - Pros
    - Easier to understand for small views
    - More explicit control over request logic
  - Cons
    - Can become repetitive
    - Less reusable for standard CRUD pages

2. Use Class-Based Views
  - Pros
    - Reduces repeated CRUD code
    - Supports reusable methods like `get_queryset()` and `form_valid()`
  - Cons
    - Can be harder to understand initially
    - Requires knowledge of Django generic views

### Solution Decided Upon:
The project will use Class-Based Views for ticket operations.

The main ticket views will include:

- `TicketCreateView`
- `TicketDetailView`
- `TicketUpdateView`
- `TicketDeleteView`

The dashboard will act as the main ticket list instead of requiring a separate ticket list page.

### Consequences:
This makes the project more scalable and aligns with Django’s reusable CRUD structure. It also allows permission and filtering logic to be placed in methods such as `get_queryset()`.

However, CBVs can be less obvious than function-based views for new developers.

### Code Reference:

```python
# tickets/views.py

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/detail.html'
    context_object_name = 'ticket'
```

```python
# tickets/urls.py

path('<int:pk>/', views.TicketDetailView.as_view(), name='detail')
path('<int:pk>/update/', views.TicketUpdateView.as_view(), name='update')
path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete')
```