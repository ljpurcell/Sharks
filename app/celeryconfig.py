## Broker settings.
broker_url='redis://localhost:6379/0'

# List of modules to import when the Celery worker starts.
imports = ['app.notifications.new_user_email',]