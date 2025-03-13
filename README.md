# QuickCart - E-commerce Platform

## Overview
QuickCart is a full-fledged e-commerce web application built using Django and Tailwind CSS. It provides a user-friendly shopping experience with features like product management, cart functionality, order tracking, authentication, and more. The application is structured with rendered templates instead of an API-based implementation, ensuring a seamless user experience.

## Features
### User Management
- User registration and login
- Profile management with avatar upload
- Password reset and change password functionality
- Two-factor authentication (2FA) enablement

### Product Management
- Browse and search for products
- View product details
- Add, edit, and delete products (admin only)
- Product reviews and ratings
- Wishlist functionality

### Shopping Cart & Checkout
- Add and remove items from cart
- Update cart item quantities
- View cart details with total price
- Checkout process with order summary
- Address management for shipping and billing

### Order Management
- Place orders and track order status
- View order history
- Cancel orders if eligible
- Order confirmation page
- Payment processing simulation

### Additional Features
- Dark mode support
- Responsive UI built with Tailwind CSS
- Optimized database queries for performance
- Admin dashboard for order and product management

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Django 4+
- SQLite (default) or any supported database
- Tailwind CSS (configured with Django reload)

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/JunaidSumsaal/quickcart.git
   cd quickcart
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

7. Open the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure
```
quickcart/
├── accounts/         # User authentication and profile management
├── cart/             # Shopping cart functionality
├── orders/           # Order management and tracking
├── products/         # Product catalog and reviews
├── templates/        # HTML templates organized by app
├── static/           # Static files including Tailwind CSS
├── core/             # Settings and configuration
├── manage.py         # Django management script
└── README.md         # Project documentation
```

## Deployment
This project is configured for deployment on Render. To deploy:
- Ensure environment variables are set for database and secret key.
- Use a production-ready WSGI server like Gunicorn.
- Set up Nginx as a reverse proxy.

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Submit a pull request.

## License
This project is licensed under the MIT License.


