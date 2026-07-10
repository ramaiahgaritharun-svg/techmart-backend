from rest_framework import viewsets
from app.models import (Product,Cart,CartItem,Order,OrderItem,Wishlist,)
from app.serializers import (ProductSerializer,CartItemSerializer,WishlistSerializer,OrderSerializer,)
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=["post"])
    def update_qty(self, request, pk=None):
        item = self.get_object()
        qty = int(request.data.get("quantity", 1))
        item.quantity = qty
        item.save()
        return Response(self.get_serializer(item).data)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        return Response({"message": "cart cleared"})


class WishlistViewSet(viewsets.ModelViewSet):

    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )

        serializer = self.get_serializer(wishlist_item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        wishlist = self.get_object()
        wishlist.delete()
        return Response({"message": "Removed from wishlist"})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"message": "Cart is empty"}, status=400)

        order = Order.objects.create(
            user=request.user,
            full_name=request.data.get("full_name"),
            email=request.data.get("email"),
            mobile=request.data.get("mobile"),
            address=request.data.get("address"),
            total=0,
        )

        total = 0

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                return Response(
                    {
                        "message": f"{cart_item.product.name} has only {cart_item.product.stock} item(s) left in stock."
                    },
                    status=400,
                )

            OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
            )

            total += cart_item.product.price * cart_item.quantity
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        order.total = total
        order.save()
        cart_items.delete()

        try:

            send_mail(
                subject=f"Genmart Order {order.order_id}",
                message=f"""
                Hello {order.full_name},
                Your order has been placed successfully.
                Order ID : Order ID : {order.order_id}
                Total Amount : ₹{order.total}
                Thank you for shopping with Genmart.
                We'll notify you once your order is shipped.""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.email],
                fail_silently=True,
                )

        except Exception:
            pass

        serializer = self.get_serializer(order)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def register(request):
    if request.method == "GET":
        return Response({"message": "Register endpoint working"})

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    if not email:
        return Response({"field": "email", "message": "Email is required"}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return Response(
            {"field": "email", "message": "Enter a valid email address"}, status=400
        )
    if "@" not in email or "." not in email:
        return Response(
            {"field": "email", "message": "Invalid email format"}, status=400
        )
    if User.objects.filter(email=email).exists():
        return Response(
            {"field": "email", "message": "Email already registered"}, status=400
        )

    if password != confirm_password:
        return Response(
            {"field": "password", "message": "Passwords do not match"}, status=400
        )

    User.objects.create_user(username=username, email=email, password=password)

    return Response({"message": "Account created successfully"})


@api_view(["POST"])
def check_email(request):
    email = request.data.get("email")

    if not email:
        return Response({"exists": False, "message": "Email required"}, status=400)

    # validate format
    try:
        validate_email(email)
    except ValidationError:
        return Response({"exists": False, "message": "Invalid email"}, status=400)

    exists = User.objects.filter(email=email).exists()

    return Response({"exists": exists})


@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")

    if not email or not new_password:
        return Response({"message": "Email and new password required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "Email not found"}, status=404)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password updated successfully"})
