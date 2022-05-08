from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("product/list/", views.list_all, name="all_products"),
    path("product/<slug:slug>/", views.single_product, name="detail"),
    path("product/create", views.create_product,name="create_product"),
    path("product/edit/<slug:slug>/", views.edit_product,name="edit_product"),
    path('product/<slug:slug>/download/<filename>/', views.download_product, name='download_product'),
    path("product/<slug:slug>/image/", views.manage_product_image,name="image_product"),
    path("product/search", views.search, name="search"),
    path('category/<slug:slug>/', views.category_single, name='category'),
]