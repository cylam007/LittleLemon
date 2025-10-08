
# Little Lemon API Project

## Overview
This Django project provides RESTful APIs for menu management and table booking for the Little Lemon restaurant. It includes user authentication, browsable API, and unit tests.

## Repository
GitHub: https://github.com/cylam007/LittleLemon.git

## Setup Instructions
1. Clone the repository
2. Install dependencies:
	 ```bash
	 pipenv install
	 pipenv shell
	 ```
3. Run migrations:
	 ```bash
	 python manage.py migrate
	 ```
4. Create a superuser (optional):
	 ```bash
	 python manage.py createsuperuser
	 ```
5. Start the server:
	 ```bash
	 python manage.py runserver
	 ```

## Test User Credentials
- **Username:** testuser
- **Password:** abcd!!8888
- **Token:** 301ba194ca753e2659fe392932afba24849bf100


## User Registration
Register a new user by POSTing to:
```
POST http://127.0.0.1:8000/auth/users/
{
	"username": "newuser",
	"password": "newpassword123",
	"email": "newuser@example.com"
}
```

## Authentication
Obtain a token by POSTing to:
```
POST http://127.0.0.1:8000/api-token-auth/
{
	"username": "testuser",
	"password": "abcd!!8888"
}
```
Use the token in the `Authorization` header:
```
Authorization: Token 301ba194ca753e2659fe392932afba24849bf100
```

## API Endpoints & Use Cases


### Menu Endpoints

#### List All Menu Items
**GET http://127.0.0.1:8000/restaurant/menu/**
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100
**Response:**
```
[
	{"Title": "IceCream", "Price": "80.00", "Inventory": 100},
	...
]
```


#### Create a Menu Item
**POST http://127.0.0.1:8000/restaurant/menu/**
**Payload Examples:**
```
{
	"Title": "Pizza",
	"Price": "15.99",
	"Inventory": 20
}

{
	"Title": "Greek Salad",
	"Price": "12.50",
	"Inventory": 50
}

{
	"Title": "Lemon Dessert",
	"Price": "8.00",
	"Inventory": 30
}
```
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100

#### Retrieve/Update/Delete a Menu Item
**GET/PUT/DELETE http://127.0.0.1:8000/restaurant/menu/<int:pk>/**
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100

### Booking Endpoints

#### List Current User's Bookings
**GET http://127.0.0.1:8000/restaurant/booking/**
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100
**Response:**
```
[
	{"Name": "testuser", "No_of_guests": 2, "BookingDate": "2025-10-10"},
	...
]
```


#### Create a Booking
**POST http://127.0.0.1:8000/booking/**
**Payload Examples:**
```
{
	"No_of_guests": 2,
	"BookingDate": "2025-10-10"
}

{
	"No_of_guests": 4,
	"BookingDate": "2025-12-25"
}

{
	"No_of_guests": 1,
	"BookingDate": "2025-11-01"
}
```
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100

#### Delete a Booking
**DELETE http://127.0.0.1:8000/booking/?pk=<booking_id>**
**Headers:**
	- Authorization: Token 301ba194ca753e2659fe392932afba24849bf100

## Unit Testing
Run all tests:
```
python manage.py test Restaurant
```

## Static Content
Django serves static HTML and images (e.g., Little Lemon logo) at `/restaurant/`.

## API Testing with Insomnia/Postman
- Import endpoints and use the test user credentials above.
- Set `Authorization: Token <token>` in headers for all protected endpoints.

## Database
Supports both SQLite and MySQL (see `settings.py`).