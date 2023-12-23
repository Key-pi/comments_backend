REST_FRAMEWORK: dict = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}



# swagger docs
SPECTACULAR_SETTINGS: dict = {
    'TITLE': 'Comments api',
    'VERSION': '1.0.0',
    'COMPONENT_SPLIT_REQUEST': True,
    'DESCRIPTION': 'Test description',
    # OTHER SETTINGS
}
