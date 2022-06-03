from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("store:category-detail", kwargs={"pk": self.pk})
    

class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True,blank=True,related_name='products')
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"pk": self.pk})
    

class Cart(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('store:cart-detail', kwargs={"pk": self.pk})
        

    def total_price(self):
        total = sum([item.total for item in self.items.all()])
        return total

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self) -> str:
        return self.product.name

    @property
    def total(self):
        return self.product.price * Decimal(self.quantity)
        

class Customer(models.Model):

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.user.username}'

class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def user_all(self):
        pass

class Order(models.Model):

    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True,)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)

    def __str__(self) -> str:
        return f'Order {self.pk}'

    @property
    def total(self):
        return sum([item.total for item in self.items.all()])

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(default=1)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'orderitem {self.id}-{self.product}'

    @property
    def total(self):
        return self.item_price * Decimal(self.quantity)
