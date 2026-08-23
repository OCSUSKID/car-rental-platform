# DriveEasy — Django Car Rental Demo

A simple, functional car rental site built with Django (server-rendered templates, no frontend framework).

## Features
- Browse cars with search/filter by make, model, category, and location
- Car detail pages
- User signup/login/logout (Django's built-in auth)
- Logged-in users can book a car for a date range; total cost is auto-calculated
- "My Bookings" page — view and cancel pending bookings
- Django admin for managing cars and bookings

## Project structure
```
core/        # project settings, root urls
cars/        # Car model, listing/detail views
bookings/    # Booking model, create/cancel/list views
accounts/    # signup view, wraps Django's auth views for login/logout
templates/   # base.html (shared layout/styling)
```

## Setup
```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/ — admin panel at /admin/.

## Deploying to Render
This project is already production-ready for Render:
- `requirements.txt` includes gunicorn, whitenoise, dj-database-url, psycopg2-binary
- `settings.py` reads `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, host, CSRF, HTTPS, and email settings from environment variables (falls back to local SQLite and a development key only when `DEBUG` is enabled)
- `Procfile` is set to `web: gunicorn core.wsgi:application`

Steps:
1. Push this project to a GitHub repo.
2. On Render: New + → PostgreSQL → create a free instance, copy its **Internal Database URL**.
3. On Render: New + → Web Service → connect the repo.
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start command: `gunicorn core.wsgi:application`
   - Environment variables: `DATABASE_URL` (from step 2), `SECRET_KEY` (any long random string), `DEBUG` = `False`, and `ALLOWED_HOSTS` if using a custom domain
4. Deploy. Once live, create an admin user via Render's Shell tab: `python manage.py createsuperuser`

Alternatively, use the included `render.yaml` blueprint. Copy `.env.example` to `.env` for local environment-based configuration; never commit the `.env` file.

## Notes / where to take this next
- Add real payment integration (e.g. Paystack/Stripe) at booking confirmation
- Add a REST API layer (DRF) if you want a separate frontend (React, mobile app, etc.)
