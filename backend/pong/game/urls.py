from django.urls import path
from . import views

urlpatterns = [
	path('quick-match/', views.quick_match_view(), name='quick_match'),
	# path('standard-match/', views.connectedmatch.as_view(), name='standard_match'),
	# path('tournament/', views.tournament.as_view(), name='tournament'),
]