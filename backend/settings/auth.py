# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
import os
from datetime import timedelta

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'user.User'

SIMPJWT_ACCESS_TOKEN_LIFETIME = timedelta(hours=1)

SIMPJWT_REFRESH_TOKEN_LIFETIME = timedelta(days=30)

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
}
