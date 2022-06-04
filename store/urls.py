
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet


router = DefaultRouter()
router.register('products',ProductViewSet,basename='products')
app_name = 'store'


urlpatterns = [
    path('', include(router.urls))
]
