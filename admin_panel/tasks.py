import asyncio
import time

from celery import shared_task, current_task
from celery.app import task
from django.core.mail import EmailMultiAlternatives

from Diploma.celery import app


@app.task(bind=True)
def send_email(self, html_content="<p>This is an <strong>important</strong> message.</p>",
               to=['dhushchyn@gmail.com',]):
    subject, from_email, = "hello", "danilservices@outlook.com"
    text_content = "This is an important message."
    for i, v in enumerate(to):
        html_content = html_content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [v])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        current_task.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': len(to)})

