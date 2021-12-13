from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


def registrationMail(receiver):
    subject = 'Thank you for registering on ChildTech'
    message = Mail(
        from_email='manzi.elyse27@gmail.com',
        to_emails=receiver,
        subject=subject,
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return print(response.headers)
    except Exception as e:
        print(e.message)


def enrollMail(receiver, course):
    subject = 'Thank you for enrolling in ' + course
    message = Mail(
        from_email='manzi.elyse27@gmail.com',
        to_emails=receiver,
        subject=subject,
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return print(response.headers)
    except Exception as e:
        print(e.message)


def appointmentMail(receiver, course, date):
    subject = 'Thank you for enrolling in ' + course
    message = Mail(
        from_email='manzi.elyse27@gmail.com',
        to_emails=receiver,
        subject=subject,
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return print(response.headers)
    except Exception as e:
        print(e.message)


def contactMail(name, phone, subject, msg):
    message = Mail(
        from_email='manzi.elyse27@gmail.com',
        to_emails='igiginixy10@gmail.com',
        subject=name + ' ' + subject,
        html_content=msg + 'contact me on ' + phone
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return print(response.headers)
    except Exception as e:
        print(e.message)
