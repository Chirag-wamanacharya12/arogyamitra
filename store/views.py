from .models import PrimaryCategory, fullBanner, ProductBase, SubCategory, ProductImage
from .models import PricingDetails, Cart, CustomUser, ImportantInfo, Order, processedtocheck
from paypal.standard.forms import PayPalPaymentsForm
from user.models import UserAddress
from userprofile.models import Medication
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from django.http import JsonResponse
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse
import uuid
import json
import re



def store(request):
    user = request.user
    primarycat = PrimaryCategory.objects.all()
    address = UserAddress.objects.filter(user=user, is_default=True) if user.is_authenticated else None
    banners = fullBanner.objects.order_by('?') 
    featuredProd = ProductBase.objects.filter(is_featured=True)
    context = {
        'primarycat':primarycat,
        'banners':banners,
        'featuredProd':featuredProd,
        'addresses':address,
    }
    return render(request,'store/store.html',context)

def viewProduct(request, primary_id, sub_id=None):
    # Fetch all subcategories under the selected primary category
    SubCat = SubCategory.objects.filter(primary_category=primary_id)

    # Filter products based on primary category (default)
    product = ProductBase.objects.filter(PrimaryCategory=primary_id)

    # If a subcategory is selected, further filter products
    if sub_id:
        product = product.filter(SubCategory=sub_id)

    # Fetch related images and pricing details
    productImage = ProductImage.objects.filter(product__in=product)
    pricing = PricingDetails.objects.filter(product__in=product)

    # Get current user and cart details


    # Calculate discounted price
    for price in pricing:
        price.discounted_price = price.price - (price.price * price.offer / 100)

    user = request.user
    if user.is_authenticated :
        address = UserAddress.objects.filter(user=user, is_default=True).first()
    else:
        address = None 

    context = {
        'product': product,
        'productImage': productImage,
        'pricing': pricing,
        'SubCat': SubCat,
        'address' : address,
        'primary_id': primary_id,  # Pass primary category ID to the template
    }

    return render(request, 'store/viewProduct.html', context)

def productDetails(request, id):
    product = get_object_or_404(ProductBase, id=id)  # Get a single product object
    product_images = get_object_or_404(ProductImage, product=product)
    pricing = PricingDetails.objects.filter(product=product)  
    guides = ImportantInfo.objects.filter(product=product) 
    user = request.user
    prodQty = Cart.objects.filter(product=product,uid=user).aggregate(Sum('qty'))['qty__sum'] or 0
    

    # Calculate discounted price
    for price in pricing:
        price.discounted_price = price.price - (price.price * price.offer / 100)
    
    integer_part, decimal_part = str(price.discounted_price).split('.')

    # Extract quantity as an integer
    quantity_text = product.quantity  # Assuming quantity is a string like "Strip of 15 Tablets"
    quantity_match = re.search(r'\d+', quantity_text)  # Extract the number
    quantity = int(quantity_match.group()) if quantity_match else None  # Convert to int

    from datetime import datetime, timedelta
    # Get current date
    current_date = datetime.now()
    # Add 2 days
    future_date = current_date + timedelta(days=2)
    # Format the date as "Thursday, 13 March"
    formatted_date = future_date.strftime("%A, %d %B")

    address = UserAddress.objects.filter(user=user, is_default=True).first()

    pricePerUnit = price.discounted_price/quantity
    pricePerUnit = round(pricePerUnit, 2)


    # Process each guide to split text fields by line
    for guide in guides:
        guide.direction_to_use = guide.direction_to_use.split('\n')
        guide.direction_to_store = guide.direction_to_store.split('\n')

    

    
    images = [
        product_images.image1.url if product_images.image1 else None,
        product_images.image2.url if product_images.image2 else None,
        product_images.image3.url if product_images.image3 else None,
        product_images.image4.url if product_images.image4 else None,
        product_images.image5.url if product_images.image5 else None,
        product_images.image6.url if product_images.image6 else None,
        product_images.image7.url if product_images.image7 else None,
        product_images.image8.url if product_images.image8 else None,
    ]

    # Remove None values (if any images are not uploaded)
    images = [img for img in images if img]

    context = {
        'product': product,
        'product_images': images,
        'pricing': pricing,
        'guides': guides,
        'integer_part': integer_part,
        'decimal_part': decimal_part,
        'pricePerUnit' : pricePerUnit, # Pass extracted quantity
        'delDate' : formatted_date,
        'user' : user,
        'address' : address,
        'quantity' : prodQty,
    }
    
    return render(request, 'store/productDetails.html', context)

def productList(request):
    return render(request, 'productList.html')

