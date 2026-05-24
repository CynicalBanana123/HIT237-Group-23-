# ADR-001: Separate Django Project into Tickets and Accounts Apps

## 20/05/2026 Revision:

### Status:
Approved

### Context
The project is a Django-based ticketing system that supports two account types: tenants and owners. The system includes authentication, ticket creation, ticket viewing, and ticket management features.

Initially, all functionality could have been placed inside a single Django application. However, combining authentication and ticket logic into one app would reduce maintainability and make the project harder to scale as more features are added.

To improve organization and separation of concerns, the project structure was divided into multiple feature-based Django apps.

### Alternative Solutions Considered

1. Single Application Structure
  - Pros
    - Easier initial setup
    - Simpler configuration
  - Cons
    - Difficult to maintain as the project grows
    - Poor separation of concerns

2. Multiple Django Apps (Chosen Solution)
  - Pros
    - Better project organization
    - Easier scalability and maintenance
  - Cons
    - More setup and configuration required
    - Requires communication between apps

### Solution Decided Upon:
The project will use two separate Django apps:

- `accounts`
  - Handles authentication and account management
  - Manages tenant and owner account types

- `tickets`
  - Handles ticket creation and ticket management
  - Stores ticket-related views and models

This structure separates authentication logic from ticket functionality while keeping the project modular and scalable.

### Consequences:
Separating the project into multiple Django apps improves maintainability, readability, and scalability. Developers can work on authentication and ticket functionality independently with reduced risk of affecting unrelated systems.

However, the project now requires additional app configuration and routing between apps.

### Code Reference:

```python
# Create Django apps
python manage.py startapp accounts
python manage.py startapp tickets
```

```python
# settings.py

INSTALLED_APPS = [
    'accounts',
    'tickets',
]
```