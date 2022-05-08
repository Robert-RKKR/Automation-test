# Django Import:
from django.urls import path

# Application Import:
from autocore.consumers import CollectConsumer

ws_urlpatterns = [
    path('ws/collect/', CollectConsumer.as_asgi()),
]