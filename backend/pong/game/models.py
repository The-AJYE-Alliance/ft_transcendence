from django.db import models
from datetime import timedelta

from django.forms import JSONField

from .validators import validate_start_date

class Match(models.Model):
	match_type = models.CharField(blank=False, null=False, choices=['Quick', 'Standard'])
	created_at = models.DateTimeField(auto_now_add=True)
	duration = models.DurationField(blank=True, default=timedelta(minutes=2))
	player_1 = models.CharField(length=30, blank=False, null=False)
	player_2 = models.CharField(length=30, blank=False, null=False)
	score_player_1 = models.IntegerField(default=0)
	score_player_2 = models.IntegerField(default=0)
	# ball position, ball speed, paddle position
	game_data = models.JSONField(default=dict, blank=True)
	winner = models.CharField(null=True)

	def __str__(self):
		return f"{self.match_type} Match started at {self.created_at}"
	
class Tournament(models.Model):
	name = models.CharField(max_length=100, unique=True, blank=False, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	start_date = models.DateTimeField(blank=False, null=False)
	end_date = models.DateTimeField(blank=False, null=False)
	players_required = models.PositiveIntegerField()
	match_duration = models.DurationField(blank=True, default=timedelta(minutes=2))
	status = models.CharField(choices=['pending', 'ongoing', 'finished'], default='pending')
	players = models.JSONField(default=dict, blank=True, null=True)
	current_match = models.ForeignKey(Match, null=True)

	def clean(self):
		super().clean()
		validate_start_date(self.created_at, self.start_date)

	def save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name
	
class Matchmaking(models.Model):
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matchmaking_set')
	players_queued = models.JSONField(defaut=list, blank=True, null=True)
	matchs = JSONField(default=list, blank=True, null=True)
	next_match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)

	# def add_player():
	# def create_match():
	# def set_next_match():

	def __str__(self):
		return f"Matchmaking for {self.tournament.name}"

