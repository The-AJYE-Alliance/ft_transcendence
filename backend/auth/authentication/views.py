from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Récupère tous les utilisateurs
    serializer_class = UserSerializer  # Utilise le serializer pour convertir les données

