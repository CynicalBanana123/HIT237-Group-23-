# ADR-007: Add Custom Exceptions, Tests, and API Support

## Testing, Exceptions, and API Revision:

### Status:
Approved

### Context
The project needs clearer error handling, automated testing, and optional API access.

Generic errors make it harder to understand why an action failed. The project also needs tests to confirm that permissions, ticket creation, and ticket management work correctly.

Django REST Framework can also expose ticket data as JSON for future frontend or mobile use.

### Alternative Solutions Considered

1. Use generic errors and manual testing only
  - Pros
    - Faster to write initially
    - Less setup required
  - Cons
    - Harder to identify specific failures
    - Bugs may not be caught early

2. Use custom exceptions, automated tests, and DRF
  - Pros
    - Clearer error handling
    - More reliable and testable project
  - Cons
    - Requires more files and setup
    - Tests and APIs need ongoing maintenance

### Solution Decided Upon:
The project will define custom ticket exceptions for permission and status errors.

The project will also include automated tests for models, services, views, permissions, and dashboard behaviour.

Django REST Framework will be included for an authenticated ticket API endpoint.

### Consequences:
This improves reliability and makes the project easier to validate. The API also allows the project to support non-HTML clients in the future.

However, API and test code increase the amount of project code that must be maintained.

### Code Reference:

```python
# tickets/services.py

class TicketPermissionError(Exception):
    """Raised when a user attempts an action they are not permitted to perform."""
```

```python
# tickets/services.py

class TicketStatusError(Exception):
    """Raised when attempting to set an invalid ticket status or illegal transition."""
```

```python
# tickets/tests.py

def test_tenant_cannot_delete_another_users_ticket(self):
    with self.assertRaises(TicketPermissionError):
        delete_ticket(self.tenant_user, self.other_ticket)
```

```python
# tickets/serializers.py

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'created_at']
```