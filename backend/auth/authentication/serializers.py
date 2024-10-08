from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'avatar', 'is_active', 'is_superuser', 'is_staff', 'friends', 'password')
        read_only_fields = ['is_superuser']
        extra_kwargs = {
            'id': {'read_only': True},
			'friends': {'read_only': True},
			'is_staff': {'read_only': True},
			'is_active': {'read_only': True},
			'date_joined': {'read_only': True},
            'password': {'write_only': True}
            }

    # save() par defaut ne hash pas le MDP user, donc redefinition ici.
    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(user.password)
        user.save()
        return user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
