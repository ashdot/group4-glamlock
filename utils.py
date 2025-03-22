from flask_mail import Message
from extensions import mail
from flask import url_for

def send_verification_email(user):
    token = user.get_reset_token()
    msg = Message('Verify Your Email', sender='noreply@glamlockja.com', recipients=[user.email])
    msg.body = f'''To verify your email, visit:
{url_for('auth.verify_email', token=token, _external=True)}

If you didn't create this account, ignore this email.
'''
    mail.send(msg)