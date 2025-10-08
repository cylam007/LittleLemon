# Put at app-level, tests folder
# Create an __init__.py file
# Import from absolute path the models

from django.test import TestCase
from Restaurant.models import Menu, Booking 


class TestMenuItem(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(Title="IceCream", Price=80, Inventory=100)
        self.assertEqual(str(item), "IceCream: $80")

    def test_create_multiple_items(self):
        Menu.objects.create(Title="Cake", Price=50, Inventory=50)
        Menu.objects.create(Title="Pie", Price=30, Inventory=30)
        self.assertEqual(Menu.objects.count(), 2)

    def test_inventory_update(self):
        item = Menu.objects.create(Title="Salad", Price=10, Inventory=5)
        item.Inventory = 10
        item.save()
        self.assertEqual(Menu.objects.get(Title="Salad").Inventory, 10)

class TestBooking(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(Name="testuser", No_of_guests=2, BookingDate="2025-10-10")
        self.assertEqual(booking.Name, "testuser")
        self.assertEqual(booking.No_of_guests, 2)
        self.assertEqual(str(booking.BookingDate), "2025-10-10")

    def test_multiple_bookings(self):
        Booking.objects.create(Name="user1", No_of_guests=1, BookingDate="2025-11-01")
        Booking.objects.create(Name="user2", No_of_guests=3, BookingDate="2025-12-25")
        self.assertEqual(Booking.objects.count(), 2)