from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

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
    path('login/42/', UserViewSet.as_view({'post': 'login_with_42'}), name='login_with_42'),
    path('auth/42/callback/', handle_42_callback, name='handle_42_callback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)