def addToCart(request, id):
    userid = request.user.id
    selected_qty = request.GET.get('quantity')

    # Convert selected_qty to integer and set default to 1
    try:
        selected_qty = int(selected_qty) if selected_qty else 1
    except ValueError:
        return JsonResponse({"error": "Invalid quantity"}, status=400)

    # Get user instance
    user = get_object_or_404(CustomUser, id=userid)

    # Get product instance
    product = get_object_or_404(ProductBase, id=id)

    # Get pricedetails instance
    Pricing = get_object_or_404(PricingDetails, product=id)

    # Get prodImage instance
    prodImage = get_object_or_404(ProductImage, product=id)

    # Check if product is already in cart
    cart_item, created = Cart.objects.get_or_create(uid=user, product=product, defaults={
        'Pricing': Pricing,
        'prodImage': prodImage,
        'qty': selected_qty
    })

    if not created:  # If product already exists in cart
        cart_item.qty += selected_qty  # Increment quantity
        cart_item.save()

    return redirect('cart')

def viewCart(request):
    id = request.user.id
    user = CustomUser.objects.get(id=id)
    cart = Cart.objects.filter(uid=user)

    total = 0  # Initialize total before loop
    for item in cart:
        # Get the original price
        original_price = item.Pricing.price if item.Pricing else Decimal(0)  

        # Calculate discounted price
        if item.Pricing and item.Pricing.offer:
            discounted_price = original_price - (original_price * Decimal(item.Pricing.offer) / 100)
        else:
            discounted_price = original_price  

        item.discounted_price = round(discounted_price, 2)

        # Total price per product (discounted price * quantity)
        item.total_price = item.discounted_price * item.qty  
    subtotal = sum(item.total_price for item in cart if item.checkedToProceed)



    cart_exists = cart.exists()  # Check if cart has items
    address = UserAddress.objects.filter(user=user).first()


    context = {
        'cart': cart,
        'subtotal': subtotal,  # Correct total (sum of all product totals)
        'cart_exists': cart_exists,
        'address': address,
    }

    return render(request, 'store/cart.html', context)

def updateQty(request,qv,id):
    product_details = Cart.objects.filter(id=id)
    if qv=='1': # Increase quantity
        if product_details[0].qty<10:
            updatedQty=product_details[0].qty+1
            product_details.update(qty=updatedQty)
        else:
            updatedQty=10
        return redirect('/cart')

    if qv == '0':  # Decrease quantity
        if product_details[0].qty > 1:  # Prevent quantity from going below 1
            updatedQty = product_details[0].qty - 1
            product_details.update(qty=updatedQty)
        else:
            updatedQty = 1  # Ensure the minimum quantity stays at 1 (optional safeguard)
        
        return redirect('cart')

def savedForLater(request, id):
    product_details = Cart.objects.filter(id=id)
    product_details.update(savedForLater=True)
    return redirect('cart')

def removeFromSaved(request, id):
    product_details = Cart.objects.filter(id=id)
    product_details.update(savedForLater=False)
    return redirect('cart')

def deleteFromCart(request, id):
    user = request.user  # Get logged-in user
    cart_item = get_object_or_404(Cart, id=id, uid=user)  # Get the specific cart item
    
    cart_item.delete()  # Delete the selected cart item
    
    return redirect('cart')  # Redirect to cart page

def checkedToProceed(request, id):
    product_details = Cart.objects.filter(id=id)
    product_details.update(checkedToProceed=True)
    return redirect('cart')

def uncheckedToProceed(request, id):
    product_details = Cart.objects.filter(id=id)
    product_details.update(checkedToProceed=False)
    return redirect('cart')

def medication(request):
    user = request.user
    print("Logged in user:", user)

    # Fetch the user's medications
    medications = Medication.objects.filter(user=user)
    medication_names = list(medications.values_list('name', flat=True))

    print("Medication names:", medication_names)

    # Use case-insensitive lookup and handle empty names
    products = ProductBase.objects.filter(
        name__in=medication_names,
        is_active=True
    ) if medication_names else ProductBase.objects.none()

    print("Found products:", list(products.values_list('name', flat=True)))

    # Calculate discounted prices for products
    pricing_details = PricingDetails.objects.filter(product__in=products)
    for price in pricing_details:
        price.discounted_price = price.price - (price.price * price.offer / 100)

    product_images = ProductImage.objects.filter(product__in=products)

    context = {
        'medications': medications,
        'product': products,  # Changed from 'product' to 'products' for clarity
        'productImage': product_images,
        'pricing': pricing_details,
        'no_medications': not medications.exists(),  # Flag to check if user has any medications
        'no_matches': medications.exists() and not products.exists(),  # Flag to check if no products match medications
    }
    
    return render(request, 'store/store.html', context)

@login_required
def submit_address(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        country = request.POST.get("country")
        additional_notes = request.POST.get("additional_notes", "")

        processedtocheck.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            pin_code=pin_code,
            country=country,
            additional_notes=additional_notes
        )
        
        messages.success(request, "Checkout details submitted successfully!")
        return redirect('checkout') 

    messages.error(request, "Invalid request method!")
    return redirect('checkout')

