"""Ticket models for the tickets app.

Includes a custom QuerySet to encapsulate frequently used filters and
optimisations (e.g. `with_creator` for select_related lookups).
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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


class Ticket(models.Model):
	STATUS_OPEN = 'open'
	STATUS_CLOSED = 'closed'
	STATUS_CHOICES = ((STATUS_OPEN, 'Open'), (STATUS_CLOSED, 'Closed'))

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
	created_at = models.DateTimeField(auto_now_add=True)

	"""Representation of a support/maintenance ticket.

	Fields:
	- `title`, `description`, `created_by` (FK to user), `status`, `created_at`.
	"""

	# Attach the custom queryset as the model manager
	objects = TicketQuerySet.as_manager()

	def __str__(self):
		return f"#{self.pk} {self.title} ({self.status})"
