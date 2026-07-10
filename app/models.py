from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Mobile", "Mobile"),
        ("Laptop", "Laptop"),
        ("Accessory", "Accessory"),
        ("Gadgets", "Gadgets"),
        ("Audio", "Audio"),
    ]

    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    stock = models.IntegerField(default=0)

    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="Mobile"
    )

    rating = models.FloatField(default=4.2)
    reviews_count = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)

    warranty = models.CharField(max_length=100, default="1 Year Warranty")

    return_policy = models.CharField(max_length=100, default="7 Day Return Policy")

    delivery_info = models.CharField(
        max_length=100, default="Free Delivery in 2-4 Days"
    )

    highlights = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} "


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    # Customer Details
    full_name = models.CharField(max_length=100, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    mobile = models.CharField(max_length=15, blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def save(self, *args, **kwargs):

        if not self.order_id:

            date = timezone.now().strftime("%y%m%d")

            random_no = random.randint(100000, 999999)

            self.order_id = f"GM{date}{random_no}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} | {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
