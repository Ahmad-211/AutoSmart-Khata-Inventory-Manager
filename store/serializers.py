from rest_framework import serializers
from .models import Customer, Part, Sale, SaleItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        # We don't include 'sale' here because it gets linked automatically
        fields = ['part', 'quantity', 'price_at_sale']

class SaleSerializer(serializers.ModelSerializer):
    # 'items' matches the related_name we set in models.py
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'customer', 'total_amount', 'payment_type', 'timestamp', 'items']

    def create(self, validated_data):
        # Extract the items data before saving the sale
        items_data = validated_data.pop('items')
        
        # Create the main Sale record
        sale = Sale.objects.create(**validated_data)
        
        # Create all SaleItems linked to this sale
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
            
        return sale