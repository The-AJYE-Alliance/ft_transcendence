from django.urls import path
from . import views

urlpatterns = [
	path('quick-match/', views.QuickMatch.as_view(), name='quick_match'),
	path('connected-match/', views.connectedmatch.as_view(), name='connected_match')
	path('tournament/', views.tournament.as_view(), name='tournament')
]