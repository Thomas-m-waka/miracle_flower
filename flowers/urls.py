from django.urls import path

from . import views

app_name = "flowers"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("<slug:slug>/", views.detail, name="detail"),
]
