from django.contrib import admin

# Register your models here.
from .models import UserCustomer, Items, Transaction

admin.site.register(UserCustomer)
admin.site.register(Items)
admin.site.register(Transaction)