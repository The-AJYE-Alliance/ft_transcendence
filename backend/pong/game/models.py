from django.db import models
from datetime import timedelta
from auth.authentication.models import User

class Match(models.Model):
	match_type = models.CharField(blank=False, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	duration = models.DurationField(default=timedelta(minutes=2))
	player_1 = models.CharField(length=30, blank=False, null=False)
	player_2 = models.CharField(length=30, blank=False, null=False)
	score_player_1 = models.IntegerField(default=0)
	score_player_2 = models.IntegerField(default=0)
	# ball position, ball speed, paddle position
	game_data = models.JSONField(default=dict, blank=True)
	winner = models.CharField(null=True)

	def __str__(self):
		return f"Match started at {self.created_at}"
	
class Tournament(models.Model):
	name = models.CharField(max_length=100)
	players = models.ManyToManyField(User, related_name='tournaments')
	current_match = models.ForeignKey(Match, null=True)

	def __str__(self):
		return self.name
	
class Matchmaking(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    next_match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    announced_match = models.BooleanField(default=False)

    def __str__(self):
        return f"Matchmaking for {self.tournament.name} (ID: {self.id})"

class MatchOrder(models.Model):
    matchmaking = models.ForeignKey(Matchmaking, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Match {self.match.id} in Matchmaking {self.matchmaking.id} at position {self.order}"
