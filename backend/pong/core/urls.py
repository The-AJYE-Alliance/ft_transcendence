from django.urls import include, path

urlpatterns = [
    path('', include('game.urls')),
    path('ht/', include('health_check.urls')),
]
