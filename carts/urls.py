from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/update_cart/<int:id>/", views.update_cart, name="update_cart"),
    path("cart/cart", views.cart, name="cart")
]