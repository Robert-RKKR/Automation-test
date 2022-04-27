# Django Import:]
from django.urls import path, include
from django.contrib import admin

# Admin URL pattern:
urlpatterns = [
    # Django admin URLs patterns:
    path('admin/', admin.site.urls),

    # Application URLs patterns:
    path('nap/', include('nap.urls')),
]
