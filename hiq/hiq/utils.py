from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from random import randint

def send_verification_email(to, code):
    subject, from_email, to = 'Email Verification', 'no-reply@hiqconnections.com', to
    html_content = render_to_string('emails/email-verification.html', {'verification_code': code})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def verification_code_generator():
    return randint(10000, 99999)
