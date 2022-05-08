from django.contrib import admin
from .models import UserPurchase
# Register your models here.

class UserPurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'products']
    class Meta:
        model = UserPurchase


admin.site.register(UserPurchase)
