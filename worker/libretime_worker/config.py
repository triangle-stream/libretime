import os

from configobj import ConfigObj
from kombu import Exchange, Queue


def get_broker():
    config = ConfigObj(os.environ["RMQ_CONFIG_FILE"])
    rabbitmq = config["rabbitmq"]
    return (
        rabbitmq["host"],
        rabbitmq["port"],
        rabbitmq["user"],
        rabbitmq["password"],
        rabbitmq["vhost"],
    )


_host, _port, _username, _password, _vhost = get_broker()

# Celery settings
# See https://docs.celeryproject.org/en/stable/userguide/configuration.html

broker_url = f"amqp://{_username}:{_password}@{_host}:{_port}/{_vhost}"

result_backend = "rpc://"
result_persistent = True
result_expires = 900
result_exchange = "celeryresults"  # needed due to php-celery

task_queues = (
    Queue("podcast", exchange=Exchange("podcast"), routing_key="podcast"),
    Queue(exchange=Exchange("celeryresults"), auto_delete=True),
)

event_queue_expires = 900
