from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.BookingView.as_view(), name='booking-list'),
    path('booking/<int:pk>/', views.BookingView.as_view(), name='booking-detail'),
    path('menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
]
