from rest_framework.routers import DefaultRouter
from django.urls import path
from app.views import *

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("cart", CartItemViewSet, basename="cart")
router.register("orders", OrderViewSet)
router.register("wishlist", WishlistViewSet, basename="wishlist")

urlpatterns = router.urls

urlpatterns += [
    path("register/", register, name="register"),
    path("check-email/", check_email),
    path("forgot-password/", forgot_password),
]
