from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter
from django.urls import path, include
from store.views import CartItemViewSet, CartViewSet, OrderItemViewSet, OrderViewSet, ProductViewSet, CustomerViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')
router.register('order', OrderViewSet, basename='order')
router.register('customer', CustomerViewSet, basename='customer')

cart_item = NestedDefaultRouter(router, 'cart', lookup='cart')
cart_item.register('items', CartItemViewSet, basename='cart-items')

order_item = NestedDefaultRouter(router, 'order', lookup='order')
order_item.register('items', OrderItemViewSet, basename='order-items')


urlpatterns = [
    path('', include(router.urls),),
    path('', include(cart_item.urls),),
    path('', include(order_item.urls),),
]
