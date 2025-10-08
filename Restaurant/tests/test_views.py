from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# Create user, auth
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Model
from Restaurant.models import Menu

# Serializer
from Restaurant.serializers import MenuSerializer

# Simulate API response
from django.urls import reverse

class TestMenuView(TestCase):
    def setUp(self):
        # Auth setup
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        
        # Authenticated client
        self.authenticated_client = APIClient()
        self.authenticated_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Unauthenticated client
        self.unauthenticated_client = APIClient()

        # Model setup
        Menu.objects.create(Title="IceCream", Price=80, Inventory=100)
        Menu.objects.create(Title="Cake", Price=50, Inventory=50)
        Menu.objects.create(Title="Pie", Price=30, Inventory=30)

    def test_getall_authenticated(self):
        """Test authenticated user can access menu list"""
        response = self.authenticated_client.get(reverse('menu-list'))
        menus = Menu.objects.all()
        serialized_data = MenuSerializer(menus, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized_data, response.data)
    
    def test_getall_unauthenticated(self):
        """Test unauthenticated user cannot access menu list"""
        response = self.unauthenticated_client.get(reverse('menu-list'))
        
        # Now that MenuItemsView has IsAuthenticated permission, should return 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_menu_authenticated(self):
        """Test authenticated user can create menu item"""
        data = {
            'Title': 'New Dish',
            'Price': '25.99',  # Use string for decimal field
            'Inventory': 10
        }
        response = self.authenticated_client.post(reverse('menu-list'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 4)
        
        # Verify the created item
        created_menu = Menu.objects.get(Title='New Dish')
        self.assertEqual(float(created_menu.Price), 25.99)
        self.assertEqual(created_menu.Inventory, 10)
    
    def test_create_menu_unauthenticated(self):
        """Test unauthenticated user cannot create menu item"""
        data = {
            'Title': 'New Dish',
            'Price': 25.99,
            'Inventory': 10
        }
        response = self.unauthenticated_client.post(reverse('menu-list'), data)
        
        # With IsAuthenticated permission, should return 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify no item was created
        self.assertEqual(Menu.objects.count(), 3)
    
    def test_get_single_menu_authenticated(self):
        """Test authenticated user can get single menu item"""
        menu_item = Menu.objects.first()
        response = self.authenticated_client.get(reverse('menu-detail', kwargs={'pk': menu_item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Title'], menu_item.Title)

    def test_get_single_menu_unauthenticated(self):
        """Test unauthenticated user cannot get single menu item"""
        menu_item = Menu.objects.first()
        response = self.unauthenticated_client.get(reverse('menu-detail', kwargs={'pk': menu_item.id}))
        # With IsAuthenticated permission, should return 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_menu_authenticated(self):
        """Test authenticated user can update menu item"""
        menu_item = Menu.objects.first()
        data = {
            'Title': 'Updated IceCream',
            'Price': '90.00',  # Use string for decimal field
            'Inventory': 120
        }
        response = self.authenticated_client.put(
            reverse('menu-detail', kwargs={'pk': menu_item.id}), 
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_menu = Menu.objects.get(id=menu_item.id)
        self.assertEqual(updated_menu.Title, 'Updated IceCream')
        self.assertEqual(float(updated_menu.Price), 90.0)
    
    def test_update_menu_unauthenticated(self):
        """Test unauthenticated user cannot update menu item"""
        menu_item = Menu.objects.first()
        data = {
            'Title': 'Updated IceCream',
            'Price': '90.00',
            'Inventory': 120
        }
        response = self.unauthenticated_client.put(
            reverse('menu-detail', kwargs={'pk': menu_item.id}), 
            data
        )
        # With IsAuthenticated permission, should return 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_menu_authenticated(self):
        """Test authenticated user can delete menu item"""
        menu_item = Menu.objects.first()
        response = self.authenticated_client.delete(
            reverse('menu-detail', kwargs={'pk': menu_item.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 2)
    
    def test_delete_menu_unauthenticated(self):
        """Test unauthenticated user cannot delete menu item"""
        menu_item = Menu.objects.first()
        response = self.unauthenticated_client.delete(
            reverse('menu-detail', kwargs={'pk': menu_item.id})
        )
        # With IsAuthenticated permission, should return 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify item was not deleted
        self.assertEqual(Menu.objects.count(), 3)

    def test_create_menu_missing_fields(self):
        """Test creating menu item with missing fields returns 400"""
        data = {
            'Title': 'No Price'
        }
        response = self.authenticated_client.post(reverse('menu-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_menu_invalid_price(self):
        """Test updating menu item with invalid price returns 400"""
        menu_item = Menu.objects.first()
        data = {
            'Title': 'IceCream',
            'Price': 'not_a_number',
            'Inventory': 100
        }
        response = self.authenticated_client.put(
            reverse('menu-detail', kwargs={'pk': menu_item.id}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_menu_not_found(self):
        """Test getting a non-existent menu item returns 404"""
        response = self.authenticated_client.get(reverse('menu-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)