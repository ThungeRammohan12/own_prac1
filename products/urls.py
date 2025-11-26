from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.get_products),
    path("products/create/", views.create_product),
    path("products/<int:id>/", views.get_product),
    path("products/update/<int:id>/", views.update_product),
    path("products/delete/<int:id>/", views.delete_product),
]
