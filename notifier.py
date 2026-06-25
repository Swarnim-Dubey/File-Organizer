# this file ( or the function in this file has only one task to do that is to give a notfification on the desktop )

from plyer import notification

def send_notification(filename, destination):
    try:
        notification.notify(
            title="File Organizer",
            message=f"Moved {filename} to {destination}",
            app_name="File Organization",
            timeout=5
        )
    except Exception:
        pass