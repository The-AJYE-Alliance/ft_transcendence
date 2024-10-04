from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Écriture seulement

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'avatar', 'is_active', 'is_superuser', 'is_staff', 'created_at', 'friends', 'password')
        read_only_fields = ['created_at', 'is_superuser']  # Champ en lecture seule

    def create(self, validated_data):
        # Hachage du mot de passe lors de la création de l'utilisateur
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Hachage du mot de passe si fourni lors de la mise à jour
        password = validated_data.pop('password', None)  # Retire le mot de passe du validated_data
        if password:
            instance.set_password(password)  # Hachage du mot de passe
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
