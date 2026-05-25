# ADR-006: Add a Service Layer for Ticket Business Logic

## Service Layer Revision:

### Status:
Approved

### Context
Some ticket actions require business rules that should not live directly inside views.

For example, creating a ticket must attach the logged-in user, deleting a ticket must check permissions, and changing ticket status should only be allowed for owners.

Placing this logic directly in views would make the views too large and harder to test.

### Alternative Solutions Considered

1. Keep all ticket logic inside views
  - Pros
    - Fewer files to manage
    - Easy to follow for very small projects
  - Cons
    - Views become too large
    - Business rules are harder to reuse and test

2. Move ticket workflows into a service layer
  - Pros
    - Keeps views focused on HTTP handling
    - Makes business logic reusable and testable
  - Cons
    - Adds another project layer
    - Requires clear naming and structure

### Solution Decided Upon:
The project will use a `tickets/services.py` file for ticket business logic.

The service layer will handle:

- ticket creation
- ticket deletion
- ticket status updates
- permission checks
- ownership rules

### Consequences:
Views become thinner and easier to read. Business rules can also be tested separately from page rendering.

However, developers need to know that some ticket logic is located in `services.py` rather than directly in views.

### Code Reference:

```python
# tickets/services.py

def create_ticket(user, form):
    ticket = form.save(commit=False)
    ticket.created_by = user
    ticket.save()
    return ticket
```

```python
# tickets/services.py

def delete_ticket(user, ticket):
    if not user_can_modify_ticket(user, ticket):
        raise TicketPermissionError("You do not have permission to delete this ticket.")
    ticket.delete()
```