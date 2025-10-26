# E-commerce API

A RESTful e-commerce API built with Django REST Framework and JWT authentication.

## Features

- 🔐 JWT Authentication
- 🛍️ Product management
- 📝 Order system
- ⭐ Product reviews
- 🔍 Search & filters

## Quick Start

1. Clone & install:
   ```bash
   git clone [your-repo-url]
   cd stage_2_backend_project
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. Run:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/auth/token/` - Get JWT token
- `GET /api/products/` - List products
- `POST /api/orders/` - Create order
- `GET /api/products/1/reviews/` - Get product reviews

## Environment

Create `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

## License

MIT
