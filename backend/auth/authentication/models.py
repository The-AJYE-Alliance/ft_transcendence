from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
	email = models.EmailField(unique=True)
	avatar = models.URLField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(default=timezone.now)

	groups = models.ManyToManyField(
		'auth.Group',
		related_name='custom_user_set'
	)

	user_permissions = models.ManyToManyField(
		'auth.Permission',
		related_name='custom_user_permissions_set',
	)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'