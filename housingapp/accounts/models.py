from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

User = get_user_model()


class Profile(models.Model):
	ROLE_TENANT = 'tenant'
	ROLE_OWNER = 'owner'
	ROLE_CHOICES = (
		(ROLE_TENANT, 'Tenant'),
		(ROLE_OWNER, 'Owner'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_TENANT)

	def __str__(self):
		return f"{self.user.get_username()} ({self.role})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	# ensure profile exists and is saved
	try:
		instance.profile.save()
	except Profile.DoesNotExist:
		Profile.objects.create(user=instance)
