# Generated by Django 5.1.1 on 2024-10-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_friends_alter_user_avatar_alter_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
