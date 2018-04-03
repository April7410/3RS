from django.urls import path
from .views import *

app_name = 'reservation'
urlpatterns = [
	path('', buildings, name='buildings'),
	path('<int:building_pk>/', rooms, name='rooms'),
	path('<int:building_pk>/<int:room_pk>/', reserve, name='reserve'),
	path('<int:building_pk>/<int:room_pk>/success/', reserve_success, name='reserve_success'),
]