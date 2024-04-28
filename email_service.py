from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)
