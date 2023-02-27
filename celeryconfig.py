
broker_url = 'redis://localhost:6379/0'
include=('app.notifications', 'app.notifications.new_user_email', 'app.notifications.new_user_email.send_async_welcome_email')
