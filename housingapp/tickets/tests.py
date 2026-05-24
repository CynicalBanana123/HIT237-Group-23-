from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Ticket

User = get_user_model()


class TicketQuerySetTests(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='u1', password='pass')
		self.user2 = User.objects.create_user(username='u2', password='pass')

		t1 = Ticket.objects.create(title='T1', description='d', created_by=self.user1, status=Ticket.STATUS_OPEN)
		t2 = Ticket.objects.create(title='T2', description='d', created_by=self.user1, status=Ticket.STATUS_CLOSED)
		t3 = Ticket.objects.create(title='T3', description='d', created_by=self.user2, status=Ticket.STATUS_OPEN)

		now = timezone.now()
		Ticket.objects.filter(pk=t1.pk).update(created_at=now - timedelta(days=1))
		Ticket.objects.filter(pk=t2.pk).update(created_at=now)
		Ticket.objects.filter(pk=t3.pk).update(created_at=now - timedelta(hours=1))

	def test_for_user(self):
		qs = Ticket.objects.for_user(self.user1)
		self.assertEqual(qs.count(), 2)

	def test_open_closed(self):
		self.assertEqual(Ticket.objects.open().count(), 2)
		self.assertEqual(Ticket.objects.closed().count(), 1)

	def test_newest_first(self):
		qs = Ticket.objects.for_user(self.user1).newest_first()
		titles = list(qs.values_list('title', flat=True))
		self.assertEqual(titles, ['T2', 'T1'])


class TicketModelAndViewTests(TestCase):
	def setUp(self):
		self.tenant1 = User.objects.create_user(username='tenant1', password='pass')
		self.tenant2 = User.objects.create_user(username='tenant2', password='pass')
		self.owner = User.objects.create_user(username='owner', password='pass')
		# set owner role
		self.owner.profile.role = 'owner'
		self.owner.profile.save()

		self.ticket_other = Ticket.objects.create(title='Other', description='x', created_by=self.tenant2)

	def test_ticket_str(self):
		t = Ticket.objects.create(title='Hello', description='d', created_by=self.tenant1)
		self.assertIn('Hello', str(t))

	def test_login_required_for_list(self):
		from django.urls import reverse
		resp = self.client.get(reverse('tickets:list'))
		self.assertEqual(resp.status_code, 302)

	def test_tenant_cannot_view_another_users_ticket(self):
		from django.urls import reverse
		self.client.login(username='tenant1', password='pass')
		resp = self.client.get(reverse('tickets:detail', args=[self.ticket_other.pk]))
		self.assertIn(resp.status_code, (403, 404))

	def test_owner_can_view_any_ticket(self):
		from django.urls import reverse
		self.client.login(username='owner', password='pass')
		resp = self.client.get(reverse('tickets:detail', args=[self.ticket_other.pk]))
		self.assertEqual(resp.status_code, 200)


class TicketServiceTests(TestCase):
	def setUp(self):
		self.tenant = User.objects.create_user(username='t', password='pass')
		self.other = User.objects.create_user(username='o', password='pass')

	def test_create_ticket_service(self):
		from .forms import TicketForm
		from .services import create_ticket
		form = TicketForm({'title': 'New', 'description': 'd'})
		self.assertTrue(form.is_valid())
		ticket = create_ticket(self.tenant, form)
		self.assertEqual(ticket.created_by, self.tenant)

	def test_delete_ticket_permission(self):
		from .services import delete_ticket, TicketPermissionError
		t = Ticket.objects.create(title='X', description='d', created_by=self.other)
		with self.assertRaises(TicketPermissionError):
			delete_ticket(self.tenant, t)
