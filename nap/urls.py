# Django Import:
from django.urls import path

# Application Import:
from .views import automation

app_name = 'automation'

urlpatterns = [
    path('automation/<int:pk>', automation, name='automation'),
]
