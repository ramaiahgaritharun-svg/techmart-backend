# GenMart Backend

## Overview

This is the Django REST Framework backend for **GenMart**, a full-stack e-commerce application. It provides secure JWT authentication and REST APIs for product browsing, cart management, wishlist, checkout, and order processing.

---

## Features

- JWT Authentication
- User Registration
- Login
- Forgot Password
- Product APIs
- Shopping Cart APIs
- Wishlist APIs
- Checkout APIs
- Order Management
- Email Confirmation
- Django Admin Panel

---

## Tech Stack

- Python 
- Django
- Django REST Framework
- Simple JWT
- SQLite
- SMTP (Gmail)

---

## Installation

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

``
python manage.py migrate
```

Start the server:

```
python manage.py runserver
```

---

## API Endpoints

- `/register/`
- `/token/`
- `/token/refresh/`
- `/products/`
- `/cart/`
- `/wishlist/`
- `/orders/`

---

## Author

G Sumanth