def checkout(request):
    id = request.user.id
    user = CustomUser.objects.get(id=id)
    cart = Cart.objects.filter(uid=user, checkedToProceed=True)

    total = 0  # Initialize total before loop
    for item in cart:
        # Get the original price
        original_price = item.Pricing.price if item.Pricing else Decimal(0)  

        # Calculate discounted price
        if item.Pricing and item.Pricing.offer:
            discounted_price = original_price - (original_price * Decimal(item.Pricing.offer) / 100)
        else:
            discounted_price = original_price  

        item.discounted_price = round(discounted_price, 2)

        # Total price per product (discounted price * quantity)
        item.total_price = item.discounted_price * item.qty  
    subtotal = sum(item.total_price for item in cart if item.checkedToProceed)

    # Apply delivery charges based on order value
    delivery_charge = 0
    if subtotal < 3000:
        delivery_charge = (subtotal * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else :
        delivery_charge = 0
    
    grand_total = subtotal + delivery_charge  # Final amount after adding delivery charge
    tax = (subtotal * Decimal("0.18")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    insurance = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    handling = (subtotal * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    shipping = delivery_charge
    totalamount = subtotal + tax + insurance + handling + shipping



    isAddressExists = UserAddress.objects.filter(user=user).exists()
    addresses = UserAddress.objects.filter(user=user)
    address = UserAddress.objects.filter(user=user).first()

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': totalamount,  # Use grand total instead of just totalamount
        'item_name':"medicine",
        'invoice': str(uuid.uuid4()),  # Unique invoice number
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment_success')}",
        'cancel_url': f"http://{host}{reverse('payment_cancel')}",

        # Send breakdown as a string (or use order_id if needed)
         'custom': f"Subtotal: {subtotal}, Tax: {tax}, Shipping: {shipping}, Insurance: {insurance}, Handling: {handling}"# Sending extra details in JSON format
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
        'isAddressExists' : isAddressExists,
        'addresses' : addresses,
        'address' : address,
        'paypal_payment' : paypal_payment,

    }
    return render(request, 'store/proceedToCheck.html', context)

def payment_cancel(request):
    messages.error(request, "Payment was cancelled.")
    return redirect('checkout')

def payment_success(request):
    user = request.user
    cart = Cart.objects.filter(uid=user, checkedToProceed=True)

    address = UserAddress.objects.filter(user=user).first()

    orderlist = []
    total = 0

    for item in cart:
        product = item.product
        pricing = item.Pricing
        qty = item.qty
        total = pricing.price * qty
        orderlist.append({
            'product': product,
            'pricing': pricing,
            'qty': qty, 
        })

        # Create an order entry
        order = Order(
            user=user,
            product=product,
            Pricing=pricing, 
            quantity=qty,
            total_price=total,
            address=address,
            order_status='Pending', 
        )
        order.save()

        # Clear the orderlit after processing the order
        orderlist.clear()
        # Clear total after processing the order
        total = 0

    # Clear the cart after processing the order
    cart.delete()
    return redirect('store')






# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# from user.models import UserAddress
# from store.models import ProductBase, PricingDetails, Order  # Ensure these models exist

# @csrf_exempt
# @login_required
# def process_order(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             order_id = data.get("orderID")
#             payer_id = data.get("payerID")
#             transaction_id = data.get("transactionID")
#             amount = float(data.get("amount", 0))  # Default to 0 if missing
#             product_id = data.get("product_id")  
#             pricing_id = data.get("pricing_id")  
#             quantity = int(data.get("quantity", 1))  # Default to 1 if missing

#             # Get user
#             user = request.user
#             address = UserAddress.objects.filter(user=user).first()  
#             if not address:
#                 return JsonResponse({"success": False, "message": "No address found!"}, status=400)

#             # Fetch product and pricing details
#             product = ProductBase.objects.filter(id=product_id).first()
#             if not product:
#                 return JsonResponse({"success": False, "message": "Invalid product ID"}, status=400)

#             pricing = PricingDetails.objects.filter(id=pricing_id, product=product).first()
#             if not pricing:
#                 return JsonResponse({"success": False, "message": "Invalid pricing ID"}, status=400)

#             # Save order in the database
#             order = Order.objects.create(
#                 user=user,
#                 product=product,
#                 quantity=quantity,
#                 pricing=pricing,  # Fixed typo
#                 total_price=amount,
#                 address=address,
#                 order_status="Pending"
#             )
#             print("Order placed successfully!")

#             return JsonResponse({"success": True, "message": "Order placed successfully!"})

#         except Exception as e:
#             return JsonResponse({"success": False, "message": str(e)}, status=500)

#     return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
