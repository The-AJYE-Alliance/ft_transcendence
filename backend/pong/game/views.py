
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def quick_match_view(request):
	player_1 = request.data.get('player_1')
	player_2 = request.data.get('player_2')
	avatar_1 = request.data.get('avatar_1')
	avatar_2 = request.data.get('avatar_2')
	duration = request.data.get('duration')

	avatar_1 = avatar_1 if avatar_1 else './img_urls/default_avatar_1'
	avatar_2 = avatar_2 if avatar_2 else './img_urls/default_avatar_2'
	duration = duration if duration else 2

	response_data = {
        'player_1': player_1,
        'avatar_1': avatar_1,
        'player_2': player_2,
        'avatar_2': avatar_2,
        'duration': duration,
    }
	return JsonResponse(response_data, status=status.HTTP_200_OK)