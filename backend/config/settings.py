"""Django settings; every deploy-specific value comes from environment variables."""

from pathlib import Path

import environ

# Paths and environment reader
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

# Core: secret key has no default so a misconfigured deploy fails fast
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# Applications: Django contrib, Ninja (schema export command, docs assets), project apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "ninja",
    "apps.core",
]

# Request pipeline
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static + SPA files, right after security
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL and WSGI entry points
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Templates: Django admin now, invoice PDF templates in M8
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database: PostgreSQL 17 only; schema relies on pg_trgm and btree_gist
DATABASES = {"default": env.db("DATABASE_URL")}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validators: PRD minimum of 12 characters plus Django defaults
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Language and time zone: owner works in America/New_York
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# Static files: collected for Django admin; WhiteNoise serves them with hashed names
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Built SvelteKit SPA: WhiteNoise serves its files at the site root; the SPA view serves index.html
FRONTEND_BUILD_DIR = Path(env.str("FRONTEND_BUILD_DIR", default=str(BASE_DIR / "frontend_build")))
WHITENOISE_ROOT = FRONTEND_BUILD_DIR if FRONTEND_BUILD_DIR.is_dir() else None

# Long-cache content-hashed files: SvelteKit's _app/immutable and Django's manifest names
WHITENOISE_IMMUTABLE_FILE_TEST = r"^/_app/immutable/|^/static/.+\.[0-9a-f]{12}\.\w+$"

# Email: defaults to Mailpit for local dev; owner's mailbox settings arrive in M8
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=1025)

# HTTPS: Cloud Run terminates TLS and forwards the original scheme
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 0 if DEBUG else 60 * 60 * 24 * 365
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

# Deploy checks silenced on purpose
SILENCED_SYSTEM_CHECKS = [
    "security.W008",  # Cloud Run only accepts HTTPS; no plain-HTTP request reaches Django
    "security.W021",  # HSTS preload would commit all of mjduleba.com, not just this app
]
