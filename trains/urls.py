from django.urls import path
from .views import *

urlpatterns = [
    path('', train_list_view, name='train_list'),
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='train_detail'),
    path('add/', TrainCreateView.as_view(), name='add_train'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete_train'),
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update_train'),
]
