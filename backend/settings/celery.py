import os

# broker settings
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'rabbit')
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'rabbit')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST', 'celery')

print('--------------------------------------', RABBITMQ_PASSWORD)
print('--------------------------------------',RABBITMQ_USERNAME )
print('--------------------------------------', RABBITMQ_HOST)
print('--------------------------------------', RABBITMQ_VHOST)
# result settings

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_CELERY_RESULT_DB = os.environ.get("REDIS_CELERY_RESULT_DB", 1)

# todo add result backend to celery settings or remove
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_RESULT_DB}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_RESULT_DB}'

