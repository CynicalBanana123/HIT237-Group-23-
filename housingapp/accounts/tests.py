from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileModelTests(TestCase):
	def test_profile_created_on_user_creation(self):
		u = User.objects.create_user(username='puser', password='pass')
		# profile should be auto-created by signals
		self.assertIsNotNone(getattr(u, 'profile', None))
		self.assertEqual(u.profile.role, 'tenant')
