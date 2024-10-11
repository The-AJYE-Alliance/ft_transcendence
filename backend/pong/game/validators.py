from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_start_date(created_date, start_date):
	if start_date and start_date < created_date:
		raise ValidationError(_("The start date cannot be earlier than the tournament creation date."))