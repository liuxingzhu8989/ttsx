from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')

@app.task
def send_email_to_verify(email, username, token):
    subject='ttsx'
    message=''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<h1>%s</h1><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1/user/active/%s</a>'%(username,token,token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
