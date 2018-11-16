from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail


@shared_task  # Use this decorator to make this a asyncronous function
def send_email(email, data):
    send_mail('times_project', str(data), 'shivam94cool@gmail.com', ['shivam.singhal212@gmail.com'],fail_silently=False,)
    print('sending email to:{0} and data is {1}'.format(email, data))
