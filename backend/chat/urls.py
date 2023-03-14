from django.urls import path, include
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<str:room_id>', room, name='room'),
    path('<str:room_id>/settings', room_settings, name='room_settings'),
]