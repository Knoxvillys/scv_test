from django.db import models
from django.db.models import Sum, Count


class UserCustomer(models.Model):
    user = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user

    def total(self):
        return UserCustomer.objects.annotate(tot=Sum('total_trades'), num=Count('id')).order_by('total_sum')


class Items(models.Model):
    items = models.CharField(max_length=50)

    def __str__(self):
        return self.items


class Transaction(models.Model):
    customer = models.ForeignKey(UserCustomer, on_delete=models.CASCADE, related_name='trades')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='trades')
    total = models.IntegerField(verbose_name="total")
    quantity = models.IntegerField(verbose_name="quantity")
    date = models.DateTimeField(verbose_name="date")

    def __str__(self):
        return self.customer