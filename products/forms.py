from django.forms import ModelForm, forms
from .models import Product, ProductImage

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = {
            "title", "description","price", "sale_price" 
        }



class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'feautured_image']