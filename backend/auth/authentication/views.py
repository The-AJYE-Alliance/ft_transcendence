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
