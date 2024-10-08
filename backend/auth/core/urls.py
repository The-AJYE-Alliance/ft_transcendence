from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('ht/', include('health_check.urls')),
]
