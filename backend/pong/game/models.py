from django.db import models
from auth.authentication.models import User

class BaseMatch(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	duration = models.DurationField(null=True, blank=True)
	score_player_1 = models.IntegerField(default=0)
	score_player_2 = models.IntegerField(default=0)
	# ball position, ball speed, paddle position
	game_data = models.JSONField(default=dict, blank=True)

	class Meta:
		abstract = True
	
	def __str__(self):
		return f"Match started at {self.created_at}"
	
class QuickMatch(BaseMatch):
	def __str__(self):
		return f"Quick Match ({self.created_at})"
	
class ConnectedMatch(BaseMatch):
	player_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='connected_player_1')
	player_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='connected_player_2')

	def __str__(self):
		return f"Connected Match between {self.player_1} and {self.player_2} ({self.created_at})"
	
class Tournament(BaseMatch):
	name = models.CharField(max_length=100)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	participants = models.ManyToManyField(User, related_name='tournaments')
	status = models.CharField(max_length=20, choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('finished', 'Finished')], default='upcoming')

	def __str__(self):
		return self.name