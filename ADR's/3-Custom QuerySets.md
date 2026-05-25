# ADR-003: Use Custom QuerySets for Ticket Filtering

## Custom QuerySets and Filtering Revision:

### Status:
Approved

### Context
The dashboard and ticket views need to display different tickets depending on the user role.

Tenants should only see their own tickets, while owners should be able to view all submitted tickets. Ticket data also needs to be ordered and sometimes optimised with related user data.

Writing these queries directly in every view would cause duplication.

### Alternative Solutions Considered

1. Write all queries directly inside views
  - Pros
    - Simple to understand at first
    - No extra model methods required
  - Cons
    - Repeated query logic across views
    - Harder to update filtering rules later

2. Use Custom QuerySets
  - Pros
    - Reusable query logic
    - Keeps views cleaner
  - Cons
    - Requires extra model code
    - May be harder for beginners to follow

### Solution Decided Upon:
The project will use a custom `TicketQuerySet` to store common ticket queries.

This includes filtering open tickets, closed tickets, tickets for a specific user, newest tickets first, and tickets with creator data.

### Consequences:
Views can reuse query methods instead of repeating filter logic. This supports the Fat Models, Skinny Views approach and makes the code easier to maintain.

However, developers need to understand where query logic is stored.

### Code Reference:

```python
# tickets/models.py

class TicketQuerySet(models.QuerySet):
    def open(self):
        return self.filter(status=self.model.STATUS_OPEN)

    def closed(self):
        return self.filter(status=self.model.STATUS_CLOSED)

    def for_user(self, user):
        return self.filter(created_by=user)

    def newest_first(self):
        return self.order_by('-created_at')

    def with_creator(self):
        return self.select_related('created_by')
```

```python
# tickets/models.py

objects = TicketQuerySet.as_manager()
```