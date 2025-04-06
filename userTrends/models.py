from django.db import models
from user.models import CustomUser
from store.models import ProductBase, ProductImage, PricingDetails, ImportantInfo, ProductReview

class ClickedProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Store user info
    product = models.ForeignKey(ProductBase, on_delete=models.CASCADE)  # Link to the Product model
    price = models.ForeignKey(PricingDetails, on_delete=models.CASCADE)  # Link to the Pricing model
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)  # Link to the Image model
    info = models.ForeignKey(ImportantInfo, on_delete=models.CASCADE)  # Link to the Info model
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)  # Link to the Review model
    clicked_at = models.DateTimeField(auto_now_add=True)  # Timestamp when clicked

    def __str__(self):
        return f"{self.user} clicked {self.product.name} at {self.clicked_at}"
