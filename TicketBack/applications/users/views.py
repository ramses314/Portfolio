import os

import boto3
import google_auth_oauthlib
import xlsxwriter

from applications.sales.models import PaymentTokenService
from django.conf import settings
from django.forms import model_to_dict
from google_auth_oauthlib import flow
from googleapiclient.discovery import build
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.main.models import Preference
from applications.sales.models import Order
from applications.users.mixins import ApiErrorsMixin, PublicApiMixin
from applications.users.serializers import GoogleSerializer, UserProfileSerializer
from applications.users.services import (clean_creds_json, jwt_login, load_creds_json,
                       user_check_auth, user_get_or_create)
from applications.users.utils import user_get_me


class GoogleUserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        given_name = serializers.CharField(required=False)
        family_name = serializers.CharField(required=False)
        picture = serializers.CharField(required=False)

    def post(self, request, *args, **kwargs):
        serializer = GoogleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redirect = 'http://localhost:3000/login/' if str(request.GET.get('dev')).lower() == 'true' \
            else Preference.objects.first().google_redirect_url
        load_creds_json(redirect)
        code = serializer.validated_data.get('code')
        google_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes=[
                "openid", "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"])
        google_flow.redirect_uri = redirect

        try:
            authorization_response = f'https://{redirect}/?code={code}'
            google_flow.fetch_token(authorization_response=authorization_response)
            credentials = google_flow.credentials
            userinfo = build("oauth2", "v2", credentials=credentials).userinfo().get().execute()
        except Exception as e:
            clean_creds_json()
            return Response({'error': f'{e}'})

        serializer = self.InputSerializer(data=userinfo)
        serializer.is_valid(raise_exception=True)
        user = user_get_or_create(
            serializer.validated_data.get('email'),
            serializer.validated_data.get('given_name', 'User'),
            serializer.validated_data.get('family_name', ''),
            serializer.validated_data.get('picture', ''),
        )
        response_jwt = jwt_login(user=user)
        response = Response(data=user_get_me(user=user, jwt=response_jwt))
        clean_creds_json()
        return response


class UserProfileView(APIView):

    def get(self, request, *args, **kwargs):
        user = user_check_auth(request)
        data = model_to_dict(user)
        data['request'] = request
        serializer = UserProfileSerializer(data)
        return Response({'profile': serializer.data})


class UserAddHashView(APIView):
    class InputSerializer(serializers.Serializer):
        hash = serializers.CharField(max_length=16)

    def post(self, request, *args, **kwargs):
        user = user_check_auth(request)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.filter(add_hash=serializer.validated_data.get('hash')).first()
        if order and order.user_uuid is None:
            order.user_uuid = user.username
            order.save()
            return Response({'status': 'success added'})
        return Response({'status': 'error added'})


class UserLoadExcel(APIView):

    def post(self, request):

        user = True if 'email' in request.data else False
        file_name = f'{request.data["file"]}.xlsx'
        s3 = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        folder = 'orders_excel'

        if user:
            email_orders = Order.objects.filter(email=request.data['email'])
            name_orders = Order.objects.filter(email=request.data['name'])
            phone_orders = Order.objects.filter(email=request.data['phone'])
            orders = email_orders | name_orders | phone_orders
            if len(orders) == 0:
                return Response({'status': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            orders = Order.objects.all()

        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        base_format = workbook.add_format()
        base_format.set_align('center')
        bold_format = workbook.add_format({'bold': True})
        bold_format.set_align('center')

        row = 0
        idx = 1

        for col in range(1, 13):
            worksheet.set_column(col, col, 16)

        headings_list = ['#', 'FULL NAME', 'COUNTRY', 'EMAIL', 'PHONE', 'TOTAL PAID', 'CURRENCY', 'TICKET PURCHASED',
                         'WON TICKETS', 'ORDER DATE', 'UNIQUE ID ORDER', 'STATUS ORDER']

        for i in range(12):
            worksheet.write(row, i, headings_list[i], base_format)

        row += 1

        for order in orders:
            winners = [i.number for i in order.tickets.filter(is_winner=True)]

            worksheet.write(row, 0, idx, base_format)
            worksheet.write(row, 1, order.name, base_format)
            worksheet.write(row, 2, 'MX', base_format)
            worksheet.write(row, 3, order.email, base_format)
            worksheet.write(row, 4, order.phone, base_format)
            worksheet.write(row, 5, order.amount, base_format)
            worksheet.write(row, 6, '$', base_format)
            worksheet.write(row, 7, len(order.tickets.all()), base_format)
            worksheet.write(row, 8, len(winners), base_format)
            worksheet.write(row, 9, str(order.created).split(' ')[0], base_format)
            worksheet.write(row, 10, str(order.uuid), base_format)
            worksheet.write(row, 11, order.status, base_format)

            if not user:
                worksheet.merge_range(row + 1, 7, row + 1, 11, 'Tickets', base_format)
                worksheet.write(row + 2, 7, 'EVENT', base_format)
                worksheet.write(row + 2, 8, 'NUMBER', base_format)
                worksheet.write(row + 2, 9, 'PRICE', base_format)
                worksheet.write(row + 2, 10, 'CURRENCY', base_format)
                worksheet.write(row + 2, 11, 'WINNER?', base_format)

                events = list(set([i.event for i in order.tickets.all()]))

                for event in events:
                    tickets = order.tickets.filter(event_id=event.id)
                    tickets_sum = 0
                    for ticket in tickets:
                        ticket_values_list = [ticket.event.title, ticket.number, str(ticket.price), '$',
                                              'YES' if ticket.is_winner else 'NO']
                        color = '#FF0000' if not ticket.is_winner else '#00FF00'
                        ticket_format = workbook.add_format()
                        ticket_format.set_align('center')
                        ticket_format.set_pattern(1)
                        ticket_format.set_bg_color(color)

                        for fill_ticket in range(5):
                            worksheet.write(row + 3, 7 + fill_ticket, ticket_values_list[fill_ticket], ticket_format)
                        tickets_sum += ticket.price
                        row += 1

                    total_values_list = ['TOTAL', '-', str(float(tickets_sum)), '$', '-']

                    for fill_total in range(5):
                        worksheet.write(row + 3, 7 + fill_total, total_values_list[fill_total], base_format)
                    row += 1
                row += 4
                idx += 1
            else:
                row += 2
                idx += 1
        workbook.close()

        with open(file_name, 'rb') as f:
            s3.upload_fileobj(f, bucket_name, f'static/{folder}/{file_name}', ExtraArgs={'ACL': 'public-read'})

        os.remove(file_name)

        return Response({'status': 'excel file created'})


class UserDeletePaymentToken(APIView):

    def get(self, request, *args, **kwargs):
        user = user_check_auth(request)
        token = PaymentTokenService.objects.filter(user=user).first()

        if token:
            token.delete()
            return Response({'status': 'success delete token'})
        return Response({'status': 'error delete token'})
