from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('search/', views.ProductSearch.as_view(), name='product-search'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    # path('cart/create', views.CartCreate.as_view(), name='cart-create'),
    path('cart/<uuid:uuid>/', views.CartDetail.as_view(), name='cart-detail'),
    path('cart/items/<int:pk>/', views.CartItemUpdate.as_view(), name='cartitem-update'),
    path('cart/items/<int:pk>/delete', views.CartItemDelete.as_view(), name='cartitem-delete'),
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(),
         name='category-detail'),
]
