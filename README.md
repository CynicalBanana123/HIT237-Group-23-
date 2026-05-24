# HIT237-Group-23-

## Deployment notes

Before deploying, set the following environment variables on your host:

- `DJANGO_SECRET_KEY` — a long random secret key
- `DJANGO_DEBUG` — `True` or `False` (set to `False` in production)
- `ALLOWED_HOSTS` — comma-separated hostnames (e.g. `example.com,www.example.com`)

Install dependencies and collect static files:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

When using a WSGI server like Gunicorn:

```bash
gunicorn housingapp.wsgi:application
```

If deploying to Render or Railway, enable WhiteNoise by ensuring
`whitenoise` is present in `requirements.txt` (already included) and
`whitenoise.middleware.WhiteNoiseMiddleware` is present in
`MIDDLEWARE` (this repo configures it automatically).

Run checks before deploying:

```bash
python manage.py check --deploy
```
