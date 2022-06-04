from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price','created','last_updated','slug','category','inventory'
        ]
        read_only_fields = ['id','created','last_updated']