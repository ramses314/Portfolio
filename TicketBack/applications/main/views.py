from django.conf import settings
from django.shortcuts import render
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
from validate_email import validate_email

from django.middleware.csrf import get_token
from django.http import JsonResponse


class IndexView(generic.TemplateView):
    template_name = 'main/index.html'


def get_csrf_token(request):
    if request.method == 'POST':
        csrf_token = get_token(request)
        return JsonResponse({'csrf_token': csrf_token})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def test(request):
    return render(request, 'main/test.html')


def admin_load_excel(request):
    return render(request, 'sales/load_excel.html', {'settings': settings})


def test_smtp_check(request):

    context = {
        'smtp': settings.EMAIL_HOST,
        'email': settings.DEFAULT_FROM_EMAIL,
        'email2': settings.EMAIL_HOST_USER
    }
    return render(request, 'main/smtp_test.html', context=context)


class TestSMTPView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', '')

        valid_full = validate_email(email, check_mx=True, verify=True)
        valid_only_mx = validate_email(email, check_mx=True)
        valid_verify = validate_email(email, verify=True)

        response = {
            'valid_full': valid_full,
            'valid_only_mx': valid_only_mx,
            'valid_only_verify': valid_verify,
        }

        return Response({'status': response})
