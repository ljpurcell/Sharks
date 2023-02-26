celery_config = dict(
## Broker settings.
BROKER_URL='redis://localhost:6379/0',

# List of modules to import when the Celery worker starts.
IMPORTS = ['app.notifications.new_user_email',]
)