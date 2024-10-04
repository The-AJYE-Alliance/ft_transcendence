from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

	def create_user(self, username, email, nickname, password=None):
		if not username:
			raise TypeError(_('No username provided'))
		user = self.model(username=username, email=self.normalize_email(email), nickname=nickname)
		user.set_password(password)
		user.clean_fields()
		user.save()
		return user

	def create_superuser(self, username, email, nickname, password):
		if not username:
			raise TypeError(_('No username provided'))
		if not password:
			raise TypeError(_('No password provided'))
		user = self.model(
            username=username,
            email=self.normalize_email(email),
            nickname=nickname,
            password=password,
        )
		user.is_admin = True
		user.save()
		return user