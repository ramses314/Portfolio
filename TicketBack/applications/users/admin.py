import random

from django.contrib import admin
from django.contrib.auth.hashers import make_password

from applications.users.models import CustomUser
from applications.core.mail import HTMLMessageContext, EmailFactory


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email'
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name'
    ]

    def get_fields(self, request, obj=None):
        if not obj:
            fields = ['email']
        else:
            fields = ['email', 'password', 'is_active']
        return fields

    def get_exclude(self, request, obj=None):
        if obj:
            exclude = []
        else:
            exclude = ['password']
        return exclude

    def save_model(self, request, obj, form, change):
        password = obj.generate_password()

        if not obj.pk:
            obj.username = random.randint(10000000000, 99999999999)
        elif obj.password != CustomUser.objects.get(pk=obj.pk).password:
            password = obj.password
        else:
            return obj.save()

        hash_password = make_password(password)
        obj.password = hash_password
        obj.save()

        EmailFactory(obj.email).send_html_email(
            subject='Gracias por registrarse' if not obj.pk else 'Su contraseña ha sido cambiada',
            template_path='sales/registration.html',
            context=HTMLMessageContext(
                email=obj.email,
                password=password
            ).return_dict()
        )
