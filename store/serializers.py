from django.urls import reverse_lazy
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Product,Customer

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'address', 'phone',
                  'birth_date', 'membership', 'name']
        read_only_fields = ['id']

    def get_name(self,instance):
        return f'{instance.user.get_full_name()}'

class CustomerInlineSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'user']
        read_only_fields = ['id']

    def get_user(self, instance):
        return instance.user.username

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price','created','last_updated','slug','category','inventory'
        ]
        read_only_fields = ['id','created','last_updated']

class ProductInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price']
        read_only_fields = ['id', 'name', 'price']

class CartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='cart-detail')

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'total_price', 'url']
        read_only_fields = ['id', 'created_at', 'total_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInlineSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total']
        read_only_fields = ['id', 'cart','total']

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total']
        read_only_fields = ['id', 'cart','total']

    def create(self, validated_data):
        cart_id = self.context.get('cart_id')
        cart = Cart.objects.get(pk=cart_id)
        return CartItem.objects.create(cart=cart,**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    customer = CustomerInlineSerializer()
    class Meta:
        model = Order
        fields = ['id', 'customer', 'payment_status',
                  'placed_at', 'total', 'url']

class OrderCreateSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Order
        fields = ['id','cart_id']
        read_only_fields = ['id']


    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['request'].user
            customer = user.customer
            cart_id = validated_data.pop('cart_id')
            cart_items = Cart.objects.get(pk=cart_id).items.all()
            order = Order.objects.create(customer=customer)
            orderitems = [
                OrderItem.objects.create(
                    order=order,
                    product = item.product,
                    quantity=item.quantity,
                    item_price=item.product.price,
                )for item in cart_items
            ]
            return order


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductInlineSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order','product','quantity','item_price','total']
        read_only_fields = ['id','order','item_price','total']

