from django.shortcuts import render
from .serializers import MenuSerializer
from .models import Menu

from rest_framework import permissions

# Provide a higher-level abstraction for building REST APIs
# Combin logic for multiple HTTP methods (GET, POST, PUT, DELETE) into a single class
from rest_framework.viewsets import ModelViewSet

# Provide base classes for building views with specific HTTP methods
# Focus on individual HTTP methods
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

def index(request):
    return render(request, 'index.html', {})

class BookingViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

# GET, POST
class MenuItemsView(ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

# GET, PUT, DELETE
class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer