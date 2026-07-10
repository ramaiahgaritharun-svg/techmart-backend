from django.contrib import admin
from app.models import *

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "quantity",
        "user",
    )

    def user(self, obj):
        return obj.cart.user.username

    user.short_description = "User"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "user",
    )

    def user(self, obj):
        return obj.order.user.username

    user.short_description = "User"
