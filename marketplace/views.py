from django.shortcuts import get_object_or_404, render
from products.models import Category, Product, CategoryImage, Feautured

def index(request):
    featured_products = []
    
    featured = Feautured.objects.get_featured_instance()
    for i in featured.products.all():
        featured_products.append(i)
    category = Category.objects.filter()[:3]

    context = {
        "category": category,
        "featured_products": featured_products,
        "featured": featured,
    }
    return render(request, "index.html", context)