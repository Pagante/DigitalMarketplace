from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.dispatch import receiver
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=100, default=0,decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     totals = [item.product.price for item in self.cartitem_set.all()]
    #     new_total = sum(totals)
    #     self.total = new_total
    #     super(Cart, self).save(*args, **kwargs)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.product.title)


@receiver([signals.post_save, signals.post_delete], sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    totals = [item.product.get_price() for item in cart.cartitem_set.all()]
    cart.total = sum(totals)
    cart.save()

