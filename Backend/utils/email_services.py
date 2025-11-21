# utils/email_services.py
from flask_mail import Message
from database.extensions import mail
from flask import current_app

def send_test_email(user_mail: str, user_name: str):
    """Trigger a test email. Returns True/False or raises."""
    if not user_mail:
        raise ValueError("user_mail required")

    subject = "Welcome to Flask App!"
    body = f"Hi {user_name},\n\nYour registration was successful. Welcome!\n\n- Flask App Team"

    try:
        msg = Message(subject=subject,
                      recipients=[user_mail],
                      body=body)
        # mail must be initialized via mail.init_app(app) in create_app()
        mail.send(msg)
        return True
    except Exception as e:
        # log actual exception in real app (use logging)
        print(f"--- Error sending email: {e} ---")
        # raise or return False, here we choose to raise so caller can decide
        raise
