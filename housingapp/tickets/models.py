from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ticket(models.Model):
	STATUS_OPEN = 'open'
	STATUS_CLOSED = 'closed'
	STATUS_CHOICES = ((STATUS_OPEN, 'Open'), (STATUS_CLOSED, 'Closed'))

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"#{self.pk} {self.title} ({self.status})"
