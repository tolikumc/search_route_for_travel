from django.urls import path
from .views import *

urlpatterns = [
     path('', search_route, name='search_route'),
     path('find/', find_routes, name='find_routes'),
     path('add_route/', add_route, name='add_route'),
     path('list_routes/', RouteListView.as_view(), name='list_routes'),
     path('route_detail/<int:pk>/', RouteDetailView.as_view(), name='routes_detail'),
     path('route_delete/<int:pk>/', RouteDeleteView.as_view(), name='route_delete'),
]