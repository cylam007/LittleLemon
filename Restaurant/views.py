# Rendering
from django.shortcuts import render
# Response
from rest_framework.response import Response
from rest_framework import status
# Serializers
from .serializers import BookingSerializer, MenuSerializer
# Models
from .models import Booking, Menu
# Security
from rest_framework import permissions
# Provide base classes for building views with specific HTTP methods
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

def index(request):
    return render(request, 'index.html', {})

class BookingView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        # Only return bookings for the current user
        return Booking.objects.filter(Name=self.request.user.username)

    def perform_create(self, serializer):
        # Always set Name to current user
        serializer.save(Name=self.request.user.username)

    # Custom delete method for user's own booking
    def delete(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'Booking ID required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=pk, Name=request.user.username)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# GET, POST
class MenuItemsView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

# GET, PUT, DELETE
class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer