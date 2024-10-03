from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

from .views import CustomTokenObtainPairView, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
