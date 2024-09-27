from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from validators import validate_alnum

class User(AbstractUser):
	username = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(3), validate_alnum])
	nickname = models.CharField(max_length=30)
	email = models.EmailField(unique=True)
	avatar = models.URLField(blank=True, null=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(default=timezone.now)
	friends = models.ForeignKey("self", related_name='friends', on_delete=models.SET_NULL)

	USERNAME_FIELD = username
	REQUIRED_FIELDS = ['email', 'nickname']

	# TODO: Model generation of user to do via manager later
	# TODO: objects = ManagerToBeDone()

	def __str__(self):
		return self.username

	def get_full_name(self):
		return self.nickname