import csv

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count

from .serializer import (
    TransactionSerializer,
    FileSSerializer,
    UserCustomerSerializer,
    ItemsSerializer
)
from .models import (
    UserCustomer,
    Items,
    Transaction
)


class UploadViewSet(ViewSet):
    serializer = TransactionSerializer
    
    def posts(self, request):
        file_serializer = FileSSerializer(data=request.data)
        file_decoded = file_serializer.read().decoded('utf-8').splitlines()
        reader = csv.DictReader(file_decoded)
        for value in reader:
            dictionary = dict(value)
            user_serializer = UserCustomerSerializer(data=dictionary)
            item_serializer = ItemsSerializer(data=dictionary)
            
            user, created = UserCustomer.objects.get_or_create(username=user_serializer.validated_data['username'])
            item, created = Items.objects.get_or_create(username=item_serializer.validated_data['text'])

            tran_serializer = TransactionSerializer(data=dictionary)
            Transaction.objects.get_or_create(
                customer=user,
                item=item,
                total=tran_serializer.validated_data['total'],
                quantity=tran_serializer.validated_data['quantity'],
                date=tran_serializer.validated_data['date'],
            )
        return Response(status=status.HTTP_201_CREATED)
    
    def get(self):
        buyers = UserCustomer.objects.annotate(
            tot=Sum('total_trades'), num=Count('id')).order_by('total_sum')[:5].prefetch_related('transaction')
        users_gems = {}
        for user in buyers:
            user_gems = set(recording.item for recording in user.transaction.select_related('item'))
            users_gems[user] = user_gems

        users = []
        for user in buyers:
            user_gems = users_gems.pop(user)
            other_user_gems = []
            
            for gems in users_gems.values():
                other_user_gems.extend(gems)
                
            cross_gems = []
            for user_gem in user_gems:
                if user_gem in other_user_gems:
                    cross_gems.append(user_gem.text)
            users_gems[user] = user_gems
            users.append({'username': user.username,
                          'spent_money': user.total_sum,
                          'gems': cross_gems})
        return Response(users, status=status.HTTP_200_OK)
        



