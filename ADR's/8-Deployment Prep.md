# ADR-008: Prepare Django Project for Deployment

## Deployment and Production Configuration Revision:

### Status:
Approved

### Context
The project needs to be suitable for deployment outside of the local development environment.

Development settings such as `DEBUG = True`, hardcoded secret keys, and local-only static file handling are unsafe or unsuitable for production.

A production-ready Django project should use environment variables, static file collection, deployment dependencies, and security checks.

### Alternative Solutions Considered

1. Keep development settings for submission
  - Pros
    - Easier to run locally
    - Less configuration required
  - Cons
    - Unsafe for real deployment
    - Does not show production awareness

2. Add production-ready configuration
  - Pros
    - More secure and realistic
    - Supports deployment platforms
  - Cons
    - Requires environment variables
    - Slightly more complex setup

### Solution Decided Upon:
The project will include production-focused configuration.

This includes:

- environment-based `SECRET_KEY`
- environment-based `DEBUG`
- configurable `ALLOWED_HOSTS`
- static file collection using `STATIC_ROOT`
- Whitenoise for static file serving
- deployment dependencies in `requirements.txt`
- deployment notes in documentation

### Consequences:
The project becomes safer and more realistic for production deployment. It also demonstrates understanding of Django deployment requirements.

However, the project now requires correct environment variables when deployed.

### Code Reference:

```python
# settings.py

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

```python
# settings.py

STATIC_ROOT = BASE_DIR / 'staticfiles'
```

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
```

```bash
python manage.py check --deploy
python manage.py collectstatic
python manage.py migrate
```