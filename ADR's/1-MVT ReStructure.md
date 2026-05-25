# ADR-001: Use Django MVT Structure for the Project

## Django MVT Structure Revision:

### Status:
Approved

### Context
The project is a Django-based housing ticketing system. It requires clear separation between data storage, request handling, page rendering, and URL routing.

Django’s MVT structure supports this separation by using Models for database structure, Views for request handling, Templates for HTML output, and URLs for routing user requests to the correct view.

### Alternative Solutions Considered

1. Place most logic directly inside templates
  - Pros
    - Faster to create simple pages
    - Less initial Python code required
  - Cons
    - Poor separation of concerns
    - Harder to maintain as the project grows

2. Use Django MVT Structure
  - Pros
    - Clear separation between models, views, templates, and URLs
    - Easier to scale and debug
  - Cons
    - Requires more files and structure
    - Takes longer to set up initially

### Solution Decided Upon:
The project will follow Django’s MVT architecture.

- Models will define database objects such as `Profile` and `Ticket`
- Views will handle requests and responses
- Templates will display pages such as dashboards and ticket forms
- URL files will connect browser paths to views

### Consequences:
This improves organisation and makes the project easier to understand. It also allows future features to be added without mixing database, HTML, and request logic together.

However, the project requires more files and clearer routing between apps.

### Code Reference:

```python
# tickets/models.py

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

```python
# tickets/urls.py

path('create/', views.TicketCreateView.as_view(), name='create')
path('<int:pk>/', views.TicketDetailView.as_view(), name='detail')
```