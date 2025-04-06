from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from .models import ClickedProduct
from store.models import ProductBase, PricingDetails, ImportantInfo, ProductReview, ProductImage

def search(request):
    return render(request,'userTrends/search.html')

def search_products(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"products": [], "pricing": [], "important_info": [], "reviews": []})

    product = list(ProductBase.objects.filter(Q(name__icontains=query) | Q(title__icontains=query)).values("id", "name", "brand_name", "quantity","rating"))
    pricing = list(PricingDetails.objects.filter(Q(product__name__icontains=query) | Q(product__title__icontains=query)).values("product__name", "price", "offer"))
    prodImage = list(ProductImage.objects.filter(Q(product__name__icontains=query) | Q(product__title__icontains=query)).values("product__name", "image1"))
    important_info = list(ImportantInfo.objects.filter(Q(product__name__icontains=query) | Q(product__title__icontains=query)).values("product__name", "direction_to_use", "direction_to_store"))
    reviews = list(ProductReview.objects.filter(Q(product__name__icontains=query) | Q(product__title__icontains=query)).values("product__name", "user__username", "rating", "review"))

    return JsonResponse({
        "products": product,
        "pricing": pricing,
        "important_info": important_info,
        "reviews": reviews,
        "prodImage": prodImage
    })
