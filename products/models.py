from django.utils import timezone
import datetime
from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
# Create your models here.

protected_loc = settings.PROTECTED_UPLOADS
def download_loc(instance, filename):
    if instance.user.username:
        return "%s/download/%s"%(instance.user.username, filename)
    else:
        return "%s/download/%s"%("default", filename)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=255)
    download = models.FileField(upload_to=download_loc, storage=FileSystemStorage(location=protected_loc), null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price > 0:
            return self.sale_price
        return self.price

    def get_absolute_url(self):
        return reverse("product:detail", args=[self.slug])


    def get_featured_image(self):
        try:
            images = self.productimage_set.all()
        except:
            return None
        for i in images:
            if i.feautured_image:
                return i.image
            else:
                return None


    def is_active(self):
        return self.active


    def edit_product_url(self):
        return reverse("product:edit_product", args=[self.slug])



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='products/image')
    title = models.CharField(max_length=120, null=True, blank=True)
    feautured_image = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.product.title)

class Tag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.CharField(max_length=120, blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.tag


class Category(models.Model):
    products = models.ManyToManyField(Product)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    class Meta: 
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-order"]

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse("product:category", args=[self.slug])






class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/image')
    title = models.CharField(max_length=120, null=True, blank=True)
    feautured_image = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.category)


class FeaturedManager(models.Manager):
    def get_featured_instance(self):
        items = super(FeaturedManager, self).filter(date_start__lte=datetime.datetime.now(tz=timezone.utc)).filter(date_end__gte=datetime.datetime.now(tz=timezone.utc))
        all_items = super(FeaturedManager, self).all()
        if len(items) >= 1:
            return items[0]
        else:
            for i in all_items:
                if i.default:
                    return i
            return all_items[0]



class Feautured(models.Model):
    title = models.CharField(max_length=150)
    products = models.ManyToManyField(Product, limit_choices_to={'active':True}, blank=True)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    date_end = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)


    objects = FeaturedManager()

    def __str__(self):
        return str(self.title)

    def get_featured(self):
        return self.products[:4]

    class Meta:
        verbose_name = "Featured"
        verbose_name_plural = "Featured"