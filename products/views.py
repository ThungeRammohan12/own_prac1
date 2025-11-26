from django.shortcuts import render

# Create your views here.
import cloudinary.uploader

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import cloudinary.uploader
import json

@csrf_exempt
def create_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        image_file = request.FILES.get("image")   # form-data file

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result["secure_url"]

        # Create product
        product = Product.objects.create(
            name=name,
            price=price,
            image=image_url
        )

        return JsonResponse({
            "message": "Product created",
            "product_id": product.id
        }, status=201)

    return JsonResponse({"error": "Invalid method"}, status=405)


def get_products(request):
    products = Product.objects.all()

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "image": p.image
        }
        for p in products
    ]

    return JsonResponse(data, safe=False)

def get_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    data = {
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "image": product.image
    }

    return JsonResponse(data)

@csrf_exempt
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    if request.method == "POST":  # using POST as form-data (PUT is not supported by forms)
        name = request.POST.get("name", product.name)
        price = request.POST.get("price", product.price)

        # If new image uploaded
        if request.FILES.get("image"):
            upload_result = cloudinary.uploader.upload(request.FILES["image"])
            product.image = upload_result["secure_url"]

        product.name = name
        product.price = price
        product.save()

        return JsonResponse({"message": "Product updated"})

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({"message": "Product deleted"})

    return JsonResponse({"error": "Invalid method"}, status=405)


