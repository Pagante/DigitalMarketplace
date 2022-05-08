from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path("profile/lib", views.library, name="lib")
]