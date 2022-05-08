from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelform_factory, modelformset_factory
from django.utils.text import slugify
from .models import UserPurchase
# Create your views here.

def library(request):
    if request.user.is_authenticated:
        products = request.user.userpurchase.products.all()


        context = {
            'products': products,
        }
        return render (request, "profiles/library.html", context)
    else:
        raise Http404
    
