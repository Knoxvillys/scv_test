from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField

from .models import UserCustomer, Items, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username')
    item = serializers.CharField(source='item.text')

    class Meta:
        model = Transaction
        fields = ['customer', 'item', 'total', 'quantity', 'date']


class FileSSerializer(Serializer):
    file = FileField()
    
    class Meta:
        fields = ['file_uploaded']


class UserCustomerSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='username')

    class Meta:
        model = UserCustomer
        fields = ['customer']


class ItemsSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='text')

    class Meta:
        model = Items
        fields = ['item']