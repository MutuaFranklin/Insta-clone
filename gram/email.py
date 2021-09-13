from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(user,receiver):
    # Creating message subject and sender
    subject = 'Welcome to the Insta-clone by Frank'
    sender = 'frankmailautomation@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/welcome_email.txt',{"name": user})
    html_content = render_to_string('email/welcome_email.html',{"name": user})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()