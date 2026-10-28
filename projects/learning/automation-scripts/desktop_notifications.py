#Automated Desktop Notifications

# Install first: pip install plyer
from plyer import notification

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

send_notification("Reminder", "Time to take a break!")