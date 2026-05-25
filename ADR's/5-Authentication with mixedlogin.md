# ADR-005: Add Authentication, User Roles, and Permission Mixins

## Authentication and User Roles Revision:

### Status:
Approved

### Context
The ticketing system requires different user types. Tenants need to create and view their own tickets, while owners need to view and manage submitted tickets.

Basic login protection is not enough because the project also requires role-based access control.

A `Profile` model can store each user’s role, and mixins can protect owner-only views.

### Alternative Solutions Considered

1. Use only Django’s built-in User model
  - Pros
    - Simple and already provided by Django
    - Works well for basic authentication
  - Cons
    - Does not store tenant/owner roles by default
    - Makes role-based access harder

2. Add Profile roles and permission mixins
  - Pros
    - Supports tenant and owner account types
    - Makes access control reusable
  - Cons
    - Requires extra model and signal logic
    - More testing is needed for permissions

### Solution Decided Upon:
The project will use Django authentication with a linked `Profile` model.

The `Profile` model will store whether a user is a tenant or owner. Login-required pages will use `LoginRequiredMixin`, and owner-only pages will use a custom `OwnerRequiredMixin`.

### Consequences:
This allows the system to show different dashboards and permissions depending on the user role.

However, role handling must be tested carefully to prevent tenants from accessing owner-only actions.

### Code Reference:

```python
# accounts/models.py

class Profile(models.Model):
    ROLE_TENANT = 'tenant'
    ROLE_OWNER = 'owner'

    ROLE_CHOICES = [
        (ROLE_TENANT, 'Tenant'),
        (ROLE_OWNER, 'Owner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

```python
# accounts/views.py

class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.role != 'owner':
            return HttpResponseForbidden("Owners only.")
        return super().dispatch(request, *args, **kwargs)
```