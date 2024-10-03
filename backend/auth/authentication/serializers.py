from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Écriture seulement

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'avatar', 'is_active', 'is_admin', 'created_at', 'friends', 'password']
        read_only_fields = ['created_at', 'is_admin']  # Champ en lecture seule

    def create(self, validated_data):
        # Hachage du mot de passe lors de la création de l'utilisateur
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Utilise set_password pour hacher le mot de passe
        user.save()
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
