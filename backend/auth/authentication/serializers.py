from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True) #écriture seulement

	class Meta:
		model = User
		fields = ['id', 'username', 'nickname', 'email', 'avatar', 'is_active', 'is_admin', 'created_at', 'friends', 'password']