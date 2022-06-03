from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('',views.Index.as_view(),name='home'),
    path('products/',views.ProductList.as_view(),name='product-list'),
    path('products/<int:pk>/',views.ProductDetail.as_view(),name='product-detail'),
    path('cart/create', views.CartCreate.as_view(), name='cart-create'),
    path('cart/<uuid:uuid>/', views.CartDetail.as_view(), name='cart-detail'),
]
