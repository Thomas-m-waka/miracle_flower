import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url


# ============================================================
# BASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get("MIRACLE_FLOWERS_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "MIRACLE_FLOWERS_SECRET_KEY is not set."
    )

DEBUG = (
    os.environ.get(
        "MIRACLE_FLOWERS_DEBUG",
        "False",
    ).lower()
    == "true"
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "MIRACLE_FLOWERS_ALLOWED_HOSTS",
        "localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]


# ============================================================
# SETTINGS DEBUG
# TEMPORARY - REMOVE AFTER THE PROBLEM IS FOUND
# ============================================================

print("====================================================")
print("       MIRACLE FLOWERS SETTINGS DEBUG")
print("====================================================")

print("DEBUG:", DEBUG)

print(
    "SECRET_KEY exists:",
    bool(os.environ.get("MIRACLE_FLOWERS_SECRET_KEY"))
)

print(
    "DATABASE_URL exists:",
    bool(os.environ.get("DATABASE_URL"))
)

print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

print(
    "CLOUD_NAME exists:",
    bool(os.environ.get("CLOUD_NAME"))
)

print(
    "API_KEY exists:",
    bool(os.environ.get("API_KEY"))
)

print(
    "API_SECRET exists:",
    bool(os.environ.get("API_SECRET"))
)

print("====================================================")


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Local apps
    "core",
    "flowers",
    "events",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "miracle_flowers.urls"

WSGI_APPLICATION = "miracle_flowers.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

print("====================================================")
print("              DATABASE DEBUG")
print("====================================================")

print(
    "DATABASE_URL exists:",
    bool(DATABASE_URL)
)

if DATABASE_URL:
    try:
        DATABASES = {
            "default": dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                ssl_require=not DEBUG,
            )
        }

        print("DATABASE CONFIG: SUCCESS")
        print(
            "DATABASE ENGINE:",
            DATABASES["default"].get("ENGINE")
        )
        print(
            "DATABASE NAME:",
            DATABASES["default"].get("NAME")
        )

    except Exception as e:
        print(
            "DATABASE CONFIG ERROR:",
            repr(e)
        )
        raise

else:
    print(
        "DATABASE CONFIG ERROR: DATABASE_URL is missing"
    )

    raise RuntimeError(
        "DATABASE_URL is not set."
    )

print("====================================================")


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        )
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# CLOUDINARY
# ============================================================

print("====================================================")
print("             CLOUDINARY DEBUG")
print("====================================================")

print(
    "CLOUD_NAME exists:",
    bool(os.environ.get("CLOUD_NAME"))
)

print(
    "API_KEY exists:",
    bool(os.environ.get("API_KEY"))
)

print(
    "API_SECRET exists:",
    bool(os.environ.get("API_SECRET"))
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUD_NAME"),
    "API_KEY": os.environ.get("API_KEY"),
    "API_SECRET": os.environ.get("API_SECRET"),
}

print("CLOUDINARY_STORAGE configured")
print("====================================================")


# ============================================================
# DJANGO STORAGE
# ============================================================

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage."
            "MediaCloudinaryStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


print("====================================================")
print("              STORAGE DEBUG")
print("====================================================")

print(
    "DEFAULT STORAGE:",
    STORAGES["default"]["BACKEND"]
)

print(
    "STATIC STORAGE:",
    STORAGES["staticfiles"]["BACKEND"]
)

print("====================================================")


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# LOGIN
# ============================================================

LOGIN_URL = "/admin/login/"


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    # HTTPS / SSL
    SECURE_SSL_REDIRECT = True

    # Secure cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Browser security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # Referrer policy
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    # Render proxy / HTTPS detection
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )


# ============================================================
# FINAL SETTINGS MESSAGE
# ============================================================

print("====================================================")
print("       MIRACLE FLOWERS SETTINGS LOADED")
print("====================================================")