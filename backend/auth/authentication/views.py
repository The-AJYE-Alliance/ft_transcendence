from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Si l'utilisateur est un admin/staff, il a accès à toutes les actions
        if request.user and request.user.is_staff:
            return True
        # Si ce n'est pas un admin/staff, il n'a que des droits de lecture (GET, HEAD, OPTIONS)
        return request.method in permissions.SAFE_METHODS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Récupère tous les utilisateurs
    serializer_class = UserSerializer  # Utilise le serializer pour convertir les données
    permission_classes = [IsAccountAdminOrReadOnly]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='register')
    def register(self, request):
        data = request.data
        is_staff = data.get('is_staff', False)
        if isinstance(is_staff, str):
            is_staff = is_staff.lower() == 'true'
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            nickname=data['nickname'],
            is_staff=is_staff
        )
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    # @action(detail=True, methods=['put', 'patch'], permission_classes=[IsAuthenticated], url_path='update')
    # def update_user(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = UserSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer
# 	authentication_classes = [JWTAuthentication]
    
# 	def get_permissions(self):
# 		if self.action == 'create':
# 			permission_classes = [AllowAny]
# 		elif self.action in ['update', 'destroy', 'retrieve']:
# 			permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
# 		else:
# 			permission_classes = [IsAdminUser]
# 		return [permission() for permission in permission_classes]


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def send_mymail(request):
# 	from_mail = "ponggame@mail.com"
# 	user_email = request.data.get('email')
# 	# verification_token = get_random_string(length=32)
# 	verication_token = "true email"

# 	try:
# 		verification_link = f"http://localhost:8000/api/verify-email/?token={verification_token}"
# 		send_mail(
# 			'Pong game email checking',
# 			f'Click the link to activate your account : {verification_link}',
# 			from_mail,
# 			[user_email],
# 			fail_silently=False,
#         )
# 		return Response({"message": "Send verification mail successfully !"}, status=status.HTTP_200_OK)
# 	except Exception as e:
# 		return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def mail_verified(request):
# 	token = request.data.get('token')
# 	if token and token == "true email"