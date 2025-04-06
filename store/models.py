from django.db import models
from user.models import CustomUser, UserAddress
from datetime import timedelta
from django.utils import timezone

# Primary Category Model
class PrimaryCategory(models.Model):
    cat_Name=models.CharField(max_length=100)
    cat_image = models.ImageField(upload_to='primaryCat')
    cat_Desc=models.TextField()
    is_ageRestricted = models.BooleanField(default=False)
    # Add any other fields you want for the primary category
    
    def __str__(self):
        return self.cat_Name

class fullBanner(models.Model):
    image = models.ImageField(upload_to='banners')
    brandName = models.CharField(max_length=50)

    def __str__(self):
        return self.brandName

# Sub Category Model
class SubCategory(models.Model):
    primary_category = models.ForeignKey(PrimaryCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Add any other fields you want for the sub category
    
    def __str__(self):
        return self.name

class Formulation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ProductBase(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    title = models.TextField()
    brand_name = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)
    total_purchased = models.PositiveIntegerField(default=0)
    quantity = models.CharField(max_length=50, null=True,blank=True)  # Quantity of the product, e.g. 10 tablets, 200 ml
    item_code = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=False)
    PrimaryCategory = models.ForeignKey(PrimaryCategory, on_delete=models.CASCADE,null=True, related_name='products')
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True, related_name='products')
    is_prescription_required = models.BooleanField(default=False)
    formulation = models.ForeignKey(Formulation, on_delete=models.CASCADE, related_name='products')
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='images')
    image1 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image5 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image6 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image7 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)
    image8 = models.ImageField(upload_to='product_images/`{product.brand_name}`',blank=True, null=True)

    def __str__(self):
        return f"Images for {self.product.name}"

class PricingDetails(models.Model):
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='pricing')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.IntegerField(default=0)  # Percentage off
    ends_in = models.DateTimeField(null=True, blank=True)  # Offer end time

    def __str__(self):
        return f"Pricing for {self.product.name}"

class ImportantInfo(models.Model):
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='important_info')
    direction_to_use = models.TextField()
    direction_to_store = models.TextField()

    def __str__(self):
        return f"Important Info for {self.product.name}"

class ProductReview(models.Model):
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='address', default=None)
    quantity = models.PositiveIntegerField(default=1)
    Pricing=models.ForeignKey(PricingDetails,on_delete=models.CASCADE,db_column='pricing_id',default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Cart(models.Model):
    uid=models.ForeignKey(CustomUser,on_delete=models.CASCADE,db_column='uid',null=True,blank=True)
    product=models.ForeignKey(ProductBase,on_delete=models.CASCADE,db_column='pid')
    Pricing=models.ForeignKey(PricingDetails,on_delete=models.CASCADE,db_column='pricing_id',default=None)
    prodImage=models.ForeignKey(ProductImage,on_delete=models.CASCADE,db_column='image_id',default=None)
    savedForLater=models.BooleanField(default=False)
    checkedToProceed=models.BooleanField(default=True)
    qty=models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.id} by {self.product.name}"

class Tray(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trays')
    products = models.ManyToManyField(ProductBase, related_name='trays')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_checked_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(hours=24)  # Auto-set expiration
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"Tray for {self.user.username} (Checked Out: {self.is_checked_out})"

class processedtocheck(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name