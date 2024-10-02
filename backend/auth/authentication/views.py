from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET', 'POST'])
def users_list(request):

	if request.method == 'GET':
		users = User.objects.all() #get all objects
		serializer = UserSerializer(users, many=True) #serialize them
		return JsonResponse(serializer.data, safe=False) #return json

	if request.method == 'POST':
		serializer = UserSerializer(data=request.data) #deserialize : on convertit de json à python
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

