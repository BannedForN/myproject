from rest_framework import serializers
from knifestore.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'

class KnifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knife
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'