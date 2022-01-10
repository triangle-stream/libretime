import os

# Make the config module visible to celery
os.environ["CELERY_CONFIG_MODULE"] = "libretime_worker.config"
