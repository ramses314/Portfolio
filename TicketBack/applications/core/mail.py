from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from applications.main.models import Preference
from applications.sales.models import LetterImage
from applications.users.models import CustomUser


class HTMLMessageContext:
    def __init__(self, email, password=None, *args, **kwargs):
        self.email = email
        self.password = password
        self.images = LetterImage.objects.first()
        self.front_url = Preference.objects.first().front_url if Preference.objects.first() else None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def return_dict(self):
        user = CustomUser.objects.filter(email=self.email).first()
        context_dict = {
            "email": self.email,
            "password": self.password,
            "images": self.images,
            "front_url": self.front_url,
            "user": user
        }

        for key, value in vars(self).items():
            if key not in context_dict:
                context_dict[key] = value

        return context_dict


class EmailFactory:
    def __init__(self, email):
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.email = email

    def __send(self, subject, message=None, html_message=None):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[self.email],
                html_message=html_message,
            )
        except:
            pass

    def send_html_email(self, subject, template_path, context: HTMLMessageContext):
        html_message = render_to_string(template_path, context)
        self.__send(subject, html_message=html_message)

    def send_message_email(self, subject, message):
        self.__send(subject, message=message)
