from django.core.mail import EmailMessage
from django.conf import settings

class EmailHandler:
    def send_email_to_user(self, data):
        print('Sending email', data)
        email = EmailMessage(subject=data['subject'], body=data['body'], from_email=settings.EMAIL_HOST_USER, to=data['email_list'])
        email.content_subtype = 'html'
        email.send()