from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from .models import User
from celery import Celery
from celery import shared_task
from .kafka_utils import send_message_to_kafka, consume_messages_from_kafka
from backend.celery import app
from base.models import Product

@app.task
def user_created(useremail, username):
    subject = 'Witaj w rodzinie Locker'
    message = 'Witaj, {}!\n\nDziekujemy za zalozenie konta na platformie Locker.'.format(username)
    mail_sent = send_mail(subject,message,'locker.marketplace@gmail.com',[useremail])
    return mail_sent

@app.task
def product_updated(product_id):
    product = Product.objects.get(id = product_id)
    user = product.user
    product_name = product.name
    email = user.email
    subject = 'Locker edycja produktu'
    message = 'Twoj przedmiot {}, zostal zaktualizowany.'.format(product_name)
    mail_sent = send_mail(subject,message,'locker.marketplace@gmail.com',[email])
    return mail_sent

#@app.task
#def send_task_to_kafka(message):
#    send_message_to_kafka('your_topic', message)

#def your_view(request):
#    consume_messages_from_kafka('your_topic')
#    # Perform other view-related actions