# ADR-009: Testing Strategy

## Testing Suite Strategy:

### Status:
Approved

### Context
For this project, a test suite is required to verify the core functionality, permission boundaries and service layer behaviour. 
Without these tests, it becomes difficult to confirm role based access control and business rules behave properly as the project grows throughout it's life cycle.

### Alternative Solutions Considered

1. Manual Testing
  - Pros
    - No additional setup
    - Much faster for simple checks throughout development
  - Cons
    - Not reliable or repeatable
    - When features grow, scaling would be difficult
    - No documented evidence of correctness

2. Third Party Testing Frameworks
  - Pros
    - Expressive syntax
    - Management via pytest fixures
  - Cons
    - Heavier on dependency
    - Django provides a built in TestCase, offering pre established sufficient tools for the projects scope

### Solution Decided Upon:
To use Django's built in TestCase class across both test files. 
Files such as tickets/tests.py and accounts/tests.py will have tests written to verify meaningful behaviour rather than solely implementation details.

What is tested: 
- Custom QuerySets: tenant_tickets() returns only the tickets belonging to the specifc tenant that is requesting, with all_tickets() returning every ticket for the owner
- Models: The creation of tickets with correct field defaults, string representation and relationships to the user owner
- Service Layer: create_ticket() effectively attaches the logged in user, with delete_ticket()
  raising a TicketPermissionError when a user who isn't an owner of a ticket attempts to delete a ticket, that then update_ticket_status() raises a TicketStatusError
  for an invalid status transition
- Permission Boundaries: The owner-only views will promptly return a 403 or redirect when accessed by a tenant or unauthenticated user

What is not tested and why: 
- API Serializers: The DRF serializer endpoints are considered supplementary to the core application and were not prioritised given the project scope
- Full Integration/Testing on the Browser: End to end tests were considered out of scope for this assessment given the time constraints
  and due to the core user journeys only being covered by view-level tests.
- Templates: Template rendering is covered by view tests that return HTTP 200. Asserting the specific HTML content would
  create inefficient tests considering presentation.
- Deployment Configuration: Environment specific settings were not meaningful to test in a local test runner.

### Consequences:
  - Pros
    - Provides a confidence that role-based access control will work not only efficiently, but correctly.
    - Repeatable, with automated verification of permission logic and service behaviour.
    - Tests are independent of the implementation details and are gathered to test meaningful outcomes.
  - Cons
    - No end to end browser test, which could potentially cause UI-level bugs which would go undetected
    - The testing coverage does not extend to templates or configuration

### Code Reference:
```python
housingapp/tickets/tests.py - service, queryset, and permission boundary tests

housingapp/accounts/tests.py - account model and authentication tests
```

```bash
python manage.py check --deploy
python manage.py collectstatic
python manage.py migrate
```
