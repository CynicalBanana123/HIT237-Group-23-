# ADR-002: Implement Ticket CRUD Using Forms and Templates

## Ticket CRUD and Forms Revision:

### Status:
Approved

### Context
The ticketing system requires users to create, view, update, and delete maintenance tickets. These operations are core CRUD features.

Initially, ticket data could be manually handled inside views using raw request data. However, this would make validation and maintenance harder.

Django ModelForms provide a cleaner way to generate forms directly from models and validate submitted data.

### Alternative Solutions Considered

1. Manually handle form data in views
  - Pros
    - Full control over form processing
    - Simple for very small forms
  - Cons
    - More repeated code
    - Validation becomes harder to maintain

2. Use Django ModelForms
  - Pros
    - Automatically connects forms to models
    - Provides built-in validation
  - Cons
    - Requires a separate forms file
    - May need customisation for advanced layouts

### Solution Decided Upon:
The project will use Django ModelForms for ticket creation and updating.

The `TicketForm` will handle user input, while the ticket views will display forms, validate submissions, and redirect users after successful actions.

### Consequences:
This reduces repeated code and keeps ticket forms connected to the `Ticket` model. It also makes the create and update features easier to maintain.

However, extra form customisation may be needed if the UI becomes more complex.

### Code Reference:

```python
# tickets/forms.py

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
```

```python
# tickets/views.py

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/create.html'
```