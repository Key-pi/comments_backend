import os


EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if not all((EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)):
    print('Something missing to send emails. Using `django.core.mail.backends.console.EmailBackend`')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
