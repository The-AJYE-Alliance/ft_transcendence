from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, LogoutView, CookieTokenRefreshView, CookieTokenObtainPairView, send_mymail

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('users/<int:pk>/update/', UserViewSet.as_view({'put': 'update_user', 'patch': 'update_user'}), name='user-update'),
    path('verify-email/', send_mymail, name='send_mymail'),
	# path('email-verified/', views.mail_verified),
]