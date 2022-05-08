from pyexpat import model
from django.contrib import admin
from .models import (Product, 
    Category, 
    ProductImage, 
    Tag, 
    CategoryImage,
    Feautured,)
# Register your models here.
class TagInline(admin.TabularInline):
    prepopulated_fields = {"slug": ("tag",)}
    extra = 1
    model = Tag


class ProductImageInline(admin.TabularInline):
    extra = 1
    model=ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','current_price', 'order','categories', 'active']
    inlines = [TagInline, ProductImageInline]
    search_fields = ['title', 'description', 'price', 'category__title', 'category__description']
    list_filter = ['price', 'timestamp', 'title']
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ['active',]
    
    
    class Meta:
        model = Product

    def current_price(self, object):
        if object.sale_price > 0:
            return object.sale_price
        
        else:
            return object.price

    def categories(self, object):
        cat = []
        for i in object.category_set.all():
            cat.append(i.title)
        return ",".join(cat)



admin.site.register(Product, ProductAdmin)


class CategoryImageInline(admin.TabularInline):
    extra = 1
    model = CategoryImage

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CategoryImageInline,]
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)

admin.site.register(Feautured)