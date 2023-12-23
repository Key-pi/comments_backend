import os

from datetime import timedelta

from celery import Celery
from kombu import Exchange, Queue  # noqa: F401


class BeatScheduleConfig:
    beat_schedule = {
    #     'task_name': {
    #         'task': 'path to task',
    #         'schedule': timedelta(days=1),
    #     },
    }
    debug_beat_schedule = {
        #     'task_name': {
        #         'task': 'path to task',
        #         'schedule': timedelta(days=10),
        #     },
    }


class QueuesConfig:
    HIGH_PRIORITY_QUEUE = 'high_priority'
    MEDIUM_PRIORITY_QUEUE = 'medium_priority'
    LOW_PRIORITY_QUEUE = 'low_priority'

    task_queues = [
        Queue(
            name=HIGH_PRIORITY_QUEUE,
            exchange=Exchange(HIGH_PRIORITY_QUEUE),
            routing_key=HIGH_PRIORITY_QUEUE,
            queue_arguments={'x-max-priority': 10}
        ),
        Queue(
            name=MEDIUM_PRIORITY_QUEUE,
            exchange=Exchange(MEDIUM_PRIORITY_QUEUE),
            routing_key=MEDIUM_PRIORITY_QUEUE,
            queue_arguments={'x-max-priority': 10}
        ),
        Queue(
            name=LOW_PRIORITY_QUEUE,
            exchange=Exchange(LOW_PRIORITY_QUEUE),
            routing_key=LOW_PRIORITY_QUEUE,
            queue_arguments={'x-max-priority': 10}
        )
    ]



class ConfigureCelery:
    celery_app = None

    @classmethod
    def create_celery_app(cls):
        # base configure celery_app
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

        from django.conf import settings

        _celery_app = Celery('celery_app', broker_url=settings.CELERY_BROKER_URL)
        cls.celery_app = _celery_app
        print(settings.CELERY_BROKER_URL)

        cls.celery_app.autodiscover_tasks()

        # configure broker options
        cls.celery_app.conf.task_queues = QueuesConfig.task_queues
        cls.celery_app.conf.task_default_queue = QueuesConfig.MEDIUM_PRIORITY_QUEUE
        cls.celery_app.conf.task_default_exchange = QueuesConfig.MEDIUM_PRIORITY_QUEUE
        cls.celery_app.conf.task_default_routing_key = QueuesConfig.MEDIUM_PRIORITY_QUEUE

        # configure schedule
        if settings.DEBUG:
            cls.celery_app.conf.beat_schedule = BeatScheduleConfig.debug_beat_schedule
        else:
            cls.celery_app.conf.beat_schedule = BeatScheduleConfig.beat_schedule

        return cls.celery_app


celery_app = ConfigureCelery.create_celery_app()
