import imp
import os
from itertools import chain
from django.db.models import Q
from django.db.models.query import QuerySet
from mimetypes import guess_type
from django.conf import settings
from carts.models import Cart
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelform_factory, modelformset_factory
from django.utils.text import slugify
from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageForm
from wsgiref.util import FileWrapper




# Create your views here.
def check_product(user, product):
    if product in user.userpurchase.products.all():
        return True
    else:
        return False



def download_product(request, slug, filename):
    product = Product.objects.get(slug=slug)
    if product in (request.user.userpurchase.products.all()):
        product_file = str(product.download)
        file_path = os.path.join(settings.PROTECTED_UPLOADS, product_file)
        wrapper = FileWrapper(open(file_path, "rb"))
        response = HttpResponse(wrapper, content_type=guess_type(product_file))
        response['Content-Disposition'] = "attachment;filename=%s" %filename
        response['Content-Type'] = ''
        response['X-SendFile'] = file_path
        return response
    
    else:
        raise Http404




def list_all(request):
    products = Product.objects.filter(active=True)

    context = {
        "products": products,
    }
    return render(request, 'products/list.html', context)

def manage_product_image(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except:
        product = False

    
    if request.user == product.user:
        queryset = ProductImage.objects.filter(product__slug=slug)
        ProductImageFormset = modelformset_factory(ProductImage, form=ProductImageForm, extra=0, can_delete=True)
        formset = ProductImageFormset(request.POST or None, request.FILES or None, queryset=queryset)
        form = ProductImageForm(request.POST or None, request.FILES or None)
        
        if formset.is_valid() and form.is_valid():
            post = form.save(commit=False)
            post.image = form.cleaned_data['image']
            post.feautured_image = form.cleaned_data['feautured_image']
            post.save()

            for form in formset:
                instance = form.save(commit=False)
                instance.save()
            if formset.deleted_forms:
                formset.save()
        
        context = {
            "form": form,
            "queryset": queryset,
            "formset": formset,
            "product": product
        }

 
        return render(request, "products/manage_images.html", context)
    else:
        raise Http404


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        
        product = form.save(commit=False)
        product.user = request.user
        product.slug = slugify(form.cleaned_data['title'])

        product.active = True
        product.save()
        # return redirect('product/detail')
        return HttpResponseRedirect ('/product/%s'%(product.slug))
    return render(request, 'products/edit.html', {"form":form})



def edit_product(request, slug):
    instance = Product.objects.get(slug=slug)
    if request.user == instance.user:

        form = ProductForm(request.POST or None,instance=instance)
        if form.is_valid():
            product_edit = form.save(commit=False)
            product_edit.save()
        context = {
            'instance': instance,
            'form': form,
        }
        return render(request, 'products/edit.html', context)
    else:
        raise Http404
def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.productimage_set.all()

    categories = product.category_set.all()
    if request.user.is_authenticated:
        downloadable = check_product(request.user, product)
    
    else:
        downloadable = False

    related = []
    if len(categories) >=1:
        for category in categories:
            product_category = category.products.all()
            for item in product_category:
                if not item == product:
                    related.append(item)


    in_cart = 0
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        for item in cart.cartitem_set.all():
            if item.product == product:
                in_cart = True
    except:
        in_cart = False
    context = {
        "product": product,
        "categories": categories,
        "edit": True,
        "images": images,
        "downloadable": downloadable,
        "in_cart": in_cart,
        'related': related,
    }
    return render(request, "products/detail.html", context)


def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
    
    if q:
        query = q
    
    product_queryset = Product.objects.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)
    )
    category_queryset = Category.objects.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)
    )

    
    results = list(chain(product_queryset, category_queryset))
    print(results)

    context = {
        "results": results,
        'query': query,

    }
        
    return render(request, "products/search.html", context)


def category_single(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    
    except:
        raise Http404

    products = category.products.all()

    related = []
    for item in products:
        product_categories = item.category_set.all()
        for single_category in product_categories:
            if not single_category == category:
                related.append(single_category)
    context = {
        "category": category,
        'related': related,
    }
    return render(request, "products/category.html", context)
