from django.urls import path
from .views import *

urlpatterns = [
     path('', city_list_view, name='city_list'),
     path('detail/<int:pk>/', CityDetailView.as_view(), name='city_detail'),
     path('add/', CityCreateView.as_view(), name='add_city'),
     path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete_city'),
     path('update/<int:pk>/', CityUpdateView.as_view(), name='update_city'),
]