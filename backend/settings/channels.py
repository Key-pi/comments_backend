import os


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(
                os.environ.get("REDIS_HOST"),
                int(os.environ.get("REDIS_PORT", 6379))
            )],
        },
    },
